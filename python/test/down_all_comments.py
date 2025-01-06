import json
import os.path

import yt_dlp
import time

from yt_dlp.extractor.weverse import WeverseIE

params = {
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

    # ids = set()

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

        data = run_extr(extr, mod_req, out_data)

        prev = get_prev_page(data)
        after = get_next_page(data)

        if use_after and not after:
            break
        elif not use_after and not prev:
            break

        print('waiting...')
        time.sleep(2)

    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        # Write the array as JSON
        json.dump(out_data, file)

def write_all_comments():
    with open(f'raw/post-data/all_live_posts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            postId = data['postId']
            print('downloading', postId)
            req = f'/comment/v1.0/post-{postId}/comments?fieldSet=postCommentsV1'
            write_all_requests(req, req, f'raw/post-data/allComments/{postId}', True, True)
            time.sleep(5)

write_all_comments()
