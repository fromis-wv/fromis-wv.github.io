import json

file_path = './python/test/data.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    test = json.load(file)
    data = test['data']
    print(len(data))
    # print(data[0])
    # for d in data:
    #     print(d)
    for k, v in data[0].items():
        print(k)