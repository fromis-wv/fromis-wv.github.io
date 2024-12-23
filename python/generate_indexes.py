def make_member(member_name):

    out_file = f'''# {member_name}

[Moments](moments.md)<br>
[Posts]({member_name}/posts)<br>
[DM](https://fromis-dm.github.io/posts/{member_name.lower()}/)

    '''
    name = f'docs/{member_name.lower()}/index.md'
    with open(name, mode='w', encoding='utf-8') as txt:
        txt.writelines(out_file)

def main():
    members = ['Saerom', 'Hayoung', 'Jiwon', 'Jisun', 'Seoyeon', 'Chaeyoung', 'Nagyung', 'Jiheon']
    # members = ['Nagyung']

    for member_name in members:
        make_member(member_name)

if __name__ == '__main__':
    main()