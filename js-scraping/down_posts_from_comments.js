indexes = [
    0,
    2,
    13,
    20,
    21,
    22,
    36,
    37,
    52,
    54,
    76,
    85,
    91,
    102,
    104,
    112,
    123,
    126,
    159,
    164,
    178,
    202,
    217,
    222,
    235,
    245,
    255,
    257,
    267,
    285,
    301,
    306,
    307,
    308,
    342,
    378,
    389,
    400,
    418,
    419,
    420,
    421,
    422,
    423,
    424,
    425,
    426,
    427,
    428,
    429,
    430,
    431,
    432,
    433,
    434,
    435,
    436,
    437,
    438,
    439,
    440,
    441,
    442,
    444,
    445,
    446,
    447,
    448,
    449,
    450,
    451,
    452,
    453,
    454,
    455,
    456,
    457,
    458,
    459,
    460,
    461,
    462,
    463,
    464,
    465,
    466,
    467,
    468,
    469,
    470,
    481,
    482,
    483,
    484,
    485,
    486,
    487,
    488,
    489,
    490,
    491,
    492,
    493,
    494,
    495,
    496,
    497,
    503,
    514,
    519,
    520,
    532,
    545,
    546,
    564,
    565,
    566,
    567,
    568,
    569,
    570,
    571,
    572,
    573,
    574,
    575,
    576,
    577,
    578,
    579,
    580,
    581,
    582,
    583,
    584,
    585,
    586,
    587,
    588,
    589,
    590,
    591,
    592,
    593,
    594,
    595,
    596,
    597,
    598,
    599,
    600,
    601,
    602,
    603,
    604,
    605,
    606,
    618,
    647,
    652,
    653,
    654,
    655,
    656,
    657,
    658,
    659,
    660,
    661,
    662,
    663,
    664,
    665,
    666,
    667,
    668,
    669,
    671,
    672,
    673,
    674,
    680,
    681,
    682,
    683,
    684,
    693,
    701,
    719,
    720
]

CLASS_VIDEO = 'WidgetMedia WidgetVideo'
ATTR_VIDEO_ATTACH = 'data-video-attachment'
ATTR_MEDIA_ATTACH = 'data-media-attachment'


CLASS_POST = 'PostListItemView_post_item__XJ0uc'
// CLASS_POST = 'ArtistPostListItemView_container__VdeOY' // PostListItemView_post_item__XJ0uc
// CLASS_POST_TEXT = ['PostPreviewTextView_-artist__-eJ6R']
CLASS_POST_NICKNAME = 'PostHeaderView_nickname__6Cb7X'
CLASS_POST_DATE = 'PostHeaderView_date__XJXBZ'
CLASS_POST_LIKES_CONTAINER = 'PostModalView_post_action__Fiydu'
CLASS_BUTTON_LIKES = 'EmotionButtonView_button_emotion__eGktL'
// PostPreviewTextView_text__93Php

// 'PostPreviewTextView_text__93Php PostPreviewTextView_-artist__-eJ6R'
// 'ArtistPostListItemView_attachment_wrap__blcy5'
CLASS_POST_IMAGE = 'PostPreviewImageView_post_image__zLzXH'
CLASS_POST_VIDEO = 'PostPreviewVideoThumbnailView_-horizontal__ZVhma'
CLASS_POST_TEXT = ['PostPreviewTextView_text__93Php']
CLASS_CLOSE_BTN = 'BaseModalView_close_button__+0N-m'

CLASS_COMMENT = 'comment_item'
CLASS_COMMENT_ORIGINAL = 'CommentViewerView_wrap_original_comment__p3f92'
CLASS_COMMENT_CONTAINER = 'wrap_artist_comment_list'
CLASS_COMMENT_CONTAINER_REPLY = 'GroupedArtistCommentListView_artist_group__edcB6'
CLASS_COMMENT_TEXT = 'CommentView_comment_text__tlVgA'
CLASS_COMMENT_NAME = 'PostHeaderView_nickname__6Cb7X'
CLASS_COMMENT_DATE = 'PostHeaderView_date__XJXBZ'
CLASS_COMMENT_THUMB = 'ProfileThumbnailView_thumbnail__8W3E7'

CLASS_EXPAND_POST_CONTAINER = 'WeverseViewer'
CLASS_EXPAND_POST_VIDEO = 'WidgetVideo'
CLASS_EXPAND_POST_IMAGE = 'WidgetPhoto'

ATTR_COMMENT_ALIAS = 'data-comment-alias'
ALIAS_ARTIST = 'GROUPED_ARTIST_COMMENT'
ALIAS_ARTIST_REPLY = 'GROUPED_ARTIST_REPLY_COMMENT'
ALIAS_ORIGINAL = 'ORIGINAL_COMMENT'
ALIAS_ORIGINAL_ARTIST = 'ORIGINAL_COMMENT_ARTIST'
ALIAS_COMMENT_LATEST = 'GROUPED_ARTIST_COMMENT_LATEST'
ALIAS_ARTIST_REPLY_LATEST = 'GROUPED_ARTIST_REPLY_COMMENT_LATEST'

function first_class(elem, class_name)
{
    let found = elem.getElementsByClassName(class_name);
    if (found.length > 0)
    {
        return found[0];
    }

    return null;
}


function is_image_element(child)
{
    let attr = child.getAttribute(ATTR_MEDIA_ATTACH);
    if (attr)
    {
        return attr.includes('photo');
    }

    return false;
}

