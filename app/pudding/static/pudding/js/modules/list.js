class List extends Pudding {

	/*
	 * json model: queryset from django model
	 * str container: div ID conteinder for render (<div id='container'>)
	 * str query: input ID with query for filter
	 */
	constructor(model, container, query) {
		super();

		this.model = this.decryptModel(model);
		this.container = document.getElementById(container);
		this.query = document.getElementById(query);
	}


	/*
	 * filter: model format 
	 */
	render(filter=null) {
		let queryset = filter || this.model;

		for (let [key, value] of Object.entries(queryset)) {
			
			let item = document.createElement('a');
            item.href = value['link'];
            item.className = 'list__item';

            let char = document.createElement('div');
            char.className = 'list__char';
            char.innerText = value['title'][0].toUpperCase();

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
            this.container.appendChild(item);
		}
	}


	/* For extends */
	prepareQuery(query) {
		return query;
	}


	filter() {
		let query = this.prepareQuery(this.query.value);
		let filtered = this.filterModel(this.model, {'title': query})

		this.container.innerHTML = '';
		return this.render(filtered);
	}


	events() {
		this.query.addEventListener('input', this.filter.bind(this));
	}
}
