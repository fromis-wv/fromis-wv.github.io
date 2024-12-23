# import base64
# import hashlib
# import hmac
# import time
#
# import requests
#
# import yt_dlp
#
# # def _call_api(self, ep, video_id, data=None, note='Downloading API JSON'):
# #     # Ref: https://ssl.pstatic.net/static/wevweb/2_3_2_11101725/public/static/js/2488.a09b41ff.chunk.js
# #     # From https://ssl.pstatic.net/static/wevweb/2_3_2_11101725/public/static/js/main.e206f7c1.js:
# #     key = b'1b9cb6378d959b45714bec49971ade22e6e24e42'
# #     # api_path = update_url_query(ep, {
# #     #     # 'gcc': 'US',
# #     #     'appId': 'be4d79eb8fc7bd008ee82c8ec4ff6fd4',
# #     #     'language': 'en',
# #     #     'os': 'WEB',
# #     #     'platform': 'WEB',
# #     #     'wpf': 'pc',
# #     # })
# #
# #     key = b'1b9cb6378d959b45714bec49971ade22e6e24e42'
# #     api_path = 'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc'
# #     wmsgpad = int(time.time() * 1000)
# #     wmd = base64.b64encode(hmac.HMAC(key, f'{api_path[:255]}{wmsgpad}'.encode(), digestmod=hashlib.sha1).digest()).decode()
#
# url = 'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments'
#
# key = b'1b9cb6378d959b45714bec49971ade22e6e24e42'
# api_path = 'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc'
# wmsgpad = int(time.time() * 1000)
# wmd = base64.b64encode(hmac.HMAC(key, f'{url[:255]}{wmsgpad}'.encode(), digestmod=hashlib.sha1).digest()).decode()
#
# print(wmsgpad)
# print(wmd)
#
# # url = "https://global.apis.naver.com/weverse/wevweb/post/v1.0/community-36/artistTabPosts"
# params = {
#     "fieldSet": "memberCommentsV1",
#     "sortType": "LATEST",
#     "appId": "be4d79eb8fc7bd008ee82c8ec4ff6fd4",
#     "language": "en",
#     "os": "WEB",
#     "platform": "WEB",
#     "wpf": "pc",
#     "wmsgpad": wmsgpad,
#     "wmd": wmd
# }
#
# headers = {
#     "accept": "application/json, text/plain, */*",
#     "accept-language": "en-US,en;q=0.9",
#     "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwMTVmNzg5NGRlNzk0YzJmOWM0N2I2YmNjMmUwMTM0Nzo4OSIsInN1YiI6IjIzYmEyZmUxZGU0YzRjOTM4MjAwYTg2MWQ2OGZiYTZlMDEwIiwiaWF0IjoxNzM0MTgxNDE2LCJleHAiOjE3MzQ0NDA2MTYsImlzcyI6Imh0dHBzOi8vYWNjb3VudGFwaS53ZXZlcnNlLmlvIiwiYXVkIjoiaHR0cHM6Ly9hY2NvdW50YXBpLndldmVyc2UuaW8iLCJ2ZXIiOjIsImNsaWVudF9pZCI6IndldmVyc2UiLCJwbGF0Zm9ybSI6IldFQiIsInNvY2lhbC5wcm92aWRlciI6IkdPT0dMRSIsInNvY2lhbC51aWQiOjE0NDQ4Njg2fQ.8aS_it0r85mNt6HnospB8kbDBT9W_5-f4SiE6zu6CT0",
#     "priority": "u=1, i",
#     "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "cross-site",
#     "wev-device-id": "25057b37-b262-4392-be76-10767c22eee5",
#     "wev-open-community": "A",
# }
#
# response = requests.get(url, headers=headers, params=params)
#
# print(response.status_code)
# print(response.json())

    # 'gyuri': 'db56036fc59a94a9ef617261c90c783f'
    # 'hayoung': '67b4c6fb2220ac6705aa97046f3503a1'
    # 'jiheon': '5fb309bc7489a576484431ba8338807e'


import yt_dlp

from yt_dlp.extractor.weverse import WeverseIE
from yt_dlp.extractor.weverse import WeverseMomentIE

test = 2

'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/post-0-153668910/comments?fieldSet=postCommentsV1&limit=50&sortType=LATEST&startFrom=first&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734588229580&wmd=wGM70VYJTV7M8IX3mhmqZF%2FWStw%3D'


'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-1-129461834?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734589572134&wmd=%2BK%2FYWDRECmo0K0QUHm4JwmQLiXQ%3D'
'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/post-1-129461834/artistComments?fieldSet=postArtistCommentsV1&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734589572935&wmd=pSP9mzJMRxvd0vBDfGKPkX5ToXQ%3D'


'https://global.apis.naver.com/weverse/wevweb/post/v1.0/member-65eff6ab044ae8dea6816794f11a6fc1/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1&filterType=MOMENT&language=en&limit=1&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734590129933&wmd=9CTKP5QFJvSjLddA7XoeT%2FYPvos%3D'


params = {
    'verbose': True,
    'cookiesfrombrowser': ('firefox',),
}

ydl = yt_dlp.YoutubeDL(params)

post = '1-129409199'

member = 'db56036fc59a94a9ef617261c90c783f'

