my_data = {}
my_data.data = []

function download_json(data)
{
    const jsonData = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonData], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'posts-api.json';
    link.click();
}

function setup_hook()
{
    XMLHttpRequest.prototype.nativeOpen = XMLHttpRequest.prototype.open;

    my_hook = function(data)
    {
        return function(method, url, asynch, user, password)
        {
            this.addEventListener("readystatechange", function() {
                if (this.readyState === 4) {
                    if (url.includes('artistTabPosts'))
                    {
                        let parsed = JSON.parse(this.response);

                        console.log(url);
                        data.data = data.data.concat(parsed['data']);
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

    download_json(my_data)

    alert('Finished!')
}

await main();