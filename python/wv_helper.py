import json
import datetime
import os
import random
import time
import re
import shutil
import textwrap
from tabnanny import check
from zoneinfo import ZoneInfo

import requests
import tzdata
from textwrap import dedent
import chardet

base_dir = 'docs/wv-posts'

skip_your_msgs = True
pfp_data = {}

empty_profile_url = 'https://cdn-v2pstatic.weverse.io/wev_web_fe/p/2_31_0/public/static/media/icon_empty_profile.b0996808ea97350978a4.png'

POSTTYPE_NORMAL = 'NORMAL'
POSTTYPE_MOMENT = 'MOMENT'
POSTTYPE_MOMENT_W1 = 'MOMENT_W1'
POSTTYPE_OFFICIAL = 'OFFICIAL'  # https://weverse.io/fromis9/fanpost/1-18493615?hl=ko
POSTTYPE_YOUTUBE = 'YOUTUBE'  # https://weverse.io/fromis9/media/1-112423954?hl=ko
POSTTYPE_VIDEO = 'VIDEO'  # https://weverse.io/fromis9/live/1-121237638?hl=ko
POSTTYPE_IMAGE = 'IMAGE'  # https://weverse.io/fromis9/media/3-108112017?hl=ko
POST_TYPES = {POSTTYPE_NORMAL, POSTTYPE_MOMENT, POSTTYPE_MOMENT_W1, POSTTYPE_OFFICIAL, POSTTYPE_YOUTUBE, POSTTYPE_VIDEO, POSTTYPE_IMAGE}
PARENT_TYPE_POST = 'POST'
PARENT_TYPE_COMMENT = 'COMMENT'

video_redirects = {
    '4-1033524': 'u9sQbsLseuM',
    '2-22': 'zqYAPFGKddU',
    '3-268692': 'o__BToVL030',
    '3-316987': '-Znw-iK_Dyk',
    '2-227577': 'xYy49ad4-GY',
    '2-290970': 'xYy49ad4-GY'
}

