class Card extends Pudding {

	constructor() {
		super();
		this.form = document.forms['card'];

		/* delete form*/
		this.form_delete = document.getElementById('card__delete');
		this.form_btnDelete = document.getElementById('card__delete_active');
		this.form_btnCancel = document.getElementById('card__delete_cancel');

		/* text in h1 */
		this.name = document.getElementById('card__name');

		/* model fields */
		this.username = document.getElementById('id_username');
		this.password = document.getElementById('id_password');
		this.notes = document.getElementById('id_notes');
		this.favorite = document.getElementById('id_favorite');

		/* components */
		this.component_clipboard = new Clipboard('card__copypass', this.password.id);
		this.component_password = new ShowPassword('card__showpass', this.password.id);
	}


	/*
	 * array fields: list name fields (<input name='xxx'>), ['user', 'login', ...]
	 */
	decryptFields(fields) {
		let masterkey = this.getMasterKey();
		let self = this;

		fields.forEach(function(item, index, arr) {
			let field = self.form[item];
			
			if (field.value != '') {
				field.value = CryptoJS.AES.decrypt(field.value, masterkey).toString(CryptoJS.enc.Utf8);
			}

			field.removeAttribute('readonly');
		});
	}


	/*
	 * array fields: list name fields (<input name='xxx'>), ['user', 'login', ...]
	 */
	encryptFields(fields) {
		let masterkey = this.getMasterKey();
		let self = this;

		fields.forEach(function(item, index, arr) {
			let field = self.form[item];

			field.setAttribute('readonly', '');
			
			if (field.value != '') {
				field.value = CryptoJS.AES.encrypt(field.value, masterkey).toString();
			}
		});
	}


	/* 
	 * Delete events (show or hide forms) 
	 */
	delete() {
		let self = this;

		this.form_btnDelete.addEventListener('click', function(event) {
			self.form.classList.add('hidden');
			self.form_delete.classList.remove('hidden');
		});

		this.form_btnCancel.addEventListener('click', function(event) {
			self.form_delete.classList.add('hidden');
			self.form.classList.remove('hidden');
		});
	}
}


class Site extends Card {

	constructor() {
		super();

		this.host = document.getElementById('id_host');
		this.uri = document.getElementById('id_uri');

		this.sitecard_uri = document.getElementById('sitecard__uri');
		this.sitecard_scheme = document.getElementById('sitecard__scheme');

		this.fields = ['host', 'uri', 'username', 'password', 'notes']; // for encrypt || decrypt

		this.component_uri = new SiteURI(
			this.sitecard_scheme.id, 
			this.sitecard_uri.id, 
			this.name.id, 
			this.host.id, 
			this.uri.id
		);
	}


	/*
	 * str page = create | update
	 */
	render() {
		this.decryptFields(this.fields);
		this.sitecard_uri.value = this.uri.value;
		this.component_uri.disassemblyURI();
	}


	submit(event) {
		event.preventDefault();
		this.host.maxLength = 1368;
		this.uri.maxLength = 1368;
		this.username.maxLength = 1368;
		this.password.maxLength = 1368;
		this.notes.maxLength = 2668;
		this.encryptFields(this.fields);
		this.form.submit();

	}

	events(page=null) {
		if (page=='update') this.delete();
		this.form.addEventListener('submit', this.submit.bind(this));
	}
}
