var Card = function(kwargs={}) {

    /* поле с паролем */
    var password = (kwargs['password']) ? document.getElementById(kwargs['password']) : null;
    /* кнопка для копирования пароля */
    var btnCopyPassword = (kwargs['btnCopyPassword']) ? document.getElementById(kwargs['btnCopyPassword']) : null;
    /* ceckbox "показать пароль" */
    var checkShowPassword = (kwargs['checkShowPassword']) ? document.getElementById(kwargs['checkShowPassword']) : null;

    function copyPassword(e) {
        if (password === null) return;

        let buffer = document.createElement('textarea');

        buffer.setAttribute('readonly', '');
        buffer.style.position = 'absolute';
        buffer.style.left = '-9999px';
        buffer.value = password.value;

        document.body.appendChild(buffer);
        buffer.select();
        document.execCommand('copy');
        buffer.remove();
    }

    function showPassword(e) {
        if (e.target.checked) {
            password.type = 'text';
        }
        else {
            password.type = 'password';
        }
    }

    function eventsUpdatePage(kwargs={}) {
        var btnDelete = document.getElementById(kwargs['btnDelete']);
        var btnCancel = document.getElementById(kwargs['btnCancel']);

        var formCard = document.getElementById(kwargs['formCard']);
        var formDelete = document.getElementById(kwargs['formDelete']);

        btnDelete.addEventListener('click', function() {
            formCard.classList.add('hidden');
            formDelete.classList.remove('hidden');
        });

        btnCancel.addEventListener('click', function() {
            formCard.classList.remove('hidden');
            formDelete.classList.add('hidden');
        });
    }

    function events() {
        if (btnCopyPassword === null || checkShowPassword === null) return;
        btnCopyPassword.addEventListener('click', copyPassword);
        checkShowPassword.addEventListener('click', showPassword);
    }

    return {
        events: events,
        eventsUpdatePage: eventsUpdatePage
    }
}