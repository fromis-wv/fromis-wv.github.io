import datetime
import json
import os
import time

import requests
from requests.exceptions import ChunkedEncodingError


def get_data_from_files(files):
    post_dict = dict()

    out_data = []
    total = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            print(f, len(json_data))
            total += len(json_data)

            for data in json_data:
                if data is None:
                    print(f, ' has invalid data!')
                    breakpoint()
                post_id = data['postId']
                if post_id in post_dict:
                    continue

                post_dict[post_id] = data
            # out_data += json_data
    print('UNIQ POSTS ', len(post_dict), 'TOTAL', total)
    return post_dict.values()


def verify_artist_posts():
    post_ids = set()
    with open('all_artist_posts.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        for data in json_data:
            post_ids.add(data['postId'])

    print(len(post_ids))

    all_data = get_data_from_files(['real_artist_posts.json', 'missing.json'])
    for data in all_data:
        if data:
            if postId := data.get('postId'):
                if postId not in post_ids:
                    print('FAILED TO FIND ', postId)
                    breakpoint()
                post_ids.remove(postId)

    for p in post_ids:
        print(p)


def download_img(image_url, file_path):
    while True:  # Infinite loop to keep trying
        try:
            # Send a GET request to the URL
            print(f"Downloading {file_path} {image_url}")
            response = requests.get(image_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Open a file in binary write mode to save the image
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    print("Image downloaded successfully!")
                return  # Exit the loop if download is successful
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                time.sleep(1)  # Optional: Wait before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Optional: Wait before retrying

    # # URL of the image
    # # image_url = 'https://phinf.wevpstatic.net/MjAyNDExMjlfMjIy/MDAxNzMyODgyMTAzNzU4.vn1UPQOkZprmnRjCrMdToTNNVQ6czzo3nQLKlSbD6-gg.D6x_Jyv8jDlFapLq0Z8tkXk5IA9Fb-Z_Ou6iHZX5lEMg.JPEG/image.jpg'
    #
    # # Send a GET request to the URL
    # response = requests.get(image_url)
    #
    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Open a file in binary write mode to save the image
    #     with open(file_path, "wb") as file:
    #         file.write(response.content)
    #     # print("Image downloaded successfully!")
    # else:
    #     print(f"Failed to download image. Status code: {response.status_code}")

def check_missing_videos(videos):
    all_videos = set()
    missing = []
    posts = dict()

    for post_id, elem in videos:
        for k, video in elem.items():
            # print(video)
            video_id = video['videoId']
            all_videos.add(video_id)
            path = f'raw/post-media/videos/weverse_{video_id}.mp4'
            if not os.path.exists(path):
                missing.append(video_id)
                posts.setdefault(post_id, [])
                posts[post_id].append(video_id)
                print(path)

    # 'C:\Documents\Projects\fromis-wv.github.io\raw\post-media'
    # 'raw/post-media/videos/weverse_2-871101.mp4'
    print(len(videos), "missing ", len(missing))
    for k, ps in posts.items():
        print(k)
        for p in ps:
            print('\t', p)

def get_photo_name(photo):
    photo_id = photo['photoId']
    url = photo['url']
    ext = url.rsplit('.')[-1]

    file_name = f'weverse_{photo_id}.{ext}'
    # path = f'raw/post-media/weverse_{file_name}'
    return file_name

def check_missing_photos(photos):
    all_videos = set()
    missing = []
    posts = dict()

    for post_id, elem in photos:
        for k, photo in elem.items():
            photo_id = photo['photoId']
            # print(id)
            # print(photo)
            # url = photo['url']
            # ext = url.rsplit('.')[-1]
            #
            # file_name = f'weverse_{photo_id}.{ext}'
            # path = f'raw/post-media/weverse_{file_name}'
            path = f'raw/post-media/{get_photo_name(photo)}'
            if not os.path.exists(path):
                print(f'missing {path}')
                missing.append(photo)

    print(f'missing {len(missing)}')

    for i, photo in enumerate(missing):
        print(i, '/', len(missing))
        down_path = f'raw/post-media/{get_photo_name(photo)}'

        download_img(photo['url'], down_path)

        # waiting = True
        # while waiting:
        #     # try:
        #         waiting = False
        #     # except ChunkedEncodingError as e:
        #     #     print(e)
        #     #     time.sleep(0.5)

        time.sleep(2)

    # 'C:\Documents\Projects\fromis-wv.github.io\raw\post-media'
    # 'raw/post-media/videos/weverse_2-871101.mp4'
    # print(len(photos), "missing ", len(missing))
    # for k, ps in posts.items():
    #     print(k)
    #     for p in ps:
    #         print('\t', p)

def process_attachments(attachments):
    # for snippet in attachments['snippet']:
    #     print(snippet)
    check_missing_videos(attachments['video'])
    check_missing_photos(attachments['photo'])

def print_all_posts():
    files = ['raw/post-data/real_artist_posts.json', 'raw/post-data/all_comment_posts.json', 'raw/post-data/missing.json']
    full_data = get_data_from_files(files)

    attachment_types = set()

    expected_types = {'photo', 'snippet', 'video'}

    attachments = dict()

    for data in full_data:
        if attachment := data.get('attachment'):
            for k, v in attachment.items():
                if k not in expected_types:
                    print("WHAT IS THIS ", k)
                    breakpoint()

                attachments.setdefault(k, [])
                attachments[k].append((data['postId'], v))
                # print(k, v)

    process_attachments(attachments)

        # if summary := data.get('summary'):
        #     for k, v in summary.items():
        #
        #         # if len(v):
        #         #     post_media.setdefault(k, set())
        #         #     post_media[k].add(v)
        #
        #         # if k != 'videoCount' and k != 'photoCount':
        #         if k == 'snippet':
        #             # if len(v):
        #             print(k, v)
        #
        #     # if int(summary['videoCount']) > 0:
        #     #     uniq_posts.add(data['postId'])

    # for k, v in post_media:
    #     print(f'{k}: {len(v)}')

    print('Attachments: ', list(attachments.keys()))

print_all_posts()
# print_all_posts()

