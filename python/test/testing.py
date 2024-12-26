import datetime
import json
import os.path

import yt_dlp
import time

from yt_dlp.extractor.weverse import WeverseIE
from yt_dlp.utils import ExtractorError

members = {
    'jiheon': '5fb309bc7489a576484431ba8338807e',  # jh
    'hayoung': '67b4c6fb2220ac6705aa97046f3503a1',  # hy
    'chaeyoung': '65eff6ab044ae8dea6816794f11a6fc1',  # cy
    'jiwon': '6599dbbcaa26237c2ab0f3becb421b45',  # jw
    'jisun': '01435f74a49ba8a519705ad242348232',  # js
    'saerom': '326c0d1e7045798aa3964e2028c34628',  # sr
    'seoyeon': '56bdfafb606d9ce1b4ecdd572595e242',  # sy
    'nagyung': '5477d46be848bd40252f9d13ef62cb4d',  # ng
    'gyuri': 'db56036fc59a94a9ef617261c90c783f'  # gr
}

params = {
    # 'verbose': True,
    'quiet': True,
    'cookiesfrombrowser': ('firefox',),
}

def make_extractor():
    ydl = yt_dlp.YoutubeDL(params)

    ext = WeverseIE()
    ext.set_downloader(ydl)
    ext.initialize()
    # ext._initialize_pre_login()
    # ext._real_initialize()
    # ext._ready = True
    return ext

def get_next_page(json_data):
    paging = json_data['paging']
    if param := paging.get('nextParams'):
        return param['after'].replace(',', '%2C')

    return None

def get_prev_page(json_data):
    paging = json_data['paging']
    if param := paging.get('previousParams'):
        if prev:= param.get('prev'):
            return prev.replace(',', '%2C')

        if prev:= param.get('before'):
            return prev.replace(',', '%2C')

        breakpoint()

    return None

def run_extr(extr, req, out_data=None, grab_data=True):
    print(req)

    while True:
        try:
            json_data = extr._call_api(req, '')
            print(json_data)
            break
        except Exception as e:
            print(e)
            breakpoint()
            time.sleep(5.0)

    if out_data is not None:
        if grab_data:
            post_data = json_data['data']
            out_data += post_data
            print(f'Found data {len(post_data)} Data: {len(out_data)}')
        else:
            out_data.append(json_data)
            print(len(out_data))

    return json_data


def write_all_requests(req, initial_req, filename, use_after, skip_exists=False):
    if skip_exists:
        if os.path.exists(filename):
            return

    extr = make_extractor()

    out_data = []

    next_page = None

    prev = None
    after = None

    ids = set()

    initial = initial_req

    while True:
        mod_req = req

        if initial:
            mod_req = initial
            initial = None

        if use_after and after:
            mod_req += f'&after={after}'
        elif not use_after and prev:
            mod_req += f'?prev={prev}'

        print(req)

        # req = '/post/v1.0/community-36/artistTabPosts?fieldSet=postsV1'
        data = run_extr(extr, mod_req, out_data)
        # print(data)
        prev = get_prev_page(data)
        after = get_next_page(data)

        for d in data['data']:
            ids.add(d['postId'])
        print(len(ids))
        # print(paging)

        # new_msgs = []
        # # print('Data', len(data['data']))
        # for msg in data['data']:
        #     msg_id = int(msg['messageId'])
        #     if msg_id in messages:
        #         continue
        #
        #     messages.add(msg_id)
        #     new_msgs.append(msg)

        # print('New msgs', len(new_msgs))
        #     # body = msg['body']
        #     # print('Body', len(body))
        #     for b in msg['body']:
        #         print(b['value'])

        if use_after and not after:
            break
        elif not use_after and not prev:
            break
        # if not paging.get('after'):
        #     break

        time.sleep(.5)

        # count += 1
        # if count > 5:
        #     break

    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        # Write the array as JSON
        json.dump(out_data, file)

def write_single(req, filename, skip_exists=True):
    file_path = f'{filename}.json'
    if skip_exists and os.path.exists(file_path):
        return False

    extr = make_extractor()
    data = run_extr(extr, req)
    with open(file_path, 'w') as file:
        # Write the array as JSON
        json.dump(data, file)
        return True


def write_multiple(reqs, filename, grab_data):
    out_data = []
    for req in reqs:
        extr = make_extractor()
        try:
            run_extr(extr, req, out_data, grab_data)
        except Exception as e:
            print(e)
            break
        time.sleep(1.0)

    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        # Write the array as JSON
        json.dump(out_data, file)

