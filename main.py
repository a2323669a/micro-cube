from message_parser import Parser

with open('./data.txt', encoding='utf-8') as file:
    data = file.read()

data_list = data.split('\n')

parser = Parser()

for idx, line in enumerate(data_list):
    line = line.strip()
    result = parser.parse(line)
    print(idx+1, result)
