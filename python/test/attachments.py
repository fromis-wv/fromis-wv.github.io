import json

import re

text = '''
베타 진짜 예쁘고 침대에서 쉬는 거 너무 귀여워
나도 키우고 싶은데 아직 자신이 없어😞
언젠간 키우겠지?
<w:attachment type="snippet" id="0-6222514" /><w:attachment type="photo" id="3-246941259" /><w:attachment type="photo" id="4-247377760" />
'''

matches = re.findall(r'type="([^"]+)"', text)
print(matches)

# attachments = set()
#
# file_path = 'raw/nagyung/comments.json'
# with open(file_path, 'r', encoding='utf-8') as file:
#     # print('Loading json')
#     test1 = json.load(file)
#     datas = test1['data']
#     for data in datas:
#         body = data['root']['data']['body']
#
#
#         matches = re.findall(r'<w:attachment type="([^"]+)"', text)
#
#         if 'snippet' in body:
#             print(body)
#             print('HAS SNIPPET')
#             print(matches)
#
#         # for m in matches:
#             # attachments.add(m)
#         attachments.update(set(matches))
#     print(attachments)