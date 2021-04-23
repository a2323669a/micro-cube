'''
A sample for parsing message
'''

from message_parser import Parser

# read messages
with open('./data.txt', encoding='utf-8') as file:
    data = file.read()
data_list = data.split('\n') #

# new class Parser
parser = Parser()

for idx, line in enumerate(data_list):
    line = line.strip()
    result = parser.parse(line)  # parse message, return a dict
    print(idx+1, result)
