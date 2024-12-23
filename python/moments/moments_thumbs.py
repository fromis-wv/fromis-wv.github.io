import csv
import mimetypes
from urllib.error import URLError

import requests, imghdr

def get_base_name(url):
    return url.split('https://phinf.wevpstatic.net/')[1].split('/')[0]

def get_all_urls():
    thumbs = set()

    members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    for member_name in members:
        tsv_name = f'raw/{member_name}/member.tsv'
        with open(tsv_name, encoding='utf-8') as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='\v')

            for line in rd:
                if len(line) > 4:
                    url = line[-1]
                    if len(url):
                        thumbs.add(line[-1])

        # for t in thumbs:
        #     print(t)

    return thumbs

def download_url(url):

    if 'empty_profile' in url:
        # save_basename = 'thumb-empty_profile'
        download('thumb-empty_profile', url)
    else:
        thumb_url = url
        source_url = url.removesuffix('?type=s68')

        base_name = get_base_name(url)

        download('thumb-' + base_name, thumb_url)
        download('src-' + base_name, source_url)


    # print(save_basename, url)
    # # print(response.headers['Content-Type'])
    # # print(mimetypes.guess_all_extensions(response.headers['Content-Type'], strict=False))
    #
    # response = requests.get(url)
    # if response.status_code != 200:
    #     raise URLError
    #
    # extension = imghdr.what(file=None, h=response.content)
    # save_path = f"raw/thumbnails/{save_basename}.{extension}"
    # with open(save_path, 'wb') as f:
    #     f.write(response.content)

def download(save_basename, url):
    print(save_basename, url)
    response = requests.get(url)
    if response.status_code != 200:
        raise URLError

    extension = imghdr.what(file=None, h=response.content)
    save_path = f"raw/thumbnails/{save_basename}.{extension}"
    with open(save_path, 'wb') as f:
        f.write(response.content)

def run():
    urls = get_all_urls()

    # download_url('https://phinf.wevpstatic.net/MjAyMjA2MTdfODAg/MDAxNjU1NDY0MTg0OTEx.ZL9fDt8pGJfq3YDsP14mtDtnQxF0PqAkJyZELsd1NlQg.8BOGOVqeazJ9qjyz2XCWFnWh0vXL7svKkv36fiRBe9wg.JPEG/c6209f76dfb240e5921eb626a24b6b35896.jpg?type=s68')

    for url in urls:
        download_url(url)

run()