import datetime
import json
import datetime
import os
import random
import re
import shutil
import textwrap
from zoneinfo import ZoneInfo

from python import wv_helper
from python.wv_helper import Comment, Post, Author

base_dir = 'docs/wv-posts'

skip_your_msgs = True
pfp_data = {}

empty_profile_url = 'https://cdn-v2pstatic.weverse.io/wev_web_fe/p/2_31_0/public/static/media/icon_empty_profile.b0996808ea97350978a4.png'

POSTTYPE_NORMAL = 'NORMAL'
POSTTYPE_MOMENT = 'MOMENT'
POSTTYPE_MOMENT_W1 = 'MOMENT_W1'
POSTTYPE_OFFICIAL = 'OFFICIAL' # https://weverse.io/fromis9/fanpost/1-18493615?hl=ko
POSTTYPE_YOUTUBE = 'YOUTUBE' # https://weverse.io/fromis9/media/1-112423954?hl=ko
POSTTYPE_VIDEO = 'VIDEO' # https://weverse.io/fromis9/live/1-121237638?hl=ko
POSTTYPE_IMAGE = 'IMAGE' # https://weverse.io/fromis9/media/3-108112017?hl=ko
POST_TYPES = {POSTTYPE_NORMAL, POSTTYPE_MOMENT, POSTTYPE_MOMENT_W1, POSTTYPE_OFFICIAL, POSTTYPE_YOUTUBE, POSTTYPE_VIDEO, POSTTYPE_IMAGE}
PARENT_TYPE_POST = 'POST'
PARENT_TYPE_COMMENT = 'COMMENT'

post_database = dict()

def get_datetime(timestamp):
    time = int(timestamp) / 1000
    return datetime.datetime.fromtimestamp(time, tz=ZoneInfo("Asia/Seoul"))

def make_image_md(url, caption='', zoom_click=True, figure=True):
    if caption:
        caption = f'<figcaption>{caption}</figcaption>'

    zoom_md = 'onclick="openFullscreen(this)' if zoom_click else ''

    if figure:
        return textwrap.dedent(f"""\
                            <figure markdown="1">
                            ![]({url}){{ loading=lazy {zoom_md}"}}{caption}
                            </figure>""")
    else:
        return textwrap.dedent(f'![]({url}){{ loading=lazy {zoom_md}"}}{caption}')

def make_iframe_md(embed_url, display_url):
    return textwrap.dedent(f"""\
    <figure class="snippet" markdown="1">
    <iframe src="{embed_url}"></iframe>
    <figcaption><a href="{display_url}">{display_url}</a></figcaption>
    </figure>""")

def date_to_str(date, sorted=False):
    if sorted:
        return date.strftime("%Y-%m-%d %H-%M")
    else:
        return date.strftime("%b %d %Y, %H:%M")

def replace_links(text):
    pattern = r"(https?://[^\s]+)"
    replacement = r'<a href="\1">\1</a>'

    result = re.sub(pattern, replacement, text)
    return result

def process_comment(comment: Comment):
    name = comment.author.profileName

    if comment.author.hasOfficialMark:
        name_md =f'<span class="artist">{name}</span>'
    else:
        name_md = name

    # pfp = comment.thumb if comment.thumb != '' else empty_profile_url
    pfp = comment.author.profileImageUrl + '?type=s72'

    if pfp is None:
        pfp = empty_profile_url

    artist_md = f'''<div class="comment" markdown="1">
<div class='id-container' markdown="1">
![]({pfp}){{ loading=lazy }}
**{name_md}** <small>{date_to_str(comment.createdAt)}</small><br>
</div>
<div class='comment-body' markdown="1">
{comment.body}
</div>
</div>'''
    return artist_md


def parse_comments(comments):
    items = []

    for comment in comments:
        items.append(process_comment(comment))

        for reply in comment.replies:
            reply_md = f'''<div class="reply" markdown="1">
{process_comment(reply)}
</div>'''
            items.append(reply_md)

#     for comment in comments:
#         md = f"""
# {comment.author.profileName}: {comment.body}
# """
#         items.append(md)

    return '\n'.join(items)



def make_post(post):
    post_id = post.postId

    name = post.author.profileName

    if post.author.hasOfficialMark:
        name_md = f'<span class="artist">{name}</span>'
    else:
        name_md = name

    # pfp = comment.thumb if comment.thumb != '' else empty_profile_url
    pfp = post.author.profileImageUrl


    categories_md = ''
    post_members = post.get_authors()

    if len(post_members) == 0:
        breakpoint()
    categories = post.get_categories()
    if len(categories):
        categories_list = '\n'.join([f'  - {m}' for m in categories])
        categories_md = f'\ncategories:\n{categories_list}'

    member_authors = '\n'.join([f'  - {m.memberId}' for m in post_members])

    head = ''
    if post.postType == POSTTYPE_VIDEO:
        url = post.extension['video']['thumb']
        caption = f'<a href="{post.shareUrl}">{post.shareUrl}</a>'

        head = textwrap.dedent(f"""\
<a href="{post.shareUrl}">
{make_image_md(url, caption, False)}
</a>""")

    author_md = f'''
<div class='id-container' markdown="1">
![]({pfp}){{ pfp loading=lazy }}
<div markdown="1">
**{name_md}** <small>{date_to_str(post.publishedAt)}</small><br>
</div>
</div>'''

    ## {post_id}
    ## {author_md}

    out = f"""---
slug: {post.postId}
date: {post.publishedAt}
authors:
{member_authors}{categories_md}
tags:
  - {post.get_tag_type()}
---

# {post_id}

<div class="post-container" markdown="1">
<div class="content-container md-sidebar__scrollwrap" markdown="1">
{head}
{post.process_body()}
{post.process_extensions()}
</div>
</div>

<div style="text-align: right;" markdown="1">
<a href="{post.shareUrl}" style="text-align: right;">:material-share:{{.big-emoji}}</a>
</div>
---
"""

    if len(post.comments):
        comments_md = f'''
<div class="comments-container md-sidebar__scrollwrap" markdown="1">
{parse_comments(post.comments)}
</div>
---
'''
        out += comments_md


    return out

