import os
import textwrap
from textwrap import dedent

import python.wv_helper as wv_helper

def make_post(post):
    post_id = post.postId

    name = post.author.profileName
    if post.author.hasOfficialMark:
        name_md = f'<span class="artist">{name}</span>'
    else:
        name_md = name


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
    if post.postType == wv_helper.POSTTYPE_VIDEO:
        url = post.extension['video']['thumb']
        caption = f'<a href="{post.shareUrl}">{post.shareUrl}</a>'

        head = textwrap.dedent(f"""\
<a href="{post.shareUrl}">
{wv_helper.make_image_md(url, caption, False)}
</a>""")

    ## {post_id}


    out = f"""
## {post_id}
<small>{wv_helper.date_to_str(post.publishedAt)}</small>
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
{wv_helper.parse_comments(post.comments)}
</div>
---
'''
        out += comments_md

    return out


def make_member_markdown_file(member, title, post_database, file_path):
    print(f'making file for {member}')
    # for post in data:
        # print(post['postId'])

    post_mds = []

    sorted_posts = sorted(post_database.values(), key=lambda p: p.publishedAt)
    for p in sorted_posts:
        print(p.json_data)
        post_mds.append(make_post(p))

    body = '\n'.join(post_mds)

    author_md = dedent(f"""
    <div class='artist-img' markdown="1">
    ![]({sorted_posts[0].author.profileImageUrl}){{ pfp loading=lazy }}
    </div>
    """)

    out_file = dedent(f"""# {title}
    {author_md}
    {body}
    """)

    with open(file_path, mode='w', encoding='utf-8') as txt:
        txt.writelines(out_file)  # print(len(out_file), len(out_file.split('\n')))
    # print(data)


def main():
    # members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    members = ['Jisun']

    comment_data = wv_helper.get_comment_data()

    artist_post_data = wv_helper.get_post_data([f'raw/post-data/real_artist_posts.json'])
    all_artist_post_database = wv_helper.make_post_database(artist_post_data, comment_data)

    for member_name in members:
        if not os.path.exists(f'docs/wv-moments/{member_name.lower()}'):
            os.mkdir(f'docs/wv-moments/{member_name.lower()}')

        moment_data = wv_helper.get_post_data([f'raw/post-data/moments/{member_name.lower()}.json'])
        if len(moment_data) == 0:
            continue

        moment_filepath = f'docs/wv-moments/{member_name.lower()}/moments.md'
        moment_database = wv_helper.make_post_database(moment_data, comment_data)
        make_member_markdown_file(member_name, "Moments", moment_database, moment_filepath)

        def filter_name(elem):
            return elem[1].author.memberId == wv_helper.members_ids[member_name.lower()]

        # filter_name = lambda elem: elem[1].author.profileName == wv_helper.members_ids[member_name.lower()]
        artist_post_filepath = f'docs/wv-moments/{member_name.lower()}/artist-posts.md'
        artist_post_database = dict(filter(filter_name, all_artist_post_database.items()))
        # print(member_name, len(artist_post_database))
        make_member_markdown_file(member_name, "Artist Posts", artist_post_database, artist_post_filepath)


if __name__ == '__main__':
    print('huh')
    main()
    # members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    # members = ['Hayoung']


        # tsv_name = f'raw/{member_name}/member.tsv'
        # media_search = f'docs/media/{member_name.lower()}/moments'
        # media_path = f'/media/{member_name.lower()}/moments'
        # main()
