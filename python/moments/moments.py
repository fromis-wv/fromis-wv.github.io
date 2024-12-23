import csv
from datetime import datetime
import os
from pydoc import describe

INDEX_ID = 'index'
POST_ID = 'post'
DATE_ID = 'date'
NAME_ID = 'name'
TEXT_ID = 'text'
REPLY_ID = 'reply'

skip_your_msgs = True

empty_profile_url = 'https://cdn-v2pstatic.weverse.io/wev_web_fe/p/2_31_0/public/static/media/icon_empty_profile.b0996808ea97350978a4.png'

headers = [INDEX_ID, POST_ID, DATE_ID, NAME_ID, TEXT_ID, REPLY_ID]

from collections import OrderedDict

class Comment:
    def __init__(self):
        self.index = -1
        self.text = ''
        self.name = ''
        self.date = None
        self.thumbnail = None
        self.replies = []

    def log(self):
        print(f'{str(self.index)} {str(self.date)} {str(self.name)} {self.text}')

        # print('replies', len(self.replies))
        for r in self.replies:
            print('REPLY')
            r.log()


    def __lt__(self, other):
        return self.date < other.date


class Post:
    def __init__(self):
        self.description = ''
        self.date = None
        self.comments = []
        self.id = ''
        self.url = ''

    def log(self):
        print(f'{self.id} {self.date} {self.description}')
        for comment in self.comments:
            comment.log()


posts = dict()

def make_media(post):
    media_name = find_media(post.id)
    print('MAKE MEDIA', media_name)

    if media_name.endswith('.jpg') or media_name.endswith('.png'):
        return f'![]({post.url}){{ loading=lazy }}'

    # if media_name.endswith('.mp4'):
    #     return f'<video class="webplayer-internal-video" controls disablepictureinpicture="true" src="{post.url}"></video>'
    # return media_name

    if media_name.endswith('.jpg') or media_name.endswith('.png'):
        return f'![](..{media_path}/{media_name}){{ loading=lazy }}'

    if media_name.endswith('.mp4'):
        thumb_name = f'{media_name.removesuffix('.mp4')}-thumb.jpg'
        return f"""
<video controls="controls" preload="none" poster="{media_path}/{thumb_name}">
<source src="{media_path}/{media_name}#t=1" type="video/mp4">
Your browser does not support the video tag.
</video>
"""
    return media_name

def read_comment(comment):
    thumb = comment.thumbnail if len(comment.thumbnail) else empty_profile_url
    out = \
f"""
<div class="comment" markdown="1">
**{comment.name}** <small>{comment.date}</small><br>
{comment.text}
</div>
"""

    # f"""
    # !!! info "{comment.date} {comment.name}"
    #     {comment.text}
    # """

    for reply in comment.replies:
        print('found reply')
        reply.log()
        out += \
f"""
<div class="reply" markdown="1">
<div class="comment" markdown="1">
**{reply.name}** <small>{reply.date}</small><br>
{reply.text}
</div>
</div>
"""
# f"""
# <div class="reply" markdown="1">
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**{reply.name}** <small>{reply.date}</small><br>
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{reply.text}
# </div>
# """
#&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**@{comment.name}** {reply.text}
        # **{reply.date} {reply.name}**
        # <br>**@{comment.name}** {reply.text}
    return out

def find_media(post_id):
    print('SEARCHING FOR ', post_id, media_search)
    for root, sub, files in os.walk(media_search):
        for f in files:
            just_name = f.rsplit('.')[0]
            if just_name.endswith('-thumb'):
                continue
            if just_name.startswith(post_id):
                print('\t', f)
                return f

    return 'MISSING MEDIA'

def read_post(post):
    out_text = \
f"""
## {post.date}

<figure markdown="span">
{make_media(post)}<br>
<figcaption>{post.description}</figcaption>
</figure>
"""

    if len(post.comments) > 0:
        out_comments = ''
        for c in post.comments:
            out_comments += read_comment(c)
        out_comments = \
f"""
<div class="comments-container md-sidebar__scrollwrap" markdown="1">
{out_comments}
</div>
"""
        out_text += out_comments


    return \
f"""
<div class="post" markdown="1">
    {out_text}
</div>
"""



def make_page():
    out_file = \
f"""---
draft: true 
date: 2024-01-31 
categories:
  - Hello
  - World
---

# Moments
"""

    # {member_name}

    for post_id, p in posts.items():
        post = read_post(p)
        out_file += post
        # out_file += '\n---\n'

    return out_file


def main():
    main_dict = dict()

    posts.clear()

    with open(tsv_name, encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='\v')
        for line in rd:
            print(line)
            if len(line) == 4:
                new_post = Post()
                new_post.id = line[0]
                new_post.date = line[1]
                new_post.description = line[2]
                new_post.url = line[3]
                posts[line[0]] = new_post
            else:
                row = dict()

                index = int(line[0])
                post_name = line[1]

                comment = Comment()
                comment.index = index
                comment.date = datetime.strptime(line[2], '%b %d, %Y, %H:%M')
                comment.name = line[3]
                comment.text = line[4].replace('\n', '<br>').replace('#', '\#')
                comment.thumbnail = line[6]

                reply = None
                if len(line) > 5:
                    if line[5] != '':
                        print(line[5])
                        reply = int(line[5])

                if reply is not None:
                    print('LOOKING FOR', reply, index)
                    post = posts[post_name]
                    for c in post.comments:
                        print('\t', c.index)
                        if c.index == reply:
                            print('ADDED REPLY')
                            c.replies.append(comment)
                            break
                else:
                    post = posts[post_name]
                    post.comments.append(comment)

        # def post_index(p):
        #     return p.date


        # print(sorted_numbers)  # Output: [3, 6, 9, 10, 2]

        for post_id, post in posts.items():
            post.comments = sorted(post.comments)
            # post.comments = sorted(post.comments, key=lambda c: c.date)
            # def test(item):
            #     print(item)
            #     return item[0]
            #
            # post.comments = {k: v for k, v in sorted(post.comments, key=test)}
            # post.log()


    out_file = make_page()
    folder = f'docs/{member_name.lower()}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    out_name = f'docs/{member_name.lower()}/moments.md'
    with open(out_name, mode='w', encoding='utf-8') as txt:
        txt.writelines(out_file)

if __name__ == '__main__':
    members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    # members = ['Hayoung']

    for member_name in members:
        tsv_name = f'raw/{member_name}/member.tsv'
        media_search = f'docs/media/{member_name.lower()}/moments'
        media_path = f'/media/{member_name.lower()}/moments'
        main()
