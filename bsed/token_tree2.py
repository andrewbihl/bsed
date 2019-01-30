from os import path
import json
import logging
from enum import Enum, IntEnum
import bsed.definitions as definitions


class Keyword(Enum):
    EVAL_PREFIX = '$EVAL__'
    EXPR_PREFIX = '$EXPR__'
    ROOT = '$ROOT'
    USER_TEXT = '$USER_TEXT_INPUT'
    USER_INTEGER = '$USER_INTEGER_INPUT'
    USER_LINE_START_INDEX = '$USER_LINE_START_INDEX'  # int which must be shifted +1 for 0-indexing.
    USER_LINE_END_INDEX = '$USER_LINE_END_INDEX'  # int which must be compared to start for validity (>= start)
    TRANSLATIONS_FILE = '$translations_file_name'
    VAR_NAME = '$var_name'

    @staticmethod
    def keyword_type(word: str):
        for prefix in [Keyword.EXPR_PREFIX, Keyword.EVAL_PREFIX]:
            if word.startswith(prefix.value):
                return prefix
        for kw in [Keyword.ROOT, Keyword.USER_TEXT, Keyword.USER_INTEGER, Keyword.USER_LINE_START_INDEX,
                   Keyword.USER_LINE_END_INDEX, Keyword.TRANSLATIONS_FILE, Keyword.VAR_NAME]:
            if word == kw.value:
                return kw
        return None


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
            except TypeError:
                # Not an integer
                return False
        return True


class TokenNode:
    def __init__(self, text: str, children_nodes, depth: int):
        self.text = text
        self.children = children_nodes
        self.depth = depth

    def __str__(self):
        children = sorted(self.children.values(), key=lambda x: x.longest_child())
        res = 'ROOT' if self.depth == 0 else ' ' * self.depth + '- ' + self.text
        for c in children:
            res += '\n'
            res += c.__str__()
        return res

    def longest_child(self):
        return 0 if len(self.children) == 0 else max(c.depth for c in self.children.values())

    def next_node(self, arg_text):
        """
        Gets the next node for interpreting the command, if there is one.
        :param arg_text: The text of the next component of the command statement
        :return: The node for the next word, and True if the node returns is a USER_INPUT_TEXT node
        """
        if arg_text in self.children.keys():
            return self.children[arg_text], InputType.COMMAND
        for input_kw, input_type in [(Keyword.USER_TEXT, InputType.USER_TEXT),
                                     (Keyword.USER_INTEGER, InputType.USER_INTEGER),
                                     (Keyword.USER_LINE_START_INDEX, InputType.USER_LINE_START_INDEX),
                                     (Keyword.USER_LINE_END_INDEX, InputType.USER_LINE_END_INDEX)]:
            if input_kw.value in self.children.keys():
                if input_type.is_valid(arg_text):
                    return self.children[input_kw.value], input_type
        # if Keyword.USER_TEXT.value in self.children.keys():
        #     return self.children[Keyword.USER_TEXT.value], InputType.USER_TEXT
        # if Keyword.USER_INTEGER.value in self.children.keys():
        #     return self.children[Keyword.USER_INTEGER.value], InputType.USER_INTEGER
        # if Keyword.USER_LINE_START_INDEX.value in self.children.keys():
        #     return self.children[Keyword.USER_LINE_START_INDEX.value], InputType.USER_LINE_START_INDEX
        # if Keyword.USER_LINE_END_INDEX.value in self.children.keys():
        #     return self.children[Keyword.USER_LINE_END_INDEX.value], InputType.USER_LINE_END_INDEX
        return None, None

    def possible_succeeding_expression_types(self):
        """

        :return: The list of expression types which can follow the node.
        """
        expr_keys = [k[len(Keyword.EXPR_PREFIX.value):] for k in self.children.keys()
                     if k.startswith(Keyword.EXPR_PREFIX.value)]
        return expr_keys

    def terminates_command(self):
        # next_nodes = [n for n in self.children.values() if isinstance(n, dict)]
        # return len(next_nodes) == 0
        return len(self.children) == 0


token_trees = {}