async function download_media()
{
    let download_btn = first_class(document, 'ImageViewerView_download_button__9ipF7');
    download_btn.click();

    await new Promise(resolve => setTimeout(resolve, 100));

    let options = document.getElementsByClassName('ImageViewerView_layer_button__3VBzE');
    if (options.length === 2)
    {
        options[1].click();
    }
    else if (options.length !== 0)
    {
        console.error('THIS SHOULD BE 2?')
    }

    let close_btn = first_class(document, 'ImageViewerView_close_button__9LG7D');
    close_btn.click();

    await new Promise(resolve => setTimeout(resolve, 1000));
    return Promise.resolve("Foo");
}

async function scroll_elem(e)
{
    let last_height = 0

    // keep trying to scroll every 500ms
    let handle = setInterval(function()
    {
        e.scrollTop += 250;
    }, 200);

    // if the scroll height hasn't changed for 10s, we are done
    while (true)
    {
        last_height = e.scrollTop;

        await new Promise(resolve => setTimeout(resolve, 2000));

        if (e.scrollTop === last_height)
        {
            clearInterval(handle);
            return Promise.resolve("Finished")
        }
    }
}

async function down_post()
{
    let scrollDiv = first_class(document,'PostModalView_post_body__Ni5Ja');
    if (scrollDiv != null)
    {
        await scroll_elem(scrollDiv);
    }

    let post_container = first_class(document, 'ReactModal__Content');
    let container = first_class(post_container, CLASS_EXPAND_POST_CONTAINER);
    // console.log(container);
    // console.log(container.children.length);
    for (let child of container.children)
    {
        child.scrollIntoView();
        await new Promise(resolve => setTimeout(resolve, 200));

        if (child.classList && child.classList.contains(CLASS_EXPAND_POST_VIDEO))
        {
            let video = first_class(child, 'PostPreviewVideoThumbnailView_container__kTCGQ')
            video.click();

            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();
        }
        else if (is_image_element(child))
        {
            // let img_elem = child.querySelector('img[src]');

            let photo = first_class(child, 'photo');
            photo.click();

            // video takes a long time to load?
            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();
        }
        else if (child.className !== 'p' && child.getAttribute('id') !== 've')
        {
            console.error('Unknown element');
            console.error(child);
            alert('Found unknown media!')
        }
    }

    return Promise.resolve("Foo")
}

function download_json(data)
{
    const jsonData = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'comment-posts.json';
    link.click();
}


async function scroll_bottom()
{
    let last_height = 0

    // keep trying to scroll every 500ms
    let handle = setInterval(function()
    {
        window.scrollBy(0, 99999);
    }, 200);

    // if the scroll height hasn't changed for 10s, we are done
    while (true)
    {
        last_height = window.scrollY

        await new Promise(resolve => setTimeout(resolve, 2000));

        if (window.scrollY === last_height)
        {
            clearInterval(handle);
            return Promise.resolve("Finished")
        }
    }
}

async function process_post(post)
{
    post.scrollIntoView()
    let button = post.getElementsByClassName('DivAsButtonView_div_as_button__jl7Xf')[0];
    button.click();

    await new Promise(resolve => setTimeout(resolve, 2000));

    let unlock_post = first_class(document, 'PostPasswordModalView_post_password__roIl4')
    if (unlock_post)
    {
        let name = first_class(document, 'CommunityProfileHeaderView_profile_name__TD0OU').textContent;
        let date = first_class(post, 'CommunityProfileCommentListItemView_my_date__f3Cjg').textContent;

        let key = `${name} ${date}`

        console.log('Searching for password: ', key)

        let password_list =
            {
                '이나경 May 29, 2023, 22:42': '0124',
                '지원 Jun 4, 2023, 18:46': '0320',
                '이채영 May 31, 2023, 23:15': '7777',
                '더여니 Jun 2, 2023, 12:30': '0124',
                '더여니 Jun 1, 2022, 18:24': '0601',
                '더여니 Mar 20, 2022, 20:52': '0122',
                "가로새롬 May 31, 2023, 00:11": '',
                '가로새롬 Sep 6, 2021, 20:24': '0107',
                '가로새롬 Feb 11, 2022, 01:52': '1154'
            }


        // May 31, 2023, 00:11
        // in:supersonic from: before: 2022-02-11

        // jisun 28/05/2023 - PW: 1123

        let password = password_list[key];
        if (password != null)
        {
            await new Promise(resolve => setTimeout(resolve, 2000));

            let password_input = document.getElementsByClassName('InputWithValidateMessageView_input__acTRE')[0];
            password_input.value = password;
            let confirm_btn = document.getElementsByClassName('ModalButtonView_-confirm__2YBz1')[0];
            confirm_btn.click()

            await new Promise(resolve => setTimeout(resolve, 2000));
        }
        else
        {
            alert('FAILED TO FIND PASSWORD ' + key)
            return Promise.resolve("Finished")
        }
    }

    await down_post();

    document.getElementsByClassName('BaseModalView_close_button__+0N-m')[0].click()
}

async function process_posts()
{
    let comment_container = document.getElementsByClassName('CommunityProfileContentView_container__tZGU9')[0];
    let comments = comment_container.getElementsByClassName('CommunityProfileCommentListItemView_container__Wo2Zp');
    console.log('Found comment elems ' + comments.length)

    for (let i of indexes)
    {
        let comment = comments[i]
        console.log('Downloading comment ' + i);
        await process_post(comment);
    }

    return Promise.resolve("Finished")
}

async function main()
{
    for (let tab of document.getElementsByClassName('CommunityProfileContentTabView_tab_link__v-CdV'))
    {
        if (tab.textContent === 'Comments')
        {
            tab.click();
            break;
        }
    }

    await new Promise(resolve => setTimeout(resolve, 3000));

    await scroll_bottom()
    // console.log('Found comment data ' + my_data.data.length)
    await process_posts();
    //
    // download_json(my_data)
    //
    alert('Finished!')
}

async function test()
{
    await down_post();
}

// test()

await main();