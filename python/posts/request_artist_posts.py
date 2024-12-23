import datetime
import json

import yt_dlp
import time

from yt_dlp.extractor.weverse import WeverseIE
from yt_dlp.utils import ExtractorError

params = {
    # 'verbose': True,
    'quiet': True,
    'cookiesfrombrowser': ('firefox',),
}

passwords = {
    '0-119852324': '',
    '0-59825': '1154',
    '0-58709': '0107',
    '4-120566436': '0124',
    '1-7529': '0601',
    '0-54144': '0122',
    '1-119817916': '0124',
    '3-120472027': '7777',
    '3-120082099': '1123',
    '4-119844206': '0605',
    '4-120717949': '0320',
    '1-119739859': '4444',
    '2-120747570': '0320',
    '0-119985805': '1111',
    '0-3962': '1004',
    '0-4013': '360',
    '0-104750': 'BABABABAB',
}

member = 'db56036fc59a94a9ef617261c90c783f'

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


def main():
    # thing = WeverseIE()
    # thing.set_downloader(ydl)
    # # thing.initialize()
    # thing._initialize_pre_login()
    # thing._real_initialize()
    # thing._ready = True

    extr = make_extractor()

    # req = '/comment/v1.0/member-6aa813460d109e841afc9ac410f25226/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4'

    req = '/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments?fieldSet=memberCommentsV1&sortType=LATEST'

    out_data = []

    count = 0
    next_page = None
    while True:
        req = '/post/v1.0/community-36/artistTabPosts?fieldSet=postsV1'
        next_page = run_extr(extr, req, next_page, out_data)
        if not next_page:
            break

        time.sleep(.5)

        # count += 1
        # if count > 5:
        #     break

    with open('all_artist_posts.json', 'w') as file:
        # Write the array as JSON
        json.dump(out_data, file)

    '"after": "1726690555959,31862"'

    'https://global.apis.naver.com/weverse/wevweb/post/v1.0/community-36/artistTabPosts?fieldSet=postsV1&limit=20&pagingType=CURSOR&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734592335582&wmd=9e%2BHhGb92uPG%2Fl12Ksp6unfMngo%3D'
    'https://global.apis.naver.com/weverse/wevweb/post/v1.0/community-36/artistTabPosts?after=1726690555959%2C31862&fieldSet=postsV1&limit=20&pagingType=CURSOR&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734592577969&wmd=mbuzOGkhc5TXbJvW29EJtLMMuxA%3D'




def run_extr(extr, req, next_page, out_data):
    # 'post/v1.0/community-36/artistTabPosts?fieldSet=postsV1'
    # req = '/post/v1.0/community-36/artistTabPosts&fieldSet=postsV1'
    if next_page:
        req += f'&after={next_page}'
    print(req)

    json_data = extr._call_api(req, '')
    # print(json_data)

    next_page = get_next_page(json_data)

    post_data = json_data['data']
    out_data += post_data

    print(f'Found {len(post_data)} Next: {next_page} Data: {len(out_data)}')

    return next_page


def read_post(extr, post_id):
    # 'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-4-186439916?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734594911973&wmd=kcV1b4j%2FiIy4M8IqQKfBz7J14DI%3D'

    'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-0-119852324?fieldSet=postV1&fields=recommendProductSlot&lockPassword=&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734599893718&wmd=fd1DgvDuEQIBFjacLdz%2F5K3KQas%3D'

    req = f'/post/v1.0/post-{post_id}?fieldSet=postV1'

    if post_id in passwords:
        password = passwords.get(post_id)
        req += f'&lockPassword={password}'

    'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-4-120566436?fieldSet=postV1&fields=recommendProductSlot&lockPassword=0124&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734597157813&wmd=qn8E8XdGlFTYm2KLG06LsSx4EO8%3D'

    try:
        json_data = extr._call_api(req, '')
        # print(json_data)
        return json_data
    except ExtractorError as e:
        print(f'FAILED TO READ {post_id} {req}')
        return None

    return None


def download_real_posts():
    all_posts = []
    extr = make_extractor()

    with open('all_artist_posts.json', 'r', encoding='utf-8') as file:
        # print('Loading json')
        json_data = json.load(file)

        i = 0
        for post in json_data:
            post_id = post['postId']
            print(post_id)
            all_posts.append(read_post(extr, post_id))
            time.sleep(.5)

    with open('real_artist_posts.json', 'w') as file:
        # Write the array as JSON
        json.dump(all_posts, file)

def get_datetime(timestamp):
    time = int(timestamp) / 1000
    date = datetime.datetime.fromtimestamp(time)
    return date.strftime("%b %d %Y, %H:%M")

