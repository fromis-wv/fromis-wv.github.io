my_data = {}
my_data.data = []

function download_json(data)
{
    const jsonData = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'comments.json';
    link.click();
}

function setup_hook()
{
    XMLHttpRequest.prototype.nativeOpen = XMLHttpRequest.prototype.open;

    my_hook = function(data)
    {
        return function(method, url, asynch, user, password)
        {
            // console.log(method, url, asynch, user, password);
            // console.log(this)


            //https://global.apis.naver.com/weverse/wevweb/comment/v1.0/post-2-147444660/artistComments?fieldSet=postArtistCommentsV1&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734314361624&wmd=7SvWRjD3iNw9XjF7%2BHWR9jCkZYc%3D

            // 'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-4-157938059?fieldSet=postV1&fields=recommendProductSlot&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734314202024&wmd=%2FCoNZkFYtQ19RGh9giae4rytqg8%3D'
            // 'https://global.apis.naver.com/weverse/wevweb/post/v1.0/post-4-157938059?fields=availableActions%2CmaxCommentCountReached&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734314202424&wmd=Pl6AK1Nxin9%2BFJLobbxW3a9Xsl4%3D'

            // Add a listener for when the request state changes
            this.addEventListener("readystatechange", function() {
                if (this.readyState === 4) { // Ready state 4 means the request is complete
                    if (url.includes('post') && url.includes('postV1')) // maybe look for fieldSet instead?
                    {
                        let parsed = JSON.parse(this.response);

                        // console.log(parsed);
                        // console.log(parsed['data']);

                        // let new_json = json.loads(this.response);
                        data.data = data.data.concat(parsed['data']);

                        console.log(url);
                        console.log(parsed);

                        // data.data += parsed.data
                    }
                }
            });

            return this.nativeOpen(method, url, asynch, user, password);
        };
    }

    XMLHttpRequest.prototype.customOpen = my_hook(my_data);

    XMLHttpRequest.prototype.open = XMLHttpRequest.prototype.customOpen;
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

        await new Promise(resolve => setTimeout(resolve, 10000));

        if (window.scrollY === last_height)
        {
            clearInterval(handle);
            return Promise.resolve("Finished")
        }
    }
}

async function main()
{
    setup_hook();

    // for (let tab of document.getElementsByClassName('CommunityProfileContentTabView_tab_link__v-CdV'))
    // {
    //     if (tab.textContent === 'Comments')
    //     {
    //         tab.click();
    //         break;
    //     }
    // }
    //
    // await new Promise(resolve => setTimeout(resolve, 3000));
    //
    // await scroll_bottom()
    //
    // download_json(my_data)

    alert('Finished!')
}

await main();