def write_all_lives():
    posts = []

    with open(f'raw/post-data/liveTabPosts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            posts.append(data['postId'])

    posts = [f'/post/v1.0/post-{p}?fieldSet=postV1' for p in posts]
    # posts = posts[:5]
    # for p in posts:
    #     print(p)
    # ['/post/v1.0/post-0-152103623?fieldSet=postV1', '/post/v1.0/post-4-104688875?fieldSet=postV1']
    write_multiple(posts, 'raw/post-data/all_live_posts', False)

def write_all_post_media():
    posts = []

    with open(f'raw/post-data/searchAllMedia.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            posts.append(data['postId'])

    # posts = [f'/post/v1.0/post-{p}?fieldSet=postV1' for p in posts]
    # posts = posts[:5]
    # for p in posts:
    #     print(p)
    # ['/post/v1.0/post-0-152103623?fieldSet=postV1', '/post/v1.0/post-4-104688875?fieldSet=postV1']
    # write_multiple(posts, 'raw/post-data/AllMedia', False)

    for i, p in enumerate(posts):
        req = f'/post/v1.0/post-{p}?fieldSet=postV1'
        if write_single(req, f'raw/post-data/media/{p}', True):
            print(i, '/', len(posts))
            time.sleep(3)


def write_all_live_comments():
    posts = []

    with open(f'raw/post-data/all_live_posts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            postId = data['postId']
            media_info = data['extension']['mediaInfo']
            if chat := media_info.get('chat'):
                artist_msgs = chat['artistMessages']
                if len(artist_msgs['data']):
                    posts.append((chat['chatId'], data))
            else:
                print('No chat id?', postId, data['shareUrl'])
                break

    # posts = posts[:5]
    for chatId, data in posts:
        postId = data['postId']
        req = f'/chat/v1.0/chat-{chatId}/artistMessages'
        print(req, postId, data['shareUrl'])
        write_all_requests(req, req, f'raw/post-data/liveChat/{postId}', True, True)

# DM - not useful?
'/dm/v1.1/rooms/233441/messages?prev=9223372036854775807'
'/post/v1.0/community-36/liveTabPosts'
# '/post/v1.0/post-0-152103623?fieldSet=postV1'
'/chat/v1.0/chat-N1Uhih/artistMessages?after=1731239924958%2C65eff6ab044ae8dea6816794f11a6fc1&limit=50&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734821629641&wmd=kLQ0UPASNYRjpKwwCrJ2NEBhlCw%3D'
'/chat/v1.0/chat-N1RpH-/artistMessages?after=1728657034748%2C6599dbbcaa26237c2ab0f3becb421b45&limit=50&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734824539937&wmd=WclqbqNrV3vDU2vwdby%2FOKWl0vA%3D'
'/media/v1.0/community-36/searchAllMedia?after=1722342300000%2C1722316670967&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1&gcc=AU&language=en&os=WEB&platform=WEB&sortOrder=DESC&wpf=pc&wmsgpad=1734826385640&wmd=s30OGAB32aQptBPF1%2Bpyi%2FbFiBg%3D'

'/post/v1.0/member-5fb309bc7489a576484431ba8338807e/posts?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postsV1&filterType=MOMENT&language=en&limit=1&os=WEB&platform=WEB&wpf=pc&wmsgpad=1735177267178&wmd=CeJPpNXyWd2bO4aXZ1C%2B3X0XBT4%3D'

def main():
    # req = '/media/v1.0/community-36/searchAllMedia'
    # req = '/post/v1.0/member-67b4c6fb2220ac6705aa97046f3503a1/posts?fieldSet=postsV1&filterType=MOMENT?after=1696674454222%2C26564616'
    # req = '/post/v1.0/member-67b4c6fb2220ac6705aa97046f3503a1/posts?fieldSet=postsV1&filterType=MOMENT?after=1696674454222%2C26564616'
    # write_single(req, 'raw/test', False)

    # write_all_requests(req, req, 'raw/post-data/searchAllMedia', True)
    # write_all_post_media()

    'https://global.apis.naver.com/weverse/wevweb/post/v1.0/member-5fb309bc7489a576484431ba8338807e/posts?after=1698763879873%2C27023472&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postV1&filterType=MOMENT_VIEWER&language=en&limit=1&os=WEB&platform=WEB&wpf=pc&wmsgpad=1735178426948&wmd=xVsr5ooMlAolx3fADGZQguc2CzY%3D'

    for m, id in members.items():
        req = f'/post/v1.0/member-{id}/posts?fieldSet=postsV1&filterType=MOMENT_VIEWER&limit=1'
        write_all_requests(req, req, f'raw/post-data/moments/{m}', True)


main()

# 'https://global.apis.naver.com/weverse/wevweb/post/v1.0/member-67b4c6fb2220ac6705aa97046f3503a1/posts?after=1699369636979%2C27138103&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=postV1&filterType=MOMENT_VIEWER&language=en&limit=1&os=WEB&platform=WEB&wpf=pc&wmsgpad=1735178210447&wmd=Y1OTRioyq7vF2%2FSYTL09CAraDDM%3D'
# 'https://global.apis.naver.com/weverse/wevweb/member/v1.1/community-36/artistMembers?appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&fieldSet=artistMembersV1&filterType=MOMENT&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1735178123317&wmd=KHioIqTMvGRFPAxb3jUuMb0WdaE%3D'