def clear_posts():
    dir = f'{base_dir}/posts/'
    shutil.rmtree(dir)
    os.makedirs(dir)

def make_markdown(posts):
    for p in posts:
        # date_title = date_to_str(p.publishedAt, True)
        out_file = f"""{make_post(p)}"""
        file_path = f'{base_dir}/posts/{p.postId}.md'
        with open(file_path, mode='w', encoding='utf-8') as txt:
            txt.writelines(out_file)
            # print(len(out_file), len(out_file.split('\n')))

def gather_comments(data):
    all_comments = dict()

    for comment_data in data:
        root = comment_data['root']['data']
        post_id = root['postId']

        comment =   Comment(comment_data)

        if comment.commentId in all_comments:
            # print(comment_data)
            continue
            # breakpoint()

        all_comments[comment.commentId] = comment

        main_comment = comment

        if comment_data['parent']['type'] == 'COMMENT':
            parent_id = comment_data['parent']['data']['commentId']
            if parent_id in all_comments:
                parent_comment = all_comments[parent_id]
            else:
                parent_comment = Comment(comment_data['parent']['data'])
                all_comments[parent_comment.commentId] = parent_comment

            parent_comment.replies.append(comment)
            main_comment = parent_comment

        if post_id in post_database:
            post_database[post_id].comments.add(main_comment)
        else:
            print('FAILED TO FIND', post_id)

    for k, post in post_database.items():
        post.comments = sorted(post.comments, key=lambda c: c.createdAt)

        for c in post.comments:
            c.replies = sorted(c.replies, key=lambda c: c.createdAt)


def gather_posts(data):
    posts = dict()

    for post_data in data:
        if post_data.get('errorCode'):
            continue

        post_id = post_data['postId']

        if post_id in posts:
            continue

        posts[post_id] = Post(post_data)

    print(f'Num posts: {len(posts)}')

    return posts

def filter_posts(posts):
    out_posts = []
    random.shuffle(posts)
    for p in posts:
        # if not p.has_attachment('video'):
        #     continue
        # if not p.author.memberId == wv_helper.members_ids['jisun']:
        #     continue

        # found = False
        # for id, _ in p.attachment['video'].items():
        #     if id in wv_helper.video_redirects:
        #         print(id)
        #         found = True
        # if not found:
        #     continue

        types = {
            # POSTTYPE_OFFICIAL,
            # POSTTYPE_YOUTUBE,
            # POSTTYPE_VIDEO,
            # POSTTYPE_IMAGE
            # POSTTYPE_MOMENT
        }

        # TODO: INSERT POSTTYPE_YOUTUBE
        if len(types) == 0 or p.postType in types:
            out_posts.append(p)
            print(p.json_data)

        if len(out_posts) > 50:
            break
    print(f'Filtered {len(out_posts)} media')
    return out_posts

def get_comment_data():
    with open('raw/post-data/all_comments.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data

def verify_posts(posts):
    for p in posts:
        if p.has_attachment('video'):
            for k, v in p.attachment['video'].items():
                media_path = f'/assets/videos/weverse_{k}.mp4'
                if not os.path.exists(media_path):
                    print('Missing video ', k, p.shareUrl)

def main():
    members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    # test = False

    all_comment_data = []
    clear_posts()

    files = ['raw/post-data/real_artist_posts.json', 'raw/post-data/all_comment_posts.json', 'raw/post-data/missing.json']
    for member in members:
        files.append(f'raw/post-data/moments/{member.lower()}.json')

    all_post_data = wv_helper.get_post_data(files)

    global post_database
    post_database = gather_posts(all_post_data)

    gather_comments(get_comment_data())

    for k, post in post_database.items():
        # print(k, post)
        for comment in post.comments:
            # print('\t', comment.commentId)

            if len(post.comments) != len(set(post.comments)):
                breakpoint()

    sorted_posts = sorted(post_database.values(), key=lambda p: p.publishedAt)

    wv_helper.make_authors(sorted_posts)

    # sorted_posts = filter_posts(sorted_posts)

    # verify_posts(sorted_posts)

    # make_markdown(sorted_posts)


if __name__ == '__main__':
    main()
