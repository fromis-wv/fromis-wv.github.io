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

MORE_BTN = 'SimpleShowMoreCommentView_container__HH0qw'

do_click = true

skip_down = true
skip_comments = true

function wait_request()
{
    request_state.waiting_request = true;
}

async function scroll_bottom()
{
    let last_height = 0

    // keep trying to scroll every 500ms
    let handle = setInterval(function()
    {
        window.scrollBy(0, 500);
    }, 200);

    // if the scroll height hasn't changed for 10s, we are done
    while (true)
    {
        last_height = window.scrollY

        await new Promise(resolve => setTimeout(resolve, 10000));

        if (window.scrollY === last_height)
        {
            clearInterval(handle);
            return Promise.resolve("Finished")
        }
    }
}

function get_inner_text(e)
{
    for (let c of e.childNodes)
    {
        if (c.nodeType === Node.TEXT_NODE)
        {
            return c.textContent;
        }
    }
    return '';
}

function download_json(data)
{
    const jsonData = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'data.json';
    link.click();
}

function first_class(elem, class_name)
{
    let found = elem.getElementsByClassName(class_name);
    if (found.length > 0)
    {
        return found[0];
    }

    return null;
}

function first_class_arr(e, a)
{
    for (c of a)
    {
        let f = first_class(e, c);
        if (f)
        {
            return f;
        }
    }

    return null;
}

async function click_close_btn()
{
    first_class(document, CLASS_CLOSE_BTN).click();
    await new Promise(resolve => setTimeout(resolve, 1000));
    return Promise.resolve("Foo")
}

