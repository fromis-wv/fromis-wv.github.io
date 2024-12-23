my_data = {}
my_data.data = []
my_data.postdata = []
my_data.indexes = []

temp_data = {}
// temp_data.wait_post = false
temp_data.latest_post = null
temp_data.parsed_urls = new Set()

function setup_hook()
{
    if (XMLHttpRequest.prototype.nativeOpen != null)
    {
        return;
    }

    XMLHttpRequest.prototype.nativeOpen = XMLHttpRequest.prototype.open;

    my_hook = function(data)
    {
        return function(method, url, asynch, user, password)
        {
            // console.log(method, url, asynch, user, password);
            // console.log(this)

            // Add a listener for when the request state changes
            this.addEventListener("readystatechange", function() {
                if (this.readyState === 4)
                { // Ready state 4 means the request is complete
                    // console.log("Response received for:", url);
                    // console.log("Status:", this.status);
                    // console.log("Response Text:", this.response);

                    if (url.includes('memberCommentsV1') || url.includes('fieldSet=postV1'))
                    {
                        let url_id = url.split("&wmsgpad")[0]

                        if (!temp_data.parsed_urls.has(url_id))
                        {
                            temp_data.parsed_urls.add(url_id);

                            if (url.includes('memberCommentsV1'))
                            {
                                let parsed = JSON.parse(this.response);


                                // console.log(url);
                                // console.log(parsed);

                                // let new_json = json.loads(this.response);
                                // data.data = data.data.concat(parsed['data']);
                                my_data.data.push(...parsed['data']);

                                // console.log(parsed['data'].length, data.data.length);

                                // data.data += parsed.data
                            }

                            if (url.includes('fieldSet=postV1'))
                            {
                                let parsed = JSON.parse(this.response);

                                temp_data.latest_post = parsed

                                // console.log(url);
                                my_data.postdata.push(parsed);
                            }
                        } else
                        {
                            console.error('Skipping ' + url);
                        }
                    }
                }
            });

            return this.nativeOpen(method, url, asynch, user, password);
        };
    }

    XMLHttpRequest.prototype.customOpen = my_hook(my_data);

    XMLHttpRequest.prototype.open = XMLHttpRequest.prototype.customOpen;
}

ATTR_MEDIA_ATTACH = 'data-media-attachment'
CLASS_EXPAND_POST_CONTAINER = 'WeverseViewer'
CLASS_EXPAND_POST_VIDEO = 'WidgetVideo'
ATTR_VIDEO_ATTACH = 'data-video-attachment'


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
        if (child.classList && child.classList.contains(CLASS_EXPAND_POST_VIDEO))
        {
            let video = first_class(child, 'PostPreviewVideoThumbnailView_container__kTCGQ')
            video.click();

            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();
        }
        else if (is_image_element(child))
        {
            let img_elem = child.querySelector('img[src]');

            let photo = first_class(child, 'photo');
            photo.click();

            // video takes a long time to load?
            await new Promise(resolve => setTimeout(resolve, 1000));

            await download_media();
        }
        else if (child.getAttribute('id') !== 've')
        {
            console.error('WHAT IS THIS?');
            console.error(child);
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

function first_class(elem, class_name)
{
    let found = elem.getElementsByClassName(class_name);
    if (found.length > 0)
    {
        return found[0];
    }

    return null;
}

async function wait_for_latest_post()
{
    while (true)
    {
        if (temp_data.latest_post != null)
        {
            break;
        }

        await new Promise(resolve => setTimeout(resolve, 50));
    }

    await new Promise(resolve => setTimeout(resolve, 100));

    return Promise.resolve('Done');
}

async function wait_for_element(ele_func)
{
    while (true)
    {
        if (document.getElementsByClassName(ele_func).length > 0)
        {
            break;
        }

        await new Promise(resolve => setTimeout(resolve, 50));
    }

    await new Promise(resolve => setTimeout(resolve, 50));

    return Promise.resolve('Done');
}

async function process_post(post, comment_data)
{
    post.scrollIntoView()
    let button = post.getElementsByClassName('DivAsButtonView_div_as_button__jl7Xf')[0];
    temp_data.latest_post = null;
    button.click();

    let locked = comment_data['root']['data']['locked']
    if (locked)
    {
        // await new Promise(resolve => setTimeout(resolve, 2000));
        await wait_for_element('PostPasswordModalView_post_password__roIl4')
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
            } else
            {
                alert('FAILED TO FIND PASSWORD ' + key)
                return Promise.resolve("Finished")
            }
        }
    }

    // let button = post.getElementsByClassName('DivAsButtonView_div_as_button__jl7Xf')[0];
    // button.click();
    // await new Promise(resolve => setTimeout(resolve, 3000));

    await wait_for_latest_post();
    await wait_for_element('BaseModalView_close_button__+0N-m')

    let post_data = temp_data.latest_post
    let post_id = post_data['postId']
    // console.log('Processing ' + post_id);
    // console.log("POST")
    // console.log(post_data)
    // console.log("COMMENT")
    // console.log(comment_data)

    let comment_post_id = comment_data['root']['data']['postId']
    if (post_id !== comment_post_id)
    {
        console.error('post id doesn\'t match' + post_id + " " + comment_post_id)
    }

    // await down_post();
    document.getElementsByClassName('BaseModalView_close_button__+0N-m')[0].click()

    return Promise.resolve("Finished")
}