class TokenTree:
    def __init__(self, command_tree_spec: dict, translations_dir: str, root_key):
        translations_file = path.join(translations_dir, command_tree_spec[root_key][Keyword.TRANSLATIONS_FILE.value])
        with open(translations_file, 'r') as fin:
            self.command_translations = json.load(fin)
        self.command_tree_dict = command_tree_spec
        self.translations_dir = translations_dir
        self.root = self.build_node_from_dict(self.command_tree_dict[root_key], '')
        self.line_range_start = None

    @staticmethod
    def normalized_command_string(command_nodes: [TokenNode]):
        res = ' '.join([node.text for node in command_nodes])
        return res

    def print_command_tree(self):
        print(self.root)

    def validate_command(self, command_statement: [str], tree_identifier=Keyword.ROOT.value):
        user_text_inputs = []
        if isinstance(command_statement, str):
            command_statement = command_statement.split()
        if not isinstance(command_statement, list):
            raise TypeError

        def step(node: TokenNode, text: str):
            next_node, input_type = node.next_node(text.lower())
            if next_node is None:
                return None, None
            if not input_type.is_valid(text):
                return None, None
            if input_type == InputType.USER_TEXT.value:
                return next_node, text
            int_val = None
            if input_type.is_integer():
                print(text)
                int_val = int(text)
            if input_type == InputType.USER_INTEGER.value:
                return next_node, text
            if input_type == InputType.USER_LINE_START_INDEX.value:
                index = int_val + 1
                if index < 0:
                    # Invalid range
                    return None, None
                self.line_range_start = index
                return next_node, str(index)
            if input_type == InputType.USER_LINE_END_INDEX.value:
                index = int_val
                if self.line_range_start is None:
                    # No start index already stored
                    return None, None
                if index < self.line_range_start:
                    # Invalid range
                    return None, None
                return next_node, str(index)
            return next_node, None

        command_nodes = []
        curr_node = token_trees[tree_identifier].root
        for i, command_word in enumerate(command_statement):
            sub_expression_keys = [k for k in curr_node.children if k.startswith(Keyword.EXPR_PREFIX.value)]
            curr_node, user_input_word = step(curr_node, command_word)
            if curr_node is None:
                if len(sub_expression_keys) == 0:
                    return None, None
                results = [self.validate_command(command_statement[i:], tree_identifier=k[len(
                    Keyword.EXPR_PREFIX.value):]) for k in sub_expression_keys]
            command_nodes.append(curr_node)
            if user_input_word is not None:
                user_text_inputs.append(user_input_word)

        valid_command = command_nodes[-1].terminates_command()
        if valid_command:
            normalized_cmd = TokenTree.normalized_command_string(command_nodes)
            if normalized_cmd in self.command_translations:
                return self.command_translations[normalized_cmd], user_text_inputs
            else:
                logging.error('Not yet implemented command of form: \"%s\"' % normalized_cmd)
        return None, None

    @staticmethod
    def _update_leaves_of_dict(d: dict, addition: dict):
        if d == {}:
            d.update(addition)
        else:
            for child in d.values():
                TokenTree._update_leaves_of_dict(child, addition)

    def build_node_from_dict(self, node: dict, node_text: str, start_depth=0):
        children_nodes = {}
        # if Keyword.REUSABLE_COMPONENTS.value in node:
        reusable_component_keys = {k for k in node.keys() if k.startswith(Keyword.EVAL_PREFIX.value)}
        for key in reusable_component_keys:
            post_component_dict = node.pop(key)
            identifier = key[len(Keyword.EVAL_PREFIX.value):]
            # Gets the expanded form of the referenced component
            reusable_component_dict = self.command_tree_dict[identifier].copy()
            # Command continues after the reusable component. This continuation must be added.
            # after_reusable_component = reusable_components[identifier]
            if len(post_component_dict) != 0:
                TokenTree._update_leaves_of_dict(reusable_component_dict, post_component_dict)
            node.update(reusable_component_dict)

        sub_expression_keys = {k for k in node.keys() if k.startswith(Keyword.EXPR_PREFIX.value)}
        for key in sub_expression_keys:
            identifier = key[len(Keyword.EVAL_PREFIX.value):]
            if identifier not in token_trees:
                token_trees[identifier] = TokenTree(self.command_tree_dict, self.translations_dir, root_key=identifier)
            child_dict = node[key]
            if not isinstance(child_dict, dict):
                continue
            child = self.build_node_from_dict(child_dict, key, start_depth + 1)
            children_nodes[key] = child

        normal_text_keys = [k for k in node.keys() if k not in reusable_component_keys and k not in sub_expression_keys]
        for child_text in normal_text_keys:
            child_dict = node[child_text]
            if not isinstance(child_dict, dict):
                continue
            child = self.build_node_from_dict(child_dict, child_text, start_depth + 1)
            children_nodes[child_text] = child
        return TokenNode(node_text, children_nodes, start_depth)

    @classmethod
    def from_json(cls, command_tree_file, translations_dir):
        with open(command_tree_file, 'r') as fin:
            tree_dict = json.load(fin)
        tree = TokenTree(tree_dict, translations_dir, root_key=Keyword.ROOT.value)
        token_trees[Keyword.ROOT.value] = tree
        return tree


def parse_command(command_statement: [str], trees: dict[str:TokenTree],
                  tree_identifier=Keyword.ROOT.value, prev_node: TokenNode=None) -> (str, dict):
    input_vars = {}
    if isinstance(command_statement, str):
        command_statement = command_statement.split()
    if not isinstance(command_statement, list):
        raise TypeError
    # Start of expression parse
    if prev_node is None:
        node = [trees[tree_identifier].root]
        return parse_command(command_statement, trees, tree_identifier, node)
    arg = command_statement[0]
    node, input_type = prev_node.next_node(arg)
    is_user_input = input_type != InputType.COMMAND
    if is_user_input:
        var_name = node.children[Keyword.VAR_NAME.value]
        if input_type.is_integer():
            value = int(arg)
    eval_keys = [kw for kw in prev_node.children if