async function down_text(post)
{
    await down_comments(post);
    await click_close_btn();
    return Promise.resolve("Foo")
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

async function down_post(out_post)
{
    let scrollDiv = first_class(document,'PostModalView_post_body__Ni5Ja');
    if (scrollDiv != null)
    {
        await scroll_elem(scrollDiv);
    }

    let post_elements = []
    let post_container = first_class(document, 'ReactModal__Content');
    let container = first_class(post_container, CLASS_EXPAND_POST_CONTAINER);
    // console.log(container);
    // console.log(container.children.length);
    for (let child of container.children)
    {
        child.scrollIntoView();
        // console.log(child);
        if (child.className === 'p')
        {
            let elem = {}
            elem.type = 'TEXT';
            elem.text = child.innerText;
            post_elements.push(elem);
        }
        else if (child.classList && child.classList.contains(CLASS_EXPAND_POST_VIDEO))
        {
            let video_id = child.getAttribute(ATTR_VIDEO_ATTACH);

            let elem = {}
            elem.type = 'VIDEO';
            elem.id = `${video_id}`;

            // post_elements.push(`weverse_${video_id}.mp4`);
            post_elements.push(elem);

            let video = first_class(child, 'PostPreviewVideoThumbnailView_container__kTCGQ')
            video.click();

            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();

            // let close_btn = first_class(document, 'ImageViewerView_close_button__9LG7D');
            // close_btn.click();
            //
            // await new Promise(resolve => setTimeout(resolve, 1000));
        }
        else if (is_image_element(child))
        {
            let image_id = child.getAttribute(ATTR_MEDIA_ATTACH);

            console.log('SEARCHING');
            console.log(child);
            let img_elem = child.querySelector('img[src]');
            console.log(img_elem);
            let image_url = img_elem.getAttribute('src');

            let elem = {}
            elem.type = 'IMAGE';
            elem.id = `${image_id}`;
            elem.link = image_url;
            post_elements.push(elem);

            let photo = first_class(child, 'photo');
            photo.click();

            // video takes a long time to load?
            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();

            // let close_btn = first_class(document, 'ImageViewerView_close_button__9LG7D');
            // close_btn.click();
            //
            // await new Promise(resolve => setTimeout(resolve, 1000));
        }
        else if (child.getAttribute('id') !== 've')
        {
            console.error('WHAT IS THIS?');
            console.error(child);
        }
    }

    out_post.data = post_elements;
    out_post.member = first_class(post_container, CLASS_POST_NICKNAME).textContent
    out_post.date = first_class(post_container, CLASS_POST_DATE).textContent

    let thumb_ele = first_class(post_container, "ProfileThumbnailView_thumbnail__8W3E7")
    out_post.thumb = thumb_ele ? thumb_ele.getAttribute('src') : '';

    out_post.likes = get_inner_text(first_class(first_class(post_container, CLASS_POST_LIKES_CONTAINER), CLASS_BUTTON_LIKES))
    out_post.comments = []

    return Promise.resolve("Foo")
}

function data_string(data)
{
    return JSON.stringify(data, null, 2);
}

function already_parsed(comment_data, post_data)
{
    // let find_dupe = data => d => (d.name === data.name && d.date === data.date && d.text === data.text)
    let find_dupe = data => d => (d.id === data.id);
    return post_data.comments.find(find_dupe(comment_data))
}

function make_comment_data(comment, post_data)
{
    let comment_data = {};
    // comment_data.index = post_data.comments.length;
    comment_data.text = first_class(comment, CLASS_COMMENT_TEXT).innerText;
    comment_data.name = first_class(comment, CLASS_COMMENT_NAME).textContent;
    comment_data.date = first_class(comment, CLASS_COMMENT_DATE).textContent;
    comment_data.alias = comment.getAttribute(ATTR_COMMENT_ALIAS);
    comment_data.id = comment.getAttribute("data-comment-id");
    comment_data.sub_comments = []

    let thumb_ele = comment.getElementsByClassName("ProfileThumbnailView_thumbnail__8W3E7")[0]
    comment_data.thumb = thumb_ele ? thumb_ele.getAttribute('src') : '';

    return comment_data;
}

function click_comment(comment)
{
    comment.getElementsByClassName(CLASS_COMMENT_TEXT)[0].children[0].children[0].click();
}

async function click_more_button(comment)
{
    let actual_btn = first_class(comment, 'styles_more__BQOyF');
    if (actual_btn != null)
    {
        let more_btn = first_class(comment, 'SimpleShowMoreCommentView_container__HH0qw');
        if (more_btn != null && more_btn.parentElement != null && more_btn.parentElement.click != null)
        {
            console.log('clicked?');
            more_btn.parentElement.click();
            await new Promise(resolve => setTimeout(resolve, 200));
        }
    }

    return Promise.resolve("Foo");
}

// async function scroll_sidebar(sidebar_index, count)
// {
//     // console.log('Scroll sidebar ' + count)
//     let sidebar = document.getElementsByClassName('commentList')[sidebar_index];
//
//     for (let i = 0; i < count; i++)
//     {
//         sidebar.scrollTop += 200;
//         // console.log('Scrolling ' + sidebar.scrollTop);
//         await new Promise(resolve => setTimeout(resolve, 100));
//     }
//
//     return Promise.resolve("Foo");
// }

async function parse_sub_comments(post_data, source_data)
{
    let error_msg = document.getElementsByClassName('CommonModalView_description__Sb7r+');
    if (error_msg != null && error_msg.textContent === 'Deleted comment.')
    {
        // ModalButtonView_-confirm__2YBz1
        console.error('Skip deleted comment?');
        return Promise.resolve("Foo");
    }

    let artists_reply_list = null;

    for (let i = 0; i < 30; i++)
    {
        let replies = document.getElementsByClassName(CLASS_COMMENT_CONTAINER_REPLY);
        let original_comment_container = first_class(document, 'CommentViewerView_wrap_original_comment__p3f92')
        if (replies.length >= 2)
        {
            console.log('FOUND artist reply?')
            artists_reply_list = replies[1];
        }

        if (artists_reply_list == null)
        {
            console.log('Artist reply null ' + i);
        }
        else if (original_comment_container == null)
        {
            console.log('Original comment null ' + i);
        }

        if (artists_reply_list != null && original_comment_container != null)
        {
            await new Promise(resolve => setTimeout(resolve, 1000));
            break;
        }

        await new Promise(resolve => setTimeout(resolve, 300));
    }

    if (!artists_reply_list)
    {
        console.error('FAILED TO FIND ARTIST_REPLY_LIST? ', source_data.text);
        return Promise.resolve("Foo");
    }

    let sub_comments = artists_reply_list.getElementsByClassName(CLASS_COMMENT);

    let original_comment_container = first_class(document, 'CommentViewerView_wrap_original_comment__p3f92')
    if (!original_comment_container)
    {
        console.error('FAILED TO FIND COMMENT CONTAINER?', source_data.text);
        return Promise.resolve("Foo");
    }

    let original_comment = first_class(original_comment_container, CLASS_COMMENT);

    await click_more_button(original_comment);
    let original_data = make_comment_data(original_comment, post_data);
    console.log(`Parsing reply comment ${original_data.id}`);

    if (already_parsed(original_data, post_data))
    {
        console.log('Skipping already parsed ' + original_data.id);
        return Promise.resolve("Foo");
    }

    // console.log('Original data')
    // console.log(original_data);

    // expand the first latest reply
    for (let comment of sub_comments)
    {
        let alias = comment.getAttribute(ATTR_COMMENT_ALIAS)
        if (alias === ALIAS_COMMENT_LATEST || alias === ALIAS_ARTIST_REPLY_LATEST)
        {
            click_comment(comment);
            await new Promise(resolve => setTimeout(resolve, 1000));
            break;
        }
    }

    // refresh subcomments
    sub_comments = artists_reply_list.getElementsByClassName(CLASS_COMMENT);
    // await scroll_sidebar(1, sub_comments.length + 1);

    for (let comment of sub_comments)
    {
        let alias = comment.getAttribute("data-comment-alias")
        if (alias === "GROUPED_ARTIST_REPLY_COMMENT" || alias === "GROUPED_ARTIST_REPLY_COMMENT_LATEST")
        {
            comment.scrollIntoView();
            await new Promise(resolve => setTimeout(resolve, 50));

            await click_more_button(comment);

            let comment_data = make_comment_data(comment, post_data);
            console.log(`\tSubcomment ${data_string(original_data.id)}`);

            original_data.sub_comments.push(comment_data);
            // post_data.comments.push(comment_data);
            // console.log(`Parsing CHILD artist reply ${main_index} ${row.text}`)
        }
        else
        {
            console.error('UNKNOWN SUBCOMMENT ALIAS ' +  alias)
        }
    }

    post_data.comments.push(original_data);

    return Promise.resolve("Foo");
}

async function parse_comment(comment, post_data)
{
    let alias = comment.getAttribute(ATTR_COMMENT_ALIAS);

    if (alias === 'COMMENT')
    {
        return Promise.resolve("Foo");
    }

    // let comment_data = make_comment_data(comment);
    // console.log(`Parsing comment ${data_string(comment_data)}`);

    if (alias === ALIAS_ARTIST)
    {
        first_class(comment, CLASS_COMMENT_TEXT);

        await click_more_button(comment);
        let comment_data = make_comment_data(comment, post_data);
        post_data.comments.push(comment_data);

        // console.log('Parsed artist comment', comment_data.text)

        // comment_data.text = first_class(comment, CLASS_COMMENT_TEXT).textContent;
        // comment_data.name = first_class(comment, CLASS_COMMENT_NAME).textContent;
        // comment_data.date = first_class(comment, CLASS_COMMENT_DATE).textContent;
        // comment_data.alias = alias;
    }
    else if (alias === ALIAS_ARTIST_REPLY)
    {
        let reply_data = make_comment_data(comment, post_data);
        if (already_parsed(reply_data, post_data))
        {
            console.log(`Skipping ${reply_data.id}`);
            return Promise.resolve("Foo");
        }

        await click_more_button(comment);

        click_comment(comment);
        await new Promise(resolve => setTimeout(resolve, 500));

        await parse_sub_comments(post_data, reply_data);

        let close_btn_container = first_class(document,'CommentView_container__Yu5S3');
        first_class(close_btn_container, 'CommentTitleView_back_button__SX9x7').click();

        await new Promise(resolve => setTimeout(resolve, 500));
    }
    else
    {
        console.error('UNKNOWN ALIAS ' +  alias)
    }

    return Promise.resolve("Foo")
}

async function down_comments(out_post)
{
    let container = first_class(document, CLASS_COMMENT_CONTAINER);
    if (container === null) // no artist comments
    {
        return Promise.resolve("Foo");
    }

    let comments = container.getElementsByClassName(CLASS_COMMENT);

    for (let comment of comments)
    {
        let alias = comment.getAttribute(ATTR_COMMENT_ALIAS)
        if (alias === ALIAS_COMMENT_LATEST || alias === ALIAS_ARTIST_REPLY_LATEST)
        {
            click_comment(comment);
            await new Promise(resolve => setTimeout(resolve, 500));
            // let child = comment.getElementsByClassName('CommentView_comment_text__tlVgA')[0].children[0].children[0]
            // if (child)
            // {
            //     child.click()
            // }
            break;
        }
    }

    console.log(`FOUND ${comments.length} comments`);
    // await scroll_sidebar(0, comments.length);

    for (let comment of comments)
    {
        comment.scrollIntoView();
        await parse_comment(comment, out_post);
    }

    // await new Promise(resolve => setTimeout(resolve, 1000));
    return Promise.resolve("Foo")
}

async function test()
{
    // await run();
    let out_post = {}
    out_post.comments = []

    await down_post(out_post)
    // await process_post(out_post)
    // await down_comments(out_post);

    let json_str = JSON.stringify(out_post, null, 2);
    console.log(json_str)
    // console.log('FINISHED')
    // return Promise.resolve("Foo")
}

// test();

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

async function process_post(out_post)
{
    out_post.comments = []

    if (!skip_down)
    {
        await down_post(out_post)
    }
    if (!skip_comments)
    {
        await down_comments(out_post)
    }
    // json_str = JSON.stringify(out_post, null, 2);
    // console.log(json_str)
    // console.log('FINISHED')
    return Promise.resolve("Foo")
}

async function read_post(post, all_posts)
{
    let image_post = first_class(post, CLASS_POST_IMAGE);
    if (image_post)
    {
        console.log('IMAGE')
        if (do_click)
        {
            wait_request();
            image_post.click()

            await new Promise(resolve => setTimeout(resolve, 2000));

            let out_post = {}
            out_post.post_id = get_post_id()
            await process_post(out_post);
            all_posts.posts.push(out_post);

            first_class(document,'BaseModalView_close_button__+0N-m').click();
        }
        return Promise.resolve("Foo")
    }

    let video_post = first_class(post, CLASS_POST_VIDEO);
    if (video_post)
    {
        console.log('VIDEO')
        if (do_click)
        {
            wait_request();
            video_post.click()
            await new Promise(resolve => setTimeout(resolve, 2000));

            let out_post = {}
            out_post.post_id = get_post_id()
            await process_post(out_post);
            all_posts.posts.push(out_post);

            first_class(document,'BaseModalView_close_button__+0N-m').click();
        }
        return Promise.resolve("Foo")
    }

    let text_post = first_class_arr(post, CLASS_POST_TEXT);
    if (text_post)
    {
        // console.log('TEXT')
        // console.log(text_post.textContent)
        if (do_click)
        {
            wait_request();
            text_post.click()

            await new Promise(resolve => setTimeout(resolve, 2000));

            let out_post = {}
            out_post.post_id = get_post_id()
            await process_post(out_post);
            all_posts.posts.push(out_post);

            first_class(document,'BaseModalView_close_button__+0N-m').click();
        }
        return Promise.resolve("Foo")
    }

    let unlock_post = first_class(post, 'PostListItemView_-secret__M4x+e')
    if (unlock_post)
    {
        let name = first_class(post, 'PostHeaderView_nickname__6Cb7X').textContent;
        let date = first_class(post, 'PostHeaderView_date__XJXBZ').textContent;
        let key = `${name} ${date}`

        let password_list =
        {
            '이나경 May 29, 2023, 22:42': '0124',
            '지원 Jun 4, 2023, 18:46': '0320',
            '이채영 May 31, 2023, 23:15': '7777',
            '더여니 Jun 2, 2023, 12:30': '0124',
            '더여니 Jun 1, 2022, 18:24': '0601',
            '더여니 Mar 20, 2022, 20:52': '0122'
        }

        // in:supersonic from: before: 2022-06-02

        // jisun 28/05/2023 - PW: 1123

        let password = password_list[key];
        if (password != null)
        {
            wait_request();
            unlock_post.click();
            await new Promise(resolve => setTimeout(resolve, 2000));

            let password_input = first_class(document, 'InputWithValidateMessageView_input__acTRE');
            password_input.value = password;
            let confirm_btn = first_class(document, 'ModalButtonView_-confirm__2YBz1');
            confirm_btn.click()

            await new Promise(resolve => setTimeout(resolve, 2000));

            let out_post = {}
            out_post.post_id = get_post_id()
            out_post.password = password;
            await process_post(out_post);
            all_posts.posts.push(out_post);

            first_class(document,'BaseModalView_close_button__+0N-m').click();

            return Promise.resolve("Foo")
        }
        else
        {
            console.error('FAILED TO FIND PASSWORD ' + key)
        }
    }

    // post.getElementsByClassName('ArtistPostListItemView_container__VdeOY')
    // console.log('UNKNOWN');
    // console.log(post.textContent);
    return Promise.resolve("Foo")
}

function get_post_id()
{
    if (request_state.url == null)
    {
        console.error('POST URL FAILED');
        return 'INVALID POST ID';
    }

    let out = request_state.url;
    request_state.url = null;
    return out;
}

async function run()
{


    // await scroll_bottom();

    let all_posts = {}
    all_posts.posts = []

    let posts = document.getElementsByClassName(CLASS_POST);

    console.log(`FOUND ${posts.length} posts}`)

    for (let p of posts)
    {
        await read_post(p, all_posts);
    }

    console.log(all_posts)
    console.log(all_posts.posts)

    download_json(all_posts);

    alert('FINISHED');

    return Promise.resolve("Foo");
}

request_state = {}
request_state.waiting_request = true;
request_state.url = null;

XMLHttpRequest.prototype.nativeOpen = XMLHttpRequest.prototype.open;

function testing(foo) {
    return function(method, url, asynch, user, password)
    {
        const match = url.match("post-([^?]*)");
        if (match)
        {
            if (request_state.waiting_request)
            {
                request_state.waiting_request = false;
                request_state.url = url;
                foo.url = match[1];

                console.log('OPENING POST: ' + foo.url);
            }
        }

        return this.nativeOpen(method, url, asynch, user, password);
    }
}

XMLHttpRequest.prototype.customOpen = testing(request_state);

XMLHttpRequest.prototype.open = XMLHttpRequest.prototype.customOpen;

// test()
run()
