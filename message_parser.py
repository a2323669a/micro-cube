'''
Util File
'''

import re
from typing import List

class Parser:
    item_dict = {}

    def __init__(self, path, encoding='utf-8'):
        self.path = path
        with open(path, encoding=encoding) as file:
            data = file.read()
        data = data.split('\n')
        for idx, d in enumerate(data):
            result = re.match(r'(.*?)<(.*?)(<(.)>)*>(.*)', d)
            if result:
                name = result.group(2)
                value_type = result.group(4)
                rule_left = result.group(1)
                rule_right = result.group(5)
            else:
                if d.strip() == '':
                    continue
                elif d.startswith('#'):
                    continue
                else:
                    raise Exception('property file wrong. wrong rule is \"' + d + "\" in line " + str(idx))

            rule_left = self.replace(rule_left)
            rule_right = self.replace(rule_right)

            if name not in self.item_dict.keys():
                self.item_dict[name] = []

            char = '.'
            if value_type == 'd':
                char = '[0-9\.,，]'

            comp = '{}(\s*{}*?\s*){}'
            if rule_right == '':
                comp = '{}(\s*{}*\s*){}'

            self.item_dict[name].append(comp.format(rule_left, char, rule_right))

    def replace(self, line :str):
        line = line.replace('*', '.*?')
        line = line.replace('(', r"\(")
        line = line.replace(')', r'\)')

        return line

    def parse(self, content) -> dict:
        '''
        :param content:  message
        :return: a dict
        '''
        result_dict = {}

        for name, rules in self.item_dict.items():
            for rule in rules:
                result = re.findall(rule, content)
                if len(result) == 0:
                    continue

                result = set(result)
                if len(result) > 1:
                    result_dict[name] = list(result)[0] # More Error
                else:
                    result_dict[name] = list(result)[0]
                    break

            if name not in result_dict.keys():
                # result_dict[item.name] = 'Not Found' # Not Found Error
                pass

        return result_dict

    def parse_list(self, content_list :List[str]) -> List[dict]:
        return [self.parse(content) for content in content_list]