def print_locked():
    with open('all_artist_posts.json', 'r', encoding='utf-8') as file:
        # print('Loading json')
        json_data = json.load(file)


    data = []
    for post in json_data:
        if post['locked']:
            # print(post['author']['profileName'], get_datetime(int(post['publishedAt'])), post['postId'])
            data.append([post['author']['profileName'], get_datetime(int(post['publishedAt'])), post['postId']])
            # print()
            # data.append(post)
    # print(json.dumps(data))

    data = sorted(data, key=lambda d: d[0])
    for d in data:
        print(d)

def download_comments():
    extr = make_extractor()

    # req = '/comment/v1.0/member-6aa813460d109e841afc9ac410f25226/comments?fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4'

    out_data = []

    members = [
        '5fb309bc7489a576484431ba8338807e', # jh
        '67b4c6fb2220ac6705aa97046f3503a1', # hy
        '65eff6ab044ae8dea6816794f11a6fc1', # cy
        '6599dbbcaa26237c2ab0f3becb421b45', # jw
        '01435f74a49ba8a519705ad242348232', # js
        '326c0d1e7045798aa3964e2028c34628', # sr
        '56bdfafb606d9ce1b4ecdd572595e242', # sy
        '5477d46be848bd40252f9d13ef62cb4d', # ng
        'db56036fc59a94a9ef617261c90c783f' # gr
    ]

    for member in members:
        req = f'/comment/v1.0/member-{member}/comments?fieldSet=memberCommentsV1&sortType=LATEST'

        count = 0

        next_page = None
        while True:
            next_page = run_extr(extr, req, next_page, out_data)
            if not next_page:
                break

            time.sleep(.5)

            # count += 1
            # if count > 3:
            #     break

    with open('all_comments.json', 'w') as file:
        # Write the array as JSON
        json.dump(out_data, file)

def download_comment_posts():
    all_posts = []
    failed_posts = []
    extr = make_extractor()

    with open('all_comments.json', 'r', encoding='utf-8') as file:
        # print('Loading json')
        json_data = json.load(file)

        uniq_posts = set()

        # i = 0
        for post in json_data:
            post_id = post['root']['data']['postId']
            # post_id = post['postId']
            uniq_posts.add(post_id)
            # print(post_id)

            # time.sleep(.5)
        print(f'FOUND {len(uniq_posts)} posts from {len(json_data)} comments')

    print(uniq_posts)

    for i, post_id in enumerate(uniq_posts):
        print(f'{i}/{len(uniq_posts)}')
        post_data = read_post(extr, post_id)
        if post_data is None:
            failed_posts.append(post_id)
        else:
            all_posts.append(post_data)
        time.sleep(0.5)
        # print(p)

    with open('all_comment_posts.json', 'w') as file:
        # Write the array as JSON
        json.dump(all_posts, file)

    with open('failed_posts.json', 'w') as file:
        # Write the array as JSON
        json.dump(failed_posts, file)

def print_all_posts():
    all_posts = []
    failed_posts = []
    extr = make_extractor()

    full_data = []

    with open('all_artist_posts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        full_data += json_data
        print('Artist posts', len(json_data))

    with open('all_comment_posts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        full_data += json_data
        print('Comment posts', len(json_data))

    uniq_posts = set()
    for data in full_data:
        if summary := data.get('summary'):
            if int(summary['videoCount']) > 0:
                uniq_posts.add(data['postId'])

    print('Uniq', len(uniq_posts))

    print(list(uniq_posts))

    # with open('all_comment_posts.json', 'w') as file:
    #     # Write the array as JSON
    #     json.dump(all_posts, file)
    #
    # with open('failed_posts.json', 'w') as file:
    #     # Write the array as JSON
    #     json.dump(failed_posts, file)

def download_missing_posts():
    all_posts = []
    extr = make_extractor()

    missing = [
        '3-120720842',
        '3-120937858',
        '2-120090083',
        '3-121097435',
        '4-121317716',
        '4-121099674',
        '4-121098139',
        '1-120332626',
        '1-120106430',
        '1-120160952',
    ]



    for post_id in missing:
        print(post_id)
        all_posts.append(read_post(extr, post_id))
        time.sleep(.5)

    with open('missing.json', 'w') as file:
        # Write the array as JSON
        json.dump(all_posts, file)

download_missing_posts()
# print_all_posts()
# download_comment_posts()
# download_comments()
# print_locked()
# download_real_posts()
# main()


# https://global.apis.naver.com/weverse/wevweb/post/v1.0/community-36/artistTabPosts?fieldSet=postsV1&limit=20&pagingType=CURSOR&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734592145141&wmd=y3YfiX4ZKNmoQWvel42uacVdFSQ%3D

# https://global.apis.naver.com/weverse/wevweb/post/v1.0/community-36/artistTabPosts?after=1726690555959%2C31862&fieldSet=postsV1&limit=20&pagingType=CURSOR&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734592155867&wmd=TDoIYrk7eQ%2BJjqZuKH1%2BiXk1TLU%3D