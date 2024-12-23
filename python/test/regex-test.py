import re

# text = 'Bla Bla<w:attachment type="photo" id="0-289017642" /><w:attachment type="photo" id="3-302218339" />Foo Foo'

text = 'Bla bla Foo 🍽️ <w:link value=\"https://docs.google.com/spreadsheets/d/1Lpwn9L1Ifdifvp3UkG24K9spARuhfDLdhu-1SEuBzuE/edit?usp=sharing\">레시피 보러가기</w:link> FooBarFooBar <w:attachment type=\"photo\" id=\"4-301672294\" /> Endinging'

# text = 'Foo <w:link>레시피</w:link> FooBar <w:attachment type=\"photo\" id=\"4-301672294\" /> Ending'

def extract_info(text):
    pattern = r'type="([^"]+)"\s+id="([^"]+)"'
    match = re.search(pattern, text)
    return {'type': match.group(1), 'id': match.group(2)}

def process_attachment(text):
    if not text.startswith('w:attachment'):
        return text

    info = extract_info(text)
    return f'{info['type']}:{info['id']}'

def process_body(body):
    # pattern = r"(<w:.*?>.*?<\/.*?>)"
    # split_body = re.split(pattern, body)

    processed = [process_attachment(s.strip()) for s in split_body(body)]


    # out = []
    # for body in split_body:
    #     sub_pattern = r'(<w:.*?\/>)'
    #     sub_split = re.split(sub_pattern, body)
    #     out += sub_split

    return '\n'.join(processed)


def split_body(body):
    pattern = r"(<w:.*?>.*?<\/.*?>)"
    sub_pattern = r'(<w:.*?\/>)'

    split_body = re.split(pattern, body)
    out = []
    for body in split_body:
        sub_split = re.split(sub_pattern, body)
        out += sub_split

    return out

print(process_body(text))
