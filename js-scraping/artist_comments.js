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

            // Add a listener for when the request state changes
            this.addEventListener("readystatechange", function() {
                if (this.readyState === 4) { // Ready state 4 means the request is complete
                    // console.log("Response received for:", url);
                    // console.log("Status:", this.status);
                    // console.log("Response Text:", this.response);

                    if (url.includes('memberCommentsV1'))
                    {
                        let parsed = JSON.parse(this.response);

                        console.log(url);
                        // console.log(parsed);
                        // console.log(parsed['data']);

                        // let new_json = json.loads(this.response);
                        data.data = data.data.concat(parsed['data']);
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