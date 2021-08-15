var SiteCard = function() {

    /* название формы */
    var cardName = (kwargs['cardName']) ? document.getElementById(kwargs['cardName']) : null;

    /* поля не связанные с моделью SiteCard */
    var uri = (kwargs['uri']) ? document.getElementById(kwargs['uri']) : null;
    var scheme = (kwargs['scheme']) ? document.getElementById(kwargs['scheme']) : null;

    /* скрытые input, связанные с моделью SiteCard*/
    var uri_hide = (kwargs['uri_hide']) ? document.getElementById(kwargs['uri_hide']) : null;
    var host = (kwargs['host']) ? document.getElementById(kwargs['host']) : null;


    function determineScheme(line) {
        line = line.toLowerCase();
        let result = null;

        if (line.startsWith('http://')) result = 'http://';
        if (line.startsWith('https://')) result = 'https://';

        return result;
    }

    function showScheme(line) {
        if (line != '') {
            scheme.classList.remove('hidden');
            uri.classList.add('input-right');
        }
        else {
            scheme.classList.add('hidden');
            uri.classList.remove('input-right');
        }
    }

    function validateURI(line) {
        let validator = document.createElement('input');
        validator.setAttribute('type','url');
        validator.setAttribute('maxlength', 254);
        validator.value = line;

        return validator.validity.valid;
    }

    function assemblyURI(obj) {
        let user_password = (obj.username && obj.password) ? obj.username + ':' + obj.password + '@' : '';
        return obj.protocol + '//' + user_password + punycode.toUnicode(obj.hostname) + obj.port + obj.pathname + obj.search + obj.hash;
    }

    function disassemblyURI(e) {
        let data_scheme = determineScheme(uri.value)

        /* если в uri содержится схема, тогда задать полю "схема" ее значение и вырезать ее из поля "uri" */
        if (data_scheme) {
            scheme.innerText = data_scheme;
            uri.value = uri.value.slice(data_scheme.length);
        }

        /* если поле "схема" не пустое, то показать его */
        showScheme(scheme.innerText);


        let data_uri = scheme.innerText + uri.value;

        /* если data_uri валидный, то:
         * установить значение host скрытому полю host,
         * установить значение host заголовку формы,
         * установить нормализированную ссылку в скрытое поле uri (uri_hide)
        */
        if (validateURI(data_uri)) {
            try {
                let url = new URL(data_uri);
                host.value = cardName.innerText = (url.host.startsWith('xn--')) ? punycode.toUnicode(url.host) : url.host;
                uri_hide.value = (url.host.startsWith('xn--')) ? assemblyURI(url) : url.href;
                uri_hide.value = decodeURI(uri_hide.value);
            }
            catch {
                cardName.innerText = '_';
                host.value = uri_hide.value ='';
            }
        }
        else {
            cardName.innerText = '_';
            host.value = uri_hide.value ='';
        }
    }

    function setDefaultScheme(e) {
        let data_scheme = determineScheme(uri.value);

        if (data_scheme === null && scheme.innerText == '') {
            uri.value = 'http://' + uri.value;
        }

        disassemblyURI(e);
    }

    function invertScheme(e) {
        let data_scheme = scheme.innerText;

        if (data_scheme == 'http://') {
            scheme.innerText = 'https://';
            uri_hide.value = (uri_hide.value != '') ? 'https://' + uri_hide.value.slice(7) : '';
        }

        if (data_scheme == 'https://') {
            scheme.innerText = 'http://';
            uri_hide.value = (uri_hide.value != '') ? 'http://' + uri_hide.value.slice(8) : '';
        }
    }

    function pageUpdate() {
        /* функция для страницы update*/
        uri.value = uri_hide.value;
        disassemblyURI();
    }

    function events() {
        uri.addEventListener('keyup', disassemblyURI);
        uri.addEventListener('change', setDefaultScheme);
        scheme.addEventListener('click', invertScheme);
    }

    return {
        events: events,
        page: {update: pageUpdate}
    }
}