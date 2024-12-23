do_batch = true
all_rows = []
post_overview = []

async function down_moment()
{
    // let down = document.getElementsByClassName("DownloadButtonView_button_download__zjP42 DownloadButtonView_-moment__NmLkQ")[0]

    while (true)
    {
        await process_moment()
        // down.click()

        let next_btn = document.getElementsByClassName("MomentPageOutlineView_button_item__siPgg MomentPageOutlineView_-next__2KZST")[0]
        if (!next_btn.disabled)
        {
            next_btn.click()
            // setTimeout(down_moment, 1500);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        else
        {
            alert("Finished!")
            break;
        }
    }

    download_all_thumb()

    save_csv()
    // let row_strs = []
    // for (let row of all_rows)
    // {
    //     let orig_date = row.origdate ? row.origdate : '';
    //     let orig_name = row.origname ? row.origname : '';
    //     let orig_text = row.origtext ? row.origtext : '';
    //     let list = [row.post, row.date, row.name, `\v${row.text}\v`, orig_date, orig_name, `\v${orig_text}\v`];
    //     let row_str = list.join('\t');
    //     row_strs.push(row_str)
    // }
    //
    // console.log(row_strs);
    // save_csv_file(root_name + '.csv', row_strs.join('\n'))

    return Promise.resolve("TEXT")
}

function make_row(comment) {
    let row = {}
    row.index = all_rows.length
    row.post = root_name
    row.name = comment.getElementsByClassName("PostHeaderView_nickname__6Cb7X")[0].textContent
    row.date = comment.getElementsByClassName("PostHeaderView_date__XJXBZ")[0].textContent
    row.text = comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent
    let thumb_ele = comment.getElementsByClassName("ProfileThumbnailView_thumbnail__8W3E7")[0]
    if (thumb_ele == null)
    {
        console.log(`ERROR NULL THUMBNAIL ${row.text}`)
    }
    else
    {
        row.thumb = thumb_ele.getAttribute('src');
    }
    return row;
}

async function read_comment(comment, alias)
{
    // let time = comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent
    // console.log('Parsing ' + time)
    let sub_time = comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent

    // check if it's already been read
    let find_dupe = row => r => (r.name === row.name && r.date === row.date && r.text === row.text)

    if (alias === "GROUPED_ARTIST_COMMENT")
    {
        let row = make_row(comment)
        if (!all_rows.find(find_dupe(row)))
        {
            all_rows.push(make_row(comment));
            console.log('Parsing MAIN, no children ' + sub_time)
        }
        else
        {
            console.log('Skipping MAIN, found dupe ' + sub_time)
        }

        // update_row(comment, row, false);
        // row.name = comment.getElementsByClassName("PostHeaderView_nickname__6Cb7X")[0].textContent
        // row.date = comment.getElementsByClassName("PostHeaderView_date__XJXBZ")[0].textContent
        // row.text = comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent

        // console.log(date + ' ' + name + ': ' + text)
        // table += '<tr><td>'+ date + '</td><td>'+name+'</td><td>'+text+'</td></tr>';
    }
    else if (alias === "GROUPED_ARTIST_REPLY_COMMENT")
    {
        let child = comment.getElementsByClassName('CommentView_comment_text__tlVgA')[0].children[0].children[0];
        if (child)
        {
            child.click()
            console.log('Expanding reply comment ' + sub_time)
            await new Promise(resolve => setTimeout(resolve, 2000));

            // let origname = ''
            // let origdate = ''
            // let origtext = ''

            let main_index = -1
            let bSkipChild = false;

            let main_reply = document.getElementsByClassName('CommentViewerView_wrap_original_comment__p3f92')[0]
            let main_comment = main_reply.getElementsByClassName("comment_item CommentView_comment_item__pDMEf")[0]
            if (main_comment)
            {
                // let sub_alias = main_comment.getAttribute("data-comment-alias")
                // if (sub_alias === "ORIGINAL_COMMENT" || sub_alias === "ORIGINAL_COMMENT_ARTIST")
                {
                    let r = make_row(main_comment);
                    if (all_rows.find(find_dupe(r)))
                    {
                        bSkipChild = true;
                        console.log(`Skipping MAIN comment! ${r.text}`)
                    }
                    else
                    {
                        main_index = all_rows.push(r) - 1

                        // update_row(sub_comment, row, true)
                        // origname = main_comment.getElementsByClassName("PostHeaderView_nickname__6Cb7X")[0].textContent
                        // origdate = main_comment.getElementsByClassName("PostHeaderView_date__XJXBZ")[0].textContent
                        // origtext = main_comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent

                        console.log(`Parsing MAIN REPLY ${main_index} ${r.text}`)
                    }
                }
            }

            if (!bSkipChild)
            {
                // CommentView_comment_content__P941+ -comment_client_moment
                // CommentView_comment_content__P941+ -comment_client_moment
                let artists_reply_list = document.getElementsByClassName('GroupedArtistCommentListView_artist_group__edcB6')[1]
                let sub_comments = artists_reply_list.getElementsByClassName("comment_item CommentView_comment_item__pDMEf")
                console.log(`Parsing reply comments ${sub_comments.length}`)

                for (let sub_comment of sub_comments)
                {
                    // let sub_time = comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent
                    //
                    let sub_alias = sub_comment.getAttribute("data-comment-alias")
                    console.log(`\t${sub_alias}`)
                    // if (sub_alias === "ORIGINAL_COMMENT" || sub_alias === "ORIGINAL_COMMENT_ARTIST")
                    // {
                    //     console.log('Parsing CHILD original ' + sub_time)
                    //
                    //     all_rows.push(make_row(sub_comment))
                    //
                    //     // update_row(sub_comment, row, true)
                    //     origname = sub_comment.getElementsByClassName("PostHeaderView_nickname__6Cb7X")[0].textContent
                    //     origdate = sub_comment.getElementsByClassName("PostHeaderView_date__XJXBZ")[0].textContent
                    //     origtext = sub_comment.getElementsByClassName("CommentView_comment_text__tlVgA")[0].textContent
                    // }

                    if (sub_alias === "GROUPED_ARTIST_REPLY_COMMENT_LATEST")
                    {
                        let child = sub_comment.getElementsByClassName('CommentView_comment_text__tlVgA')[0].children[0].children[0];
                        child.click()
                        await new Promise(resolve => setTimeout(resolve, 1000));
                    }

                    if (sub_alias === "GROUPED_ARTIST_REPLY_COMMENT" || sub_alias === "GROUPED_ARTIST_REPLY_COMMENT_LATEST")
                    {
                        let row = make_row(sub_comment)
                        row.reply = main_index
                        // row.origname = origname
                        // row.origdate = origdate
                        // row.origtext = origtext
                        all_rows.push(row)

                        console.log(`Parsing CHILD artist reply ${main_index} ${row.text}`)

                        // let row = {}

                        // update_row(sub_comment, row, false)
                    }
                }
            }


            // window.history.back();
            let mything = document.getElementsByClassName('CommentView_container__Yu5S3')[0];
            mything.getElementsByClassName('CommentTitleView_back_button__SX9x7')[0].click();

            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    return Promise.resolve("TEXT")
}

async function get_comments()
{
    comments = document.getElementsByClassName("comment_item CommentView_comment_item__pDMEf")

    for (let comment of comments)
    {
        let alias = comment.getAttribute("data-comment-alias")
        if (alias === "GROUPED_ARTIST_COMMENT_LATEST" || alias === "GROUPED_ARTIST_REPLY_COMMENT_LATEST")
        {
            let child = comment.getElementsByClassName('CommentView_comment_text__tlVgA')[0].children[0].children[0]
            if (child)
            {
                child.click()
            }
            break;
        }
    }

    await new Promise(resolve => setTimeout(resolve, 1000));

    let table = '<table><thead><th>Date</th><th>Name</th><th>Text</th><th>OName</th><th>AName</th><th>BName</th></thead><tbody>';
    for (let comment of comments)
    {
        // console.log(comment);
        let alias = comment.getAttribute("data-comment-alias")
        if (alias === "GROUPED_ARTIST_COMMENT" || alias === "GROUPED_ARTIST_REPLY_COMMENT")
        {
            // let row = {}
            // row.post = root_name
            //
            // console.log('Reading comment for ', row.post)

            await read_comment(comment, alias);

            // let orig_date = row.origdate ? row.origdate : '';
            // let orig_name = row.origname ? row.origname : '';
            // let orig_text = row.origtext ? row.origtext : '';
            // let list = [row.post, row.date, row.name, `\v${row.text}\v`, orig_date, orig_name, `\v${orig_text}\v`];

            // let row_str = list.join('\t');
            // console.log(row_str);
            // all_rows.push(row_str);

            // let new_row = '<tr>';

            // console.log(row.date + ' ' + row.name + ': ' + row.text + orig_date + ': ' + orig_name + ': ' + orig_text);

            // for (let v of list)
            // {
            //     new_row += '<td>' + v + '</td>';
            // }
            // new_row += '</tr>';
            // console.log(new_row);
            // table += row
            // table += '<tr><td>'+ row.date + '</td><td>'+ row.name + '</td><td>' + row.origtext + '</td><td>'+ row.name + '</td><td>' + row.text + '</td><td>'+ row.name + '</td></tr>';
        }
    }

    // let w = window.open("");
    // w.document.write(table);

    // alert("Finished")
    console.log("Finished comments")
    return Promise.resolve("Finished")
}

function save_csv_file(filename, csv_file)
{
    let blob = new Blob([csv_file], { type: 'text/tsv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, filename);
    }
    else
    {
        let link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            let url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

async function get_moment_url(out_url)
{
    for (let i = 0; i < 10; i++)
    {
        let video = document.getElementsByClassName('webplayer-internal-video')[0]
        if (video)
        {
            console.log('fonund video')
            out_url.link = video.getAttribute('src');
            console.log(out_url.link)
            return Promise.resolve('get_moment_url');
        }

        let image = document.getElementsByClassName('OldMomentPostView_moment_photo__99ssq')[0]
        if (image)
        {
            console.log('fonund image')
            // out_url.link = video.getAttribute('src');
        }

        if (!video && !image)
        {
            console.log('waiting...')
            await new Promise(resolve => setTimeout(resolve, 2000));
            continue;
        }

        let style = image.getAttribute('style')
        let regex = /url\("(.+?)"\)/;
        let match = style.match(regex);
        if (match)
        {
            // return match[1].split();
            out_url.link = match[1].split('?').slice(0, -1).join('?') + '?attachment=&cors=weverse.io'
            console.log(out_url.link)
            break;
        }
        else
        {
            alert('regex failed!')
        }

        return Promise.resolve('get_moment_url');
    }
}

function download_thumb(url)
{
    let thumb_name = 'thumb-' + url.split('https://phinf.wevpstatic.net/')[1].split('/')[0]

    url = url.split('?').slice(0, -1).join('?') + '?attachment=&cors=weverse.io'
    console.log('downloading thumb', url)

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
    xhr.onload = function () {
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl =  urlCreator.createObjectURL(this.response);
        var tag = document.createElement('a');
        tag.href = imageUrl;
        tag.target = '_blank';
        tag.download = thumb_name
        document.body.appendChild(tag);
        tag.click();
        document.body.removeChild(tag);
    };
    xhr.send();
}

async function download_all_thumb()
{
    if (true)
    {
        return Promise.resolve("skip");
    }

    console.log('downloading thumbnails');
    let thumbs = new Set()
    for (let r of all_rows)
    {
        console.log(r);
        if (r.thumb != null)
        {
            thumbs.add(r.thumb)
        }
    }

    for (let t of thumbs)
    {
        download_thumb(t);
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    return Promise.resolve("down-thumb");
}

async function downloadImage(out_link)
{
    let test = {}
    await get_moment_url(test)
    console.log('HUH ' + test.link)
    if (!test.link)
    {
        alert('no media found?')
        return;
    }

    let url = test.link

    console.log('downloading ', url)

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
    xhr.onload = function () {
        var urlCreator = window.URL || window.webkitURL;
        var imageUrl = urlCreator.createObjectURL(this.response);
        var tag = document.createElement('a');
        tag.href = imageUrl;
        tag.target = '_blank';
        tag.download = window.location.href.split('/').at(-1);
        document.body.appendChild(tag);
        tag.click();
        document.body.removeChild(tag);
    };
    xhr.send();

    out_link.link = test.link;
    return Promise.resolve("down-image");
}

// downloadImage();

function save_csv()
{
    console.log(all_rows)
    let row_strs = []

    for (let row of post_overview)
    {
        row_strs.push(row.join('\t'))
    }

    for (let row of all_rows)
    {
        // let orig_date = row.origdate ? row.origdate : '';
        // let orig_name = row.origname ? row.origname : '';
        // let orig_text = row.origtext ? row.origtext : '';
        let reply = row.reply != null ? row.reply : '';
        let list = [row.index, row.post, row.date, row.name, `\v${row.text}\v`, reply, row.thumb];
        let row_str = list.join('\t');
        row_strs.push(row_str)
    }

    console.log(row_strs);
    let file_name = do_batch ? 'member' : root_name
    save_csv_file(file_name + '.tsv', row_strs.join('\n'))
}

async function process_moment()
{
    console.log('NEED TO FIX THE CLICK MORE BUTTON BEFORE RUNNING THIS AGAIN')
    return false;

    root_name = window.location.href.split('/').at(-1)
    console.log(root_name)

    let comment = ''
    let main_comment = document.getElementsByClassName('OldMomentPostView_extra_moment_text__lYxs5')
    if (main_comment.length > 0)
    {
        comment = main_comment[0].textContent
    }

    let main_date = document.getElementsByClassName('PostHeaderView_date__XJXBZ')[0].textContent;


    let test = {}
    await downloadImage(test)

    let overview_row = [root_name, main_date, `\v${comment}\v`, test.link];
    console.log('OVERVIEW', overview_row)

    post_overview.push(overview_row)

    await get_comments()

    if (!do_batch)
    {
        console.log('Save CSV?')
        save_csv()
        await download_all_thumb()
    }

    console.log('Finish')
    return Promise.resolve("What")
}

if (do_batch)
{
    down_moment()
}
else
{
    process_moment()
}
