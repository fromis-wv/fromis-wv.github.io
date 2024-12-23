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
            alert('Finished scrolling')
            return Promise.resolve("Finished")
        }
    }
}

scroll_bottom()