async function process_posts()
{
    let comment_container = document.getElementsByClassName('CommunityProfileContentView_container__tZGU9')[0];
    let comments = comment_container.getElementsByClassName('CommunityProfileCommentListItemView_container__Wo2Zp');
    console.log('Found comment elems ' + comments.length)

    let visited = {}
    visited.posts = new Set()

    for (let i = 0; i < comments.length; i++)
    {
        let comment_data = my_data.data[i];

        // let locked = comment_data['root']['data']['locked']
        // if (locked !== true)
        // {
        //     continue;
        // }

        // console.log(comment_data)
        let post_id = comment_data['root']['data']['postId']
        let post_type = comment_data['root']['data']['postType']
        if (post_type !== "NORMAL")
        {
            // moment!
            continue;
        }


        let comment = comments[i]

        if (visited.posts.has(post_id))
        {
            // console.error('Skip ' + post_id);
            continue;
        }

        my_data.indexes.push(i);

        visited.posts.add(post_id)

        console.log(`Processing comment ${i} / ${comments.length}`);
        await process_post(comment, comment_data);
    }

    return Promise.resolve("Finished")
}

async function verify_posts()
{
    let comment_container = document.getElementsByClassName('CommunityProfileContentView_container__tZGU9')[0];
    let comments = comment_container.getElementsByClassName('CommunityProfileCommentListItemView_container__Wo2Zp');
    console.log('Found comment elems ' + comments.length)

    let visited = {}
    visited.posts = new Set()

    let test = {}
    test.data = []

    test.original = []
    for (let i = 0; i < my_data.data.length; i++)
    {
        let data = my_data.data[i];
        let elem = {}
        elem.index = i;
        elem.text = data['body']
        test.original.push(elem)
    }

    for (let i = 0; i < comments.length; i++)
    {
        let comment_data = my_data.data[i];
        if (my_data.length < i)
        {
            console.error('MISSING DATA ' + i);
            continue;
        }


        let data_text = comment_data['body']
        let comment_text = comments[i].getElementsByClassName('CommunityProfileCommentListItemView_my_comment__veq1S')[0].textContent
        // visited.posts.add(post_id)

        if (comment_text !== data_text)
        {
            console.log('DATA NOT MATCHING? ' + i)
            console.log(comment_text)
            console.log(data_text)
        }

        let elem = {}
        elem.data = data_text
        elem.elem = comment_text
        elem.index = i
        test.data.push(elem);
    }

    download_json(test)

    return Promise.resolve("Finished")
}

async function main()
{
    setup_hook();

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

    // await verify_posts()

    // console.log('Found comment data ' + my_data.data.length)
    await process_posts();
    //
    download_json(my_data)
    //
    alert('Finished!')
}

await main();

// https://weverse.io/fromis9/fanpost/1-91387175
