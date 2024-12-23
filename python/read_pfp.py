import json
import os.path


def find_thumbnails(member_name, thumbs):
    file_name = f'raw/{member_name.lower()}/posts/data.json'

    if os.path.exists(file_name):
        with open(file_name, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            all_posts = data['posts']

            for p in all_posts:
                add_thumb(thumbs, p['member'], p['thumb'])

                for c in p['comments']:
                    add_thumb(thumbs, c['name'], c['thumb'])
                    for s in c['sub_comments']:
                        add_thumb(thumbs, s['name'], s['thumb'])


def add_thumb(thumbs, name, url):
    if url != '' and name not in thumbs:
        thumbs[name] = url


def main():
    members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    # members = ['Nagyung']

    thumbs = {}

    for member_name in members:
        find_thumbnails(member_name, thumbs)

    for n, u in thumbs.items():
        print(n, u)

    with open("raw/misc/pfps.txt", "w", encoding='utf-8') as file:
        file.write(str(thumbs))

if __name__ == '__main__':
    main()
