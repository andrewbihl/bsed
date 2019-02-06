import json
from enum import Enum, IntEnum


class Keyword(Enum):
    EVAL_PREFIX = '$EVAL__'
    EXPR_PREFIX = '$EXPR__'
    ROOT_TREE = 'main'
    USER_TEXT = '$USER_TEXT_INPUT'
    USER_INTEGER = '$USER_INTEGER_INPUT'
    USER_LINE_START_INDEX = '$USER_LINE_START_INDEX'  # int which must be shifted +1 for 0-indexing.
    USER_LINE_END_INDEX = '$USER_LINE_END_INDEX'  # int which must be compared to start for validity (>= start)
    TRANSLATIONS_FILE = '$translations_file_name'
    VAR_NAME = '$var_name'

    @staticmethod
    def prefix_key_to_identifier(s: str, kw):
        if kw not in [Keyword.EVAL_PREFIX, Keyword.EXPR_PREFIX]:
            return None
        if not s.startswith(kw.value):
            return None
        try:
            return s[len(kw.value):]
        except:
            return None

    @staticmethod
    def expr_key_to_identifier(s: str):
        return Keyword.prefix_key_to_identifier(s, Keyword.EXPR_PREFIX)

    @staticmethod
    def eval_key_to_identifier(s: str):
        return Keyword.prefix_key_to_identifier(s, Keyword.EVAL_PREFIX)


class InputType(IntEnum):
    COMMAND = 0
    USER_TEXT = 1
    USER_INTEGER = 2
    USER_LINE_START_INDEX = 3
    USER_LINE_END_INDEX = 4

    def is_integer(self):
        return InputType.USER_INTEGER <= self <= InputType.USER_LINE_END_INDEX

    def is_valid(self, text):
        if self.is_integer():
            try:
                _ = int(text)
            except ValueError:
                # Not an integer
                return False
        return True

    def token_str(self):
        return {
            InputType.USER_TEXT: Keyword.USER_TEXT.value,
            InputType.USER_INTEGER: Keyword.USER_INTEGER.value,
            InputType.USER_LINE_START_INDEX: Keyword.USER_LINE_START_INDEX.value,
            InputType.USER_LINE_END_INDEX: Keyword.USER_LINE_END_INDEX.value
        }.get(self, None)

    def validated_and_formatted(self, text):
        if self == InputType.USER_TEXT:
            return text
        if self == InputType.COMMAND:
            return text.lower()
        if self.is_integer():
            try:
                int_val = int(text)
            except ValueError:
                return None
            if self == InputType.USER_INTEGER.value:
                pass
            if self == InputType.USER_LINE_START_INDEX.value:
                if int_val < 0:
                    # Invalid range
                    return None
                int_val += 1
            if self == InputType.USER_LINE_END_INDEX.value:
                if int_val < 1:
                    return None
            return int_val
        return None


def keyword_to_user_input_type(kw: str):
    user_inputs = {Keyword.USER_TEXT.value: InputType.USER_TEXT,
                   Keyword.USER_INTEGER.value: InputType.USER_INTEGER,
                   Keyword.USER_LINE_START_INDEX.value: InputType.USER_LINE_START_INDEX,
                   Keyword.USER_LINE_END_INDEX.value: InputType.USER_LINE_END_INDEX}
    return user_inputs.get(kw, None)


class TokenNode:
    def __init__(self, text: str, children_nodes, depth: int, var_name=None):
        self.text = text
        self.children = children_nodes
        self.depth = depth
        self.var_name = var_name

    def __str__(self):
        children = sorted(self.children.values(), key=lambda x: x.longest_child())
        res = 'ROOT' if self.depth == 0 else ' ' * self.depth + '- ' + self.text
        for c in children:
            res += '\n'
            res += c.__str__()
        return res

    def is_root(self):
        return self.depth == 0

    def is_sub_expression(self):
        return self.text.startswith(Keyword.EXPR_PREFIX.value)

    def is_user_input(self):
        return self.text.startswith('$USER')

    def longest_child(self):
        return 0 if len(self.children) == 0 else max(c.depth for c in self.children.values())

    def terminates_command(self):
        next_nodes = [n for n in self.children.values() if isinstance(n, TokenNode)]
        return len(next_nodes) == 0


# TODO: Refactor
token_trees = {}


class TokenTree:
    def __init__(self, command_tree_spec: dict, root_key):
        self.command_tree_dict = command_tree_spec
        self.root = self.build_node_from_dict(self.command_tree_dict[root_key], '')
        self.line_range_start = None
        self.translation_file = self.command_tree_dict[root_key][Keyword.TRANSLATIONS_FILE.value]
        self.var_name = self.command_tree_dict[root_key].get(Keyword.VAR_NAME.value, None)

    def print_command_tree(self):
        print(self.root)

    @staticmethod
    def _update_leaves_of_dict(d: dict, addition: dict):
        if d == {}:
            d.update(addition)
        else:
            for child in d.values():
                TokenTree._update_leaves_of_dict(child, addition)

    def build_node_from_dict(self, node_dict: dict, node_text: str, start_depth=0):
        input_var_name = node_dict.get(Keyword.VAR_NAME.value)
        children_nodes = {}
        # if Keyword.REUSABLE_COMPONENTS.value in node:
        reusable_component_keys = {k for k in node_dict.keys() if k.startswith(Keyword.EVAL_PREFIX.value)}
        for key in reusable_component_keys:
            post_component_dict = node_dict.pop(key)
            identifier = Keyword.eval_key_to_identifier(key)
            # Gets the expanded form of the referenced component
            reusable_component_dict = self.command_tree_dict[identifier].copy()
            # Command continues after the reusable component. This continuation must be added.
            if len(post_component_dict) != 0:
                TokenTree._update_leaves_of_dict(reusable_component_dict, post_component_dict)
            node_dict.update(reusable_component_dict)

        sub_expression_keys = {k for k in node_dict.keys() if k.startswith(Keyword.EXPR_PREFIX.value)}
        for key in sub_expression_keys:
            identifier = Keyword.expr_key_to_identifier(key)
            if identifier not in token_trees:
                token_trees[identifier] = TokenTree(self.command_tree_dict, root_key=identifier)
            child_dict = node_dict[key]
            if not isinstance(child_dict, dict):
                continue
            child = self.build_node_from_dict(child_dict, key, start_depth + 1)
            children_nodes[key] = child

        normal_text_keys = [k for k in node_dict.keys() if k not in reusable_component_keys
                            and k not in sub_expression_keys
                            and k != Keyword.VAR_NAME.value]
        for child_text in normal_text_keys:
            child_dict = node_dict[child_text]
            if not isinstance(child_dict, dict):
                continue
            child = self.build_node_from_dict(child_dict, child_text, start_depth + 1)
            children_nodes[child_text] = child
        return TokenNode(node_text, children_nodes, start_depth, input_var_name)

    @classmethod
    def from_json(cls, command_tree_file):
        with open(command_tree_file, 'r') as fin:
            tree_dict = json.load(fin)
        tree = TokenTree(tree_dict, root_key=Keyword.ROOT_TREE.value)
        token_trees[Keyword.ROOT_TREE.value] = tree
        return tree
