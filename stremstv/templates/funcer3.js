

function get_sport(pos, cl) {
    blocks = ['section-linemove-1', 'section-linemove-2', 'section-linemove-3', 'section-linemove-4', 'section-linemove-5']
    if (cl) {
        document.getElementsByTagName('sport')[0].innerText = pos
        block = document.getElementById(blocks[pos])
    } else {
        pos = document.getElementsByTagName('sport')[0].innerText
        block = document.getElementById(blocks[pos])
    };
    $.post(
        '/api/get_events/',
        {p: pos, c:cl, csrfmiddlewaretoken:document.getElementsByTagName('csrf')[0].innerText},
        function (response) {
            response.events.forEach(event => {
                create_or_update(event, block)
            });
        }
    );
};

function create_events(event, block) {
    event_link = document.createElement('a')
    event_link.className = 'event_link'
    event_link.href = '/event/'+event.id+'/'
    if (event.stream == null) {
        stream = '/player/'+event.id+'/'
    } else {
        stream = event.stream
    };
    div = document.createElement('div')
    div.className = 'x-text-center elevation x-bg-lg'
    event_link.append(div)
    div_league = document.createElement('div')
    div_league.className = 'x-color-dg x-pt-2'
    div.append(div_league)
    league = document.createElement('p')
    league.setAttribute('style', 'font-size: 16px;font-weight: 500 !important;color: #fff;')
    league.innerText = event.league
    div_league.append(league)
    if (event.minute != null) {
        time = document.createElement('small')
        time.className = 'event_time'
        time.setAttribute('style', 'position: absolute; right: 4%;')
        time.innerText = event.minute+"'"
        league.append(time)
    };
    div_event = document.createElement('div')
    div_event.setAttribute('style', 'display: flex; justify-content: space-around;')
    div.append(div_event)

    div_home = document.createElement('div')
    div_home.className = 'x-color-black x-hover'
    div_home.setAttribute('style', 'align-items: center;display: flex;flex-direction: column;justify-content: center;flex-basis: 0;flex-grow: 1; margin-top: -3px !important;')
    div_home.innerHTML = '<img src="'+event.home_logo+'" style="width: 40px;">'
    div_event.append(div_home)
    home = document.createElement('div')
    home.className = 'x-py-2'
    home.innerHTML = '<div class="x-pb-3" style="padding: 5px;"></div><span>'+event.home+'</span></div>'
    div_home.append(home)

    div_info = document.createElement('div')
    div_info.setAttribute('style', 'align-items: center;display: flex;flex-direction: column;justify-content: center;')
    div_event.append(div_info)
    div_info2 = document.createElement('div')
    div_info2.className = 'x-font-150 x-color-red'
    div_info.append(div_info2)
    div_info3 = document.createElement('div')
    div_info3.className = 'x-font-bold'
    div_info3.setAttribute('style', 'font-weight: 400 !important;color: white; font-size: 20px;')
    div_info3.innerHTML = '<span class="event_status" style="font-size: 14px; color: #cdcdcd;">'+event.status+'</span><br><span class="event_score">'+event.score+'</span><br>'
    div_info2.append(div_info3)
    div_info2.innerHTML += '<div class="x-font-75"></div>'

    div_away = document.createElement('div')
    div_away.className = 'x-color-black x-hover'
    div_away.setAttribute('style', 'align-items: center;display: flex;flex-direction: column;justify-content: center;flex-basis: 0;flex-grow: 1; margin-top: -3px !important;')
    div_event.append(div_away)
    away_logo = document.createElement('img')
    away_logo.src = event.away_logo
    away_logo.setAttribute('style', 'width: 40px;')
    div_away.append(away_logo)
    away = document.createElement('div')
    away.className = 'x-py-2'
    away.innerHTML = '<div class="x-pb-3" style="padding: 5px;"></div><span>'+event.away+'</span></div>'
    div_away.append(away)
    div.innerHTML += '<div class="x-pb-3"></div><br>'
    elem = document.createElement('div')
    elem.className = 'event_link'
    elem.id = event.id
    elem.append(event_link)
    block.append(elem)
    block.innerHTML += '<div class="x-pb-4" style="background:#f73434;margin-top: -17px;position: relative;height: 20px !important;font-size: 14px;font-weight: 600 !important;border-radius: 0px 0px 8px 8px;color: #fff;">«Фрибет 3000р на этот матч в разделе ставки»</div><br>'
};


function close_modal() {
    document.getElementById('modalNews').hidden = true
};


function update_event(event, element) {
    if (event.stream != null) {
        element.getElementsByClassName('event_link')[0].href = '/event/'+event.id+'/'
    }
    if (event.minute != null) {
        element.getElementsByClassName('event_time')[0].innerText = event.minute+"'"
        element.getElementsByClassName('event_status')[0].innerText = event.status
        element.getElementsByClassName('event_score')[0].innerText = event.score
    }
};

function create_or_update(event, block) {
    element = document.getElementById(event.id)
    if (element == undefined) {
        create_events(event, block)
    } else {
        update_event(event, element)
    };
};