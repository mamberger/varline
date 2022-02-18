
let stories = new Zuck('news', {
    backNative: true,
    backButton: true,
    previousTap: true,
    skin: 'snapgram',
    autoFullScreen: false,
    paginationArrows: true,
    avatars: true,
    list: false,
    rtl: false,
    cubeEffect: true,
    openEffect: true,
    localStorage: true,
    callbacks: {
        onView (storyId) {
            viewer = document.getElementsByClassName('viewing')[0].getElementsByClassName('slides')[0].getElementsByClassName('active')[0]
            item = document.getElementById('news-'+storyId)
            js = item.getElementsByTagName('json')[0]
            content = item.getElementsByTagName('content')[0]
            data_now = document.querySelector('div[data-story-id="'+storyId+'"]')
            if (viewer.getElementsByTagName('content')[0] == undefined) {
                viewer.append(content.cloneNode(true))
                logo = JSON.parse(js.innerText).logo
                data_now.getElementsByClassName('profilePhoto')[0].src = logo
                data_now.getElementsByClassName('next')[0].setAttribute('onclick', "next_news(true)")
                data_now.getElementsByClassName('previous')[0].setAttribute('onclick', "next_news(false)")
            };
            $.post('/api/news_view/', {'id': storyId}, function (response) {})
        },
    }
});

news_json = document.getElementsByTagName('json')

for (i=0; i<news_json.length; i++) {
    js = JSON.parse(news_json[i].innerText);
    if (js.video == 'True') {
        story_type = 'video'
    } else {
        story_type = 'photo'
    };
    stories.update({
        id: js.id,
        photo: js.img,
        name: js.title,
        link: "",
        last_update: js.update,
        seen: false,
        items: [{
            id: js.id,
            type: story_type,
            length: js.length,
            src: js.background,
            preview: js.logo,
            link: "",
            linkText: "",
            time: js.update,
            seen: false,
        }]
    });
};


function next_news(is_next) {
    if (is_next == true) {
        stories.next();
    } else {
        stories.previous();
    };
};