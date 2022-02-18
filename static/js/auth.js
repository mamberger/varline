function check_password() {
    pass1 = document.getElementsByName('password')[0].value;
    pass2 = document.getElementsByName('password2')[0].value;
    nickname = document.getElementsByName('username')[0].value;
    if (pass2 == pass1 && pass2 != '' && nickname != '') {
        document.getElementById('butreg').disabled = false
    } else {
        document.getElementById('butreg').disabled = true
    };
};

function reform(login) {
    if (login == true) {
        document.getElementsByTagName('h2')[0].innerText = 'Регистрация в партнерский кабинет varline';
        document.getElementById('register').hidden = false;
        document.getElementById('login').hidden = true;
        document.getElementById('reg').hidden = false;
        document.getElementById('log').hidden = true;
    } else {
        document.getElementsByTagName('h2')[0].innerText = 'Вход в партнерский кабинет varline';
        document.getElementById('register').hidden = true;
        document.getElementById('login').hidden = false;
        document.getElementById('reg').hidden = true;
        document.getElementById('log').hidden = false;
    };
};


setInterval(check_password, 1000)