if test == 1:
    url = 'https://weverse.io/fromis9/moment/5fb309bc7489a576484431ba8338807e/post/1-129461834'
    info = ydl.extract_info(url, download=False)
    print(info)

    # 'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-0-153668910?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734588229189&wmd=EKlZsXsaS%2BiPiPXYfviSYGVMQSg%3D'
    'post-0-153668910?fieldSet=postV1'

if test == 2:
    thing = WeverseIE()
    thing.set_downloader(ydl)
    # thing.initialize()
    thing._initialize_pre_login()
    thing._real_initialize()
    thing._ready = True
    # req = "https://weverse-rmcnmv.akamaized.net/c/read/v2/VOD_ALPHA/weverse-moment_2023_11_11_0/3c6615ec-7fe7-11ee-90f9-a0369fff69c0.mp4?__gda__=1734588957_5761ac4b4ddd09a00b8c5eb0dfd2b398"
    # req = '/post/v1.0/post-1-129461834/preview?fieldSet=postV1'
    req = '/post/v1.0/post-1-129461834?fieldSet=postV1'

    req = '/post/v1.0/post-1-129461834/preview?fieldSet=postV1'


    req = f'/comment/v1.0/post-{post}/artistComments?fieldSet=postArtistCommentsV1'

    # 'https://weverse.io/fromis9/moment/5fb309bc7489a576484431ba8338807e/post/1-129461834'
    # req = '/post-0-153668910/comments?fieldSet=postCommentsV1'
    # req = '/post-0-153668910/comments?fieldSet=postCommentsV1'

    req = '/post/v1.0/member-65eff6ab044ae8dea6816794f11a6fc1/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1'
    req = '/post/v1.0/member-6599dbbcaa26237c2ab0f3becb421b45/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1'

    req = '/post/v1.0/member-db56036fc59a94a9ef617261c90c783f/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1'

    # 'https://global.apis.naver.com/weverse/wevweb/comment/v1.0/member-6aa813460d109e841afc9ac410f25226/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734590393752&wmd=KCsF9Bx6avMI3EDGwTchW5o4W6I%3D'

    # req = '/comment/v1.0/member-6aa813460d109e841afc9ac410f25226/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4'
    req = '/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments?fieldSet=memberCommentsV1&sortType=LATEST'

    req = '/post/v1.0/community-36/artistTabPosts?fieldSet=postsV1&after=1726690555959%2C31862'

    req = f'/post/v1.0/post-1-119817916?fieldSet=postV1&lockPassword=0124'

    req = '/post/v1.0/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&lockPassword='

    req = '/chat/v1.0/chat-N1Uhih/artistMessages'

    # req = '/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot'
    # '/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&lockPassword=&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734599893718&wmd=fd1DgvDuEQIBFjacLdz%2F5K3KQas%3D'

    'https://global.apis.naver.com/weverse/wevweb/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=ko&os=WEB&platform=WEB&wpf=pc'

    'https://global.apis.naver.com/weverse/wevweb/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&lockPassword=%22%22&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=ko&os=WEB&platform=WEB&wpf=pc'

    'https://global.apis.naver.com/weverse/wevweb/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=ko&os=WEB&platform=WEB&wpf=pc'
    # req = '/post/v1.0/member-db56036fc59a94a9ef617261c90c783f/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1&filterType=DEFAULT&language=en&limit=20&os=WEB&platform=WEB&sortType=LATEST&wpf=pc'

    'https://global.apis.naver.com/weverse/wevweb/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&lockPassword=&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=ko&os=WEB&platform=WEB&wpf=pc'

    thing_out = thing._call_api(req, '')
    print(thing_out)

else:
    # '/post/v1.0/post-1-129461834/preview?fieldSet=postV1'
    # 'https://weverse-rmcnmv.akamaized.net/c/read/v2/VOD_ALPHA/weverse-moment_2023_11_11_0/3c6615ec-7fe7-11ee-90f9-a0369fff69c0.mp4?__gda__=1734588957_5761ac4b4ddd09a00b8c5eb0dfd2b398'

    # yt_dlp.extractor()
    #
    thing = WeverseIE()
    thing.set_downloader(ydl)
    thing.initialize()
    # req = "https://weverse-rmcnmv.akamaized.net/c/read/v2/VOD_ALPHA/weverse-moment_2023_11_11_0/3c6615ec-7fe7-11ee-90f9-a0369fff69c0.mp4?__gda__=1734588957_5761ac4b4ddd09a00b8c5eb0dfd2b398"
    req = '/post/v1.0/post-1-129461834/preview?fieldSet=postV1'
    thing_out = thing._call_api(req, '1-129461834')
    print(thing_out)




    # WeverseBaseIE._call_api()
    # yt_dlp.extractor

# WDM4A9C7A6

# https://global.apis.naver.com/weverse/wevweb/dm/v1.1/rooms/321529?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734736687399&wmd=tFxi%2FOoDLGZETDeOZTqd60lemSo%3D
# https://global.apis.naver.com/weverse/wevweb/dm/v1.1/rooms/321529/messages?prev=9223372036854775807&transLang=en&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734736687860&wmd=rhLrdVnWaTLan7H8ZSFkTPn%2BZcE%3D