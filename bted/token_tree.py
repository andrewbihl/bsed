import json
import logging
from enum import Enum
import bted.definitions as definitions


class Keyword(Enum):
    REUSABLE_COMPONENTS = 'reusable_components'
    ROOT = 'root'
    USER_TEXT = '$USER_TEXT_INPUT'
    USER_INTEGER = '$USER_INTEGER_INPUT'


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
            return self.children[arg_text], 0
        if Keyword.USER_TEXT.value in self.children.keys():
            return self.children[Keyword.USER_TEXT.value], 1
        if Keyword.USER_INTEGER.value in self.children.keys():
            return self.children[Keyword.USER_INTEGER.value], 2
        return None, False

    def terminates_command(self):
        return len(self.children) == 0


class TokenTree:

    def __init__(self, command_tree: dict, translations: dict):
        self.command_tree = command_tree
        self.command_translations = translations
        self.root = self.enumerate_node_dict(self.command_tree['root'], '')

    @staticmethod
    def normalized_command_string(command_nodes: [TokenNode]):
        res = ' '.join([node.text for node in command_nodes])
        return res

    def print_command_tree(self):
        print(self.root)

    def validate_command(self, command_statement: [str]):
        user_text_inputs = []
        if isinstance(command_statement, str):
            command_statement = command_statement.split()
        if not isinstance(command_statement, list):
            raise TypeError

        def step(node: TokenNode, text: str):
            next_node, input_type = node.next_node(text.lower())
            if input_type == 1:
                return next_node, text
            elif input_type == 2:
                try:
                    _ = int(text)
                    return next_node, text
                except TypeError:
                    # Invalid input
                    return None, None
            return next_node, None

        command_nodes = []
        curr_node = self.root
        for command_word in command_statement:
            curr_node, user_input_word = step(curr_node, command_word)
            if curr_node is None:
                return None, None
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

    def enumerate_node_dict(self, node: dict, node_text: str, start_depth=0):
        children_nodes = {}
        if Keyword.REUSABLE_COMPONENTS.value in node:
            reusable_component_identifiers = node.pop(Keyword.REUSABLE_COMPONENTS.value)
            for identifier in reusable_component_identifiers:
                node.update(self.command_tree[Keyword.REUSABLE_COMPONENTS.value][identifier])
        for child_text, child_dict in node.items():
            child = self.enumerate_node_dict(child_dict, child_text, start_depth + 1)
            children_nodes[child_text] = child
        return TokenNode(node_text, children_nodes, start_depth)

    @classmethod
    def from_json(cls, command_tree_file, translations_file):
        with open(command_tree_file, 'r') as fin:
            tree_dict = json.load(fin)
        with open(translations_file, 'r') as fin:
            command_translations = json.load(fin)
        return TokenTree(tree_dict, command_translations)
