var List = function(kwargs={}) {

    /* перечень объектов в формате: {'uuid': {link:link, char:char, title:title, username:username}, ...} */
    var model = kwargs['model'] || null;
    /* родительский контейнер */
    var container = (kwargs['container']) ? document.getElementById(kwargs['container']) : null;
    /* поле для ввода фильтра*/
    var query = (kwargs['query']) ? document.getElementById(kwargs['query']) : null;

    function render(dataset=null) {
        if (model === null || container === null) return;

        dataset = (dataset === null) ? model : dataset;

        for (let [key, value] of Object.entries(dataset)) {
            let item = document.createElement('a');
            item.href = value['link'];
            item.id = key;
            item.className = 'list__item';

            let char = document.createElement('div');
            char.className = 'list__char';
            char.innerText = value['char'];

            let wrapper = document.createElement('div');
            wrapper.className = 'list__wrapper';

            let title = document.createElement('div');
            title.className = 'list__title';
            title.innerText = value['title'];

            let username = document.createElement('div');
            username.className = 'list__username';
            username.innerText = value['username'];

            wrapper.appendChild(title);
            wrapper.appendChild(username);
            item.appendChild(char);
            item.appendChild(wrapper);
            container.appendChild(item);
        }
    }

    function prepareQuery(line) {
        line = line.toLowerCase();
        line = (line.startsWith('http://')) ? line.slice(7) : line;
        line = (line.startsWith('https://')) ? line.slice(8) : line;
        line = (line.startsWith('www.')) ? line.slice(4) : line;
        line = (line[line.length - 1] == '/') ? line.slice(0, -1) : line;
        return line;
    }

    function filter() {
        if (model === null || query === null) return;

        let search = prepareQuery(query.value);
        container.innerHTML = '';

        for (let [key, value] of Object.entries(model)) {
            if (!value['title'].includes(search)) continue;
            render({[key]: value});
        }
    }

    function events() {
        if (query === null) return;
        query.addEventListener('keyup', filter);
    }

    return {
        render: render,
        events: events,
    }
}