members_ids = {
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

def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


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
                            ![]({url+'?type=e1920'}){{ loading=lazy {zoom_md}"}}{caption}
                            </figure>""")
    else:
        return textwrap.dedent(f'![]({url+'?type=e1920'}){{ loading=lazy {zoom_md}"}}{caption}')


def make_iframe_md(embed_url, display_url=None):
    if display_url is None:
        return textwrap.dedent(f"""\
                <figure class="snippet" markdown="1">
                <iframe src="{embed_url}" frameborder="0" allow="fullscreen"></iframe>
                </figure>""")
    else:
        return textwrap.dedent(f"""\
                <figure class="snippet" markdown="1">
                <iframe src="{embed_url}" frameborder="0" allow="fullscreen"></iframe>
                <figcaption><a href="{display_url}">{display_url}</a></figcaption>
                </figure>""")


class Author:
    def __init__(self, data):
        self.memberId = data.get('memberId')
        self.communityId = data.get('communityId')
        self.joined = data.get('joined')
        self.profileName = data.get('profileName')
        self.profileImageUrl = data.get('profileImageUrl')
        if not self.profileImageUrl:
            self.profileImageUrl = empty_profile_url
        self.memberJoinStatus = data.get('memberJoinStatus')
        self.profileType = data.get('profileType')
        self.hasMembership = data.get('hasMembership')
        self.hasOfficialMark = bool(data.get('hasOfficialMark'))
        self.profileSpaceStatus = data.get('profileSpaceStatus')
        self.myProfile = data.get('myProfile')
        self.badges = data.get('badges')

    def __repr__(self):
        properties = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({properties})"

    def __eq__(self, other):
        return self.memberId == other.memberId

    def __hash__(self):
        return hash(self.memberId)


class Post:
    def __init__(self, data):

        # self.type = type
        # if self.type != 'POST': # and self.type != PARENT_TYPE_COMMENT:
        #     print(f'UNKNOWN ROOT TYPE {self.type}')
        #     breakpoint()

        self.publishedAt = get_datetime(data.get('publishedAt'))
        self.hideFromArtist = data.get('hideFromArtist')
        self.plainBody = data.get('plainBody')
        self.commentCount = data.get('commentCount')
        self.viewerEmotionId = data.get('viewerEmotionId')
        self.extension = data.get('extension')
        self.errorCode = data.get('errorCode')
        self.attachment = data.get('attachment') if data.get('attachment') else dict()
        self.sectionType = data.get('sectionType')
        self.locked = data.get('locked')
        self.emotionCount = data.get('emotionCount')
        self.exposeStatus = data.get('exposeStatus')
        self.message = data.get('message')
        self.maxCommentCount = data.get('maxCommentCount')
        self.shareUrl = data.get('shareUrl').removesuffix('?hl=ko')
        self.postId = data.get('postId')
        self.community = data.get('community')
        self.author = Author(data.get('author'))
        self.artistReactions = data.get('artistReactions')
        self.maxCommentCountReached = data.get('maxCommentCountReached')
        self.membershipOnly = data.get('membershipOnly')
        self.tags = data.get('tags')
        self.body = data.get('body')

        self.availableActions = data.get('availableActions')
        self.bookmarked = data.get('bookmarked')
        self.hasProduct = data.get('hasProduct')
        self.postType = data.get('postType')

        if self.postType not in POST_TYPES:
            print(f'UNKNOWN POST TYPE {self.postType}')
            breakpoint()

        if self.body is None:
            if self.postType == 'MOMENT':
                self.body = self.extension['moment'].get('body')
            elif self.postType == 'MOMENT_W1':
                self.body = self.extension['momentW1'].get('body')
            else:
                breakpoint()

        if self.body is None:
            self.body = ''

        self.body = self.body.replace('#', '\\#')  # .replace('\n', '<br>')

        self.comments = set()
        self.json_data = data

    def get_members(self):
        comments = []

        for c in self.comments:
            comments.append(c)
            for r in c.replies:
                comments.append(r)

        members = set()
        for c in comments:
            if c.author.hasOfficialMark:
                members.add(c.author)

        if self.author.hasOfficialMark:
            members.add(self.author)

        return members

    def get_authors(self):
        authors = [self.author]
        members = get_members(self)
        for m in members:
            if m not in authors:
                authors.append(m)
        return authors

    def get_tag_type(self):
        if self.postType == POSTTYPE_MOMENT or self.postType == POSTTYPE_MOMENT_W1:
            return 'Moment'

        if self.author.memberId in members_ids.values():
            return 'Artist Post'

        if self.author.hasOfficialMark:
            return 'Official Post'

        return 'Fan Post'

    def get_categories(self):
        categories = []  # [ post.postType ]
        category_remapping = {
            "가로새롬": "Saerom",
            "규리": "Gyuri",
            "더여니": "Seoyeon",
            "이나경": "Nagyung",
            "이채영": "Chaeyoung",
            "지선": "Jisun",
            "지원": "Jiwon",
            "지헌": "Jiheon",
            "하영": "Hayoung",
        }

        categories += [category_remapping.get(m.profileName) if m.profileName in category_remapping else m.profileName for m in get_members(self)]
        return categories

    def has_attachment(self, type):
        for k, v in self.attachment.items():
            if k == type:
                return True
        return False

    @staticmethod
    def extract_info(text):
        pattern = r'type="([^"]+)"\s+id="([^"]+)"'
        match = re.search(pattern, text)
        return {
            'type': match.group(1),
            'id': match.group(2)
        }

    def process_attachment(self, text):
        if text.startswith('<w:link'):
            return text.replace('w:link', 'a').replace('value=', 'href=')

        if not text.startswith('<w:attachment'):
            # regular text
            text = replace_links(text)
            return text.replace('\n', '<br>')

        info = Post.extract_info(text)

        attachment_type = info['type']
        attachment_id = info['id']
        print('Processing ', attachment_type, attachment_id)

        # attachment_inner = info['inner']

        # if not text.startswith('w:link'):
        #     return f'<a href='{}'>{}'

        # <video controls="controls" preload="none" poster="{media_path}/{thumb_name}">

        if attachment_type == 'photo':
            url = self.attachment[attachment_type][attachment_id]['url']
            return make_image_md(url)
        elif attachment_type == 'video':
            return self.make_video_md(attachment_id)
        elif attachment_type == 'snippet':
            url = self.attachment[attachment_type][attachment_id]['url']
            embed_url = url

            link_md = f'<a href="{url}">{url}</a>'

            if 'youtube' in url:
                embed_url = url.replace('watch?v=', 'embed/')
                embed_url = embed_url.replace('shorts', 'embed')
                print('EMBED', embed_url)
            else:
                return f'<figure class="snippet" markdown="1">\n{link_md}\n</figure>'

            return dedent(f"""
                <figure class="snippet" markdown="1">
                <iframe src="{embed_url}" title="What is this"></iframe>
                {link_md}
                </figure>
                """)

        return f'{attachment_type}:{attachment_id}'


    def make_video_md(self, attachment_id):
        if youtubeVideoId := video_redirects.get(attachment_id):
            return make_iframe_md(f'https://www.youtube.com/embed/{youtubeVideoId}')
        else:
            media_path = f'/assets/videos/weverse_{attachment_id}.mp4'
            if not os.path.exists(media_path):
                print('MISSING ', media_path, self.shareUrl)
                # breakpoint()

            thumb_path = f'/assets/videos/weverse_{attachment_id}-thumb.jpg'
            return dedent(f"""
            <figure markdown="1">
            <video controls="controls" preload="none" poster="{thumb_path}">
            <source src="{media_path}#t=1" type="video/mp4">
            Your browser does not support the video tag.
            </video>
            </figure>""")


    def split_body(self):
        pattern = r"(<w:.*?>.*?<\/.*?>)"
        sub_pattern = r'(<w:.*?\/>)'

        split_body = re.split(pattern, self.body)
        out = []
        for body in split_body:
            sub_split = re.split(sub_pattern, body)
            out += sub_split

        return out  # [o.strip() for o in out if o.strip()]

    def get_moment_ext(self):
        if self.postType == 'MOMENT':
            return self.extension['moment']
        elif self.postType == 'MOMENT_W1':
            return self.extension['momentW1']
        return None

    def process_moment(self):
        ext = self.get_moment_ext()
        content = ''

        if photo := ext.get('photo'):
            content = make_image_md(photo['url'])

        if video := ext.get('video'):
            content = self.make_video_md(video['videoId'])

        if backgroundImage := ext.get('backgroundImageUrl'):
            content = make_image_md(backgroundImage)

        if self.plainBody and len(self.plainBody) > 0:
            return dedent(f"""
<figure markdown="1">
{content}
<figcaption>{self.plainBody.replace('\n', '<br>')}</figcaption>
</figure>
            """
                          )
        else:
            return dedent(f"""
<figure markdown="1">
{content}
</figure>""")

    def process_body(self):
        if self.postType == POSTTYPE_MOMENT or self.postType == POSTTYPE_MOMENT_W1:
            return self.process_moment()

        # print(self.attachment)
        # pattern = r'<(.*?)\s*/>'
        # split_body = [self.process_attachment(s) for s in re.split(pattern, self.body) if s.strip()]
        split_body = [self.process_attachment(s) for s in self.split_body()]
        if len(split_body) > 1:
            print(split_body)
        return '\n'.join(split_body)

    def process_extensions(self):
        lines = []
        if image := self.extension.get('image'):
            if photos := image.get('photos'):
                for p in photos:
                    url = p['url']
                    lines.append(make_image_md(url, figure=True))

        if youtube := self.extension.get('youtube'):
            youtubeVideoId = youtube['youtubeVideoId']
            md = make_iframe_md(f'https://www.youtube.com/embed/{youtubeVideoId}', f'https://www.youtube.com/watch?v={youtubeVideoId}')
            lines.append(md)

        return '\n'.join(lines)

    def __eq__(self, other):
        return self.postId == other.postId if isinstance(other, Post) else False

    def __hash__(self):
        return hash(self.postId)

    def __lt__(self, other):
        return self.date < other.date

    def arrange_comments(self):
        new_comments = set()
        for c in self.comments:
            if c.parent:
                new_comments.add(c.parent.comment)
            else:
                new_comments.add(c)

        self.comments = list(new_comments)

    def __repr__(self):
        properties = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({properties})"


class Parent:
    def __init__(self, comment, data):
        self.type = data['type']
        self.post = None
        self.comment = None
        if self.type == PARENT_TYPE_POST:
            # self.post = Post(data['data'])
            self.post = data['data']['postId']
        elif self.type == PARENT_TYPE_COMMENT:
            self.comment = data['data']['commentId']  # self.comment = Comment(data['data'])  # self.comment.replies.append(comment)
        else:
            print('UNKNOWN PARENT TYPE ', self.type)
            breakpoint()

    def __repr__(self):
        properties = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({properties})"


class Comment:
    def __init__(self, data):
        self.createdAt = get_datetime(data.get('createdAt'))
        self.body = data.get('body').replace('#', '\\#').replace('\n', '<br>')
        # self.availableActions = data.get('availableActions')
        self.emotionCount = data.get('emotionCount')
        self.commentCount = data.get('commentCount')
        self.writtenIn = data.get('writtenIn')
        self.commentId = data.get('commentId')
        self.parent = Parent(self, data.get('parent')) if data.get('parent') else None  # what we are replying to, COMMENT / POST
        self.author = Author(data.get('author'))

        # self.root = None
        # new_root = Post(self, data.get('root')['data'], data.get('root')['type']) if data.get('root') else None
        # if new_root:
        #     if new_root.postId in post_database:
        #         self.root = post_database[new_root.postId]
        #     else:
        #         self.root = new_root
        #         post_database[new_root.postId] = self.root
        # self.root = Root(self, data.get('root')['data'], data.get('root')['type']) if data.get('root') else None # the root (always a post?)

        # if self.root:
        #     self.root.post.comments.append(self)

        self.replies = []

    def __repr__(self):
        properties = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({properties})"


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


def process_comment(comment):
    name = comment.author.profileName

    if comment.author.hasOfficialMark:
        name_md = f'<span class="artist">{name}</span>'
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


def get_members(post):
    comments = []

    for c in post.comments:
        comments.append(c)
        for r in c.replies:
            comments.append(r)

    members = set()
    for c in comments:
        if c.author.hasOfficialMark:
            members.add(c.author)

    if post.author.hasOfficialMark:
        members.add(post.author)

    return members


def get_authors(post):
    authors = [post.author]
    members = get_members(post)
    for m in members:
        if m not in authors:
            authors.append(m)
    return authors


def get_categories(post):
    categories = []  # [ post.postType ]
    category_remapping = {
        "가로새롬": "Saerom",
        "규리": "Gyuri",
        "더여니": "Seoyeon",
        "이나경": "Nagyung",
        "이채영": "Chaeyoung",
        "지선": "Jisun",
        "지원": "Jiwon",
        "지헌": "Jiheon",
        "하영": "Hayoung",
    }

    categories += [category_remapping.get(m.profileName) if m.profileName in category_remapping else m.profileName for m in get_members(post)]
    return categories


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
    post_members = get_authors(post)

    if len(post_members) == 0:
        breakpoint()
    categories = get_categories(post)
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
date: {post.publishedAt}
authors:
{member_authors}{categories_md}
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
            txt.writelines(out_file)  # print(len(out_file), len(out_file.split('\n')))


def get_comment_data():
    with open('raw/post-data/all_comments.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def gather_comments(comment_data, post_database):
    all_comments = dict()

    for comment_data in comment_data:
        root = comment_data['root']['data']
        post_id = root['postId']

        comment = Comment(comment_data)

        if comment.commentId in all_comments:
            # print(comment_data)
            continue  # breakpoint()

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
            post_database[post_id].comments.add(main_comment)  # else:  #     print('FAILED TO FIND', post_id)

    for k, post in post_database.items():
        post.comments = sorted(post.comments, key=lambda c: c.createdAt)

        for c in post.comments:
            c.replies = sorted(c.replies, key=lambda c: c.createdAt)


def make_post_database(data, comment_data = None):
    post_database = gather_posts(data)
    gather_comments(get_comment_data() if not comment_data else comment_data, post_database)
    return post_database


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


def make_authors(sorted_posts):
    authors = set()
    for post in sorted_posts:
        for m in get_members(post):
            authors.add(m)

        if post.author not in authors:
            authors.add(post.author)

    text = ''
    # for author in authors.values():
    #     if author.hasOfficialMark:
    #         print(author.profileName)
    for author in authors:
        name = str(author.profileName).replace('\x81', '').replace('\x8d', '').replace("'", '')
        # name = remove_emojis(name)
        if len(name) == 0:
            name = '(Error emojis)'

        text += f'''  {author.memberId}:
    name: '{name}'
    description: ''
    avatar: {author.profileImageUrl + '?type=s72'}
'''

    out_file = f'''authors:
{text}
'''
    with open(f'{base_dir}/.authors.yml', mode='w', encoding='utf-8') as txt:
        txt.writelines(out_file)


def get_post_data(files):
    all_post_data = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            for data in json_data:
                # if data['postId'] != '4-274884509':
                #     continue
                all_post_data.append(data)  # print(len(all_post_data))

    return all_post_data


def load_json_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def get_ext(file):
    return file.rsplit('.')[-1]

def download_img(image_url, file_path, skip_exists=True):
    if skip_exists and os.path.exists(file_path):
        print('skip')
        return

    while True:  # Infinite loop to keep trying
        try:
            # Send a GET request to the URL
            print(f"Downloading {file_path} {image_url}")
            response = requests.get(image_url)

            # Check if the request was successful
            if response.status_code == 200:
                print("Writing to file...")
                # Open a file in binary write mode to save the image
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    print("Image downloaded successfully!")
                return  # Exit the loop if download is successful
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                time.sleep(10)  # Optional: Wait before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)  # Optional: Wait before retrying