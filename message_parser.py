'''
Util File
'''

import re
from typing import List

class Item:
    name = None

    strict_rule_list :List = []

    def __init__(self, name, strict_rule_list):
        self.name = name
        self.strict_rule_list = strict_rule_list

class Parser:
    item_list = [
        Item('账户',[(r'(?<!保单)(尾|尾号|贵账|账户|卡号).{0,2}?\s*([0-9]{2,})\s*[^\d年月日\s]', 1),]),
        Item('收入', [('(汇入的|汇入|收入|转入|增加人民币|转存人民币|入账款项，人民币|汇款|入账工资，人民币)\s*([0-9\.,].*?)[，。]', 1), ('收入（.*?）([0-9\.].*?)[，]', 0)]),
        Item('支出', [('(扣贷款|转出|转支金额|支出\(消费\)|成功转账，金额|支出人民币|消费|折现金取金额|汇兑金额|支付|扣款指出|入账工资，人民币|实扣)\s*([0-9\.,].*?)[，。]', 1)]),
        Item('手续费', [('手续费金额([0-9\.]*元)', 0)]),
        Item('交易金额', [('(汇入的|汇入|收入|转入|增加人民币|转存人民币|入账款项，人民币|汇款|入账工资，人民币)\s*([0-9\.,].*?)[，。]', 1),
                      ('收入（.*?）([0-9\.].*?)[，]', 0),
                      ('(扣贷款|转出|转支金额|支出\(消费\)|成功转账，金额|支出人民币|消费|折现金取金额|汇兑金额|支付|扣款指出|入账工资，人民币|实扣)\s*([0-9\.,].*?)[，。]', 1)]),
        Item('交易对手', [('由(.*?)汇入', 0), ('银行收入（(.*?)）', 0), ('(付款方|对方信息)：([^，]*)', 1),
                        ('[：，](.*)于[\d]+', 0), ('向(.*?)支付[\d]+', 0)
        ]),
        Item('摘要', [('摘要：([^\[]*)', 0)],),
        Item('交易银行', [('【(.*)银行】', 0), ('\[(.*)银行\]', 0), ('([^，]{2})银行' ,0), ('中国(邮政)' ,0)]),
    ]

    def __init__(self):
        pass

    def parse(self, content) -> dict:
        '''
        :param content:  message
        :return: a dict
        '''
        result_dict = {}

        for item in self.item_list:
            for rule, posi in item.strict_rule_list:
                result = re.findall(rule, content)
                if len(result) == 0:
                    continue

                if posi != 0:
                    result = [r[posi] for r in result]

                result = set(result)
                if len(result) > 1:
                    result_dict[item.name] = list(result)[0] # More Error
                else:
                    result_dict[item.name] = list(result)[0]
                    break

            if item.name not in result_dict.keys():
                # result_dict[item.name] = 'Not Found' # Not Found Error
                pass

        return result_dict

    def parse_list(self, content_list :List[str]) -> List[dict]:
        return [self.parse(content) for content in content_list]
