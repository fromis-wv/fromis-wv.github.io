import csv
import json
import shutil
from datetime import datetime
import os
import chardet

INDEX_ID = 'index'
POST_ID = 'post'
DATE_ID = 'date'
NAME_ID = 'name'
TEXT_ID = 'text'
REPLY_ID = 'reply'

skip_your_msgs = True
pfp_data = {}

empty_profile_url = 'https://cdn-v2pstatic.weverse.io/wev_web_fe/p/2_31_0/public/static/media/icon_empty_profile.b0996808ea97350978a4.png'

class Comment:
    def __init__(self):
        self.text = ''
        self.name = ''
        self.date = ''
        self.alias = ''
        self.id = ''
        self.sub_comments = []

    def __lt__(self, other):
        return self.date < other.date


class Post:
    def __init__(self):
        self.comments = []
        self.data = []
        self.member = ''
        self.date = ''
        self.likes = ''
        self.thumb = ''

    def __lt__(self, other):
        return self.date < other.date

def get_video_id(data):
    return f'weverse_{data['id']}'

def get_pfp(name):
    return pfp_data[name] if name in pfp_data else empty_profile_url

def process_content(datas):
    texts = []
    for data in datas:
        type = data['type']

        if type == 'IMAGE':
            id = data['type']
            md = f"""
<figure markdown="1">
![]({data['link']}){{ loading=lazy onclick="openFullscreen(this)" }}
</figure>"""

            texts.append(md)
        elif type == 'TEXT':
            md = f"""<div class="text-content-container" markdown="1">
{data['text'].replace('\n', '<br>')}
</div>"""
            texts.append(md)
        elif type == 'VIDEO':
            thumb_name = f'{get_video_id(data)}-thumb.jpg'
            media_name = f'{get_video_id(data)}.mp4'
            md = f"""
<figure markdown="1">
<video controls="controls" preload="none" poster="{media_path}/{thumb_name}">
<source src="{media_path}/{media_name}#t=1" type="video/mp4">
Your browser does not support the video tag.
</video>
</figure>
"""
            texts.append(md)

    return ''.join(texts)

def process_comment(comment):
    artist_replies = ['GROUPED_ARTIST_COMMENT', 'GROUPED_ARTIST_REPLY_COMMENT', 'ORIGINAL_COMMENT_ARTIST', 'GROUPED_ARTIST_COMMENT_LATEST', 'GROUPED_ARTIST_REPLY_COMMENT_LATEST']

    if comment.alias in artist_replies:
        name_md =f'<span class="artist">{comment.name}</span>'
    else:
        name_md = comment.name

    # pfp = comment.thumb if comment.thumb != '' else empty_profile_url
    pfp = get_pfp(comment.name)

    md = f'''<div class="comment" markdown="1">
<div class='id-container' markdown="1">
![]({pfp}){{ pfp loading=lazy }}
<div markdown="1">
**{name_md}** <small>{date_to_str(comment.date)}</small><br>
{comment.text}
</div>
</div>
</div>'''
    return md

def process_comments(comments):
    md_list = []
    for comment in comments:
        print('comment ', comment.date)
        comment_md = process_comment(comment)
        md_list.append(comment_md)

        for sub_comment in comment.sub_comments:
            print('sub ', sub_comment.date)
            sub_md = process_comment(sub_comment)
            sub_md = f'''<div class="reply" markdown="1">
{sub_md}
</div>
'''
            md_list.append(sub_md)

    return ''.join(md_list)

def process_post(post):
    content_md = process_content(post.data)
    comments_md = process_comments(post.comments)

    optional_password = f'**PASSWORD:** {post.password}<br>' if post.password != '' else '';

    out_file = f'''
# {date_to_str(post.date, True)}
    
{content_md}

**{post.member}** <br>{optional_password}
❤️{post.likes}

---
<div class="comments-container md-sidebar__scrollwrap" markdown="1">
{comments_md}
</div>
'''

    # Write to file!
    if not os.path.exists(f'docs/{member_name.lower()}/posts'):
        os.makedirs(f'docs/{member_name.lower()}/posts', exist_ok=True)

    name = f'docs/{member_name.lower()}/posts/{date_to_str(post.date, True)}.md'
    # print('Writing post ', name)
    with open(name, mode='w', encoding='utf-8') as txt:
        txt.writelines(out_file)

def date_to_str(date, sorted=False):
    if sorted:
        return date.strftime("%Y-%m-%d %H-%M")
    else:
        return date.strftime("%b %d %Y, %H:%M")

def get_date_time(date_string):
    try:
        out = datetime.strptime(date_string, '%b %d, %H:%M')
        out = out.replace(year=datetime.now().year)
        return out
    except ValueError:
        return datetime.strptime(date_string, '%b %d, %Y, %H:%M')

def make_comment(json_comment):
    comment = Comment()
    comment.text = json_comment['text'].replace('\n', '<br>')
    comment.name = json_comment['name']
    comment.date = get_date_time(json_comment['date'])
    comment.alias = json_comment['alias']
    comment.id = json_comment['id']
    comment.thumb = json_comment['thumb']
    comment.sub_comments = []
    for sub_comment in json_comment['sub_comments']:
        comment.sub_comments.append(make_comment(sub_comment))
    return comment

def make_post(json_post):
    post = Post()
    post.data = json_post['data']
    post.member = json_post['member']
    post.date = get_date_time(json_post['date'])
    post.likes = json_post['likes']
    post.password = '' if 'password' not in json_post else json_post['password']
    post.thumb = json_post['thumb']

    post.comments = []
    for json_comment in json_post['comments']:
        post.comments.append(make_comment(json_comment))

    post.comments.sort()

    return post

if __name__ == '__main__':
    # members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    members = ['Jiwon', 'Chaeyoung']

    with open("raw/misc/pfps.txt", "r", encoding='utf-8') as pfp_file:
        pfp_data = eval(pfp_file.read())

    for member_name in members:
        media_path = f'/media/{member_name.lower()}/posts'
        # media_search = f'docs/media/{member_name.lower()}'
        # relative_media_path = f'docs/media/{member_name.lower()}'

        file_path = f'raw/{member_name}/posts/data.json'
        enc = chardet.detect(open(file_path, 'rb').read())['encoding']

        def sort_date(elem):
            return elem['date']


        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_posts = data['posts']

            new_posts = []

            for p in all_posts:
                new_posts.append(make_post(p))

            new_posts.sort()

            new_posts = sorted(new_posts)

            for p in new_posts:
                process_post(p)
            print('posts ', len(all_posts))
