
function ref_filter() {

    console.log(true)
    nick_or_token = document.getElementById('nick_or_token');

    if (nick_or_token != null) {
        nick_or_token = nick_or_token.value;
    } else {
        nick_or_token = '';
    };

    if (nick_or_token == '') {
        nick_or_token_key = '';
    } else if (nick_or_token.split('-').length > 3) {
        nick_or_token_key = 'token';
    } else {
        nick_or_token_key = 'nick';
    };

    start = document.getElementById('from').value;
    end = document.getElementById('to').value;
    loc = document.getElementById('loc').value;

    data = {
        'start': start,
        'end': end,
        'nt': nick_or_token,
        'ntk': nick_or_token_key,
        'loc': loc
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/api/ref_filter/');
    xhr.responseType = 'json';
    xhr.setRequestHeader("Accept", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            tbody = document.getElementsByTagName('tbody')[0]
            tbody.innerHTML = ''
            xhr.response.rows.forEach(row => {
                tbody.innerHTML += '<tr><td>'+row.date+'</td><td>'+row.views+'</td><td>'+row.downloads+'</td></tr>'
            });
            tbody.innerHTML += '<tr><th>TOTAL</th><td>'+xhr.response.total.views+'</td><td>'+xhr.response.total.downloads+'</td></tr>'
        }};

    xhr.send(JSON.stringify(data));
};


function open_modal(uid, name) {
    document.getElementById('ModalLabel').innerText = name;
    content = document.getElementById(uid);
    document.getElementsByClassName('modal-body')[0].innerHTML = content.innerHTML;
    document.getElementById('opener').click()
};