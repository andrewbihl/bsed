import sys
from os import path
import json
from .parser import TranslatorInterface
from typing import Optional


class Translator(TranslatorInterface):

    def __init__(self, translations_dir):
        self.translations_dir = translations_dir
        self.translations = {}

    def load_translations(self, translation_file: str) -> bool:
        if translation_file not in self.translations:
            try:
                with open(path.join(self.translations_dir, translation_file), 'r') as fin:
                    self.translations[translation_file] = json.load(fin)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                print('Invalid translation configuration.', file=sys.stderr)
                return False
        return True

    def translate(self, formatted_cmd, input_args: dict, translation_file: str) -> Optional[str]:
        if isinstance(formatted_cmd, list):
            formatted_cmd = ' '.join(formatted_cmd)
        if not isinstance(formatted_cmd, str):
            raise TypeError
        load_success = self.load_translations(translation_file)
        if not load_success:
            return None
        translation_dict = self.translations[translation_file]
        base_str = translation_dict[formatted_cmd]
        return base_str.format(**input_args)
