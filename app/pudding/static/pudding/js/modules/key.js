class Key extends Pudding {

	/*
	 * str form: form name (<form name='xxx'>)
	 * str container: div ID conteinder for render (<div id='container'>)
	 */
	constructor(form, container) {
		super();

		this.form = document.forms[form];
		this.container = document.getElementById(container);
		
		// set in render()
		this.masterkey = null;
		this.errors = null;
	}


	setMasterKey(key, commit=false) {
		key = CryptoJS.SHA3(key, {outputLength: 256}).toString(); // = 32 bytes
		if (commit==true) localStorage.setItem('key', key);
		return key;
	}


	addError(message) {
		let li = document.createElement('li');
		li.innerText = message;
		this.errors.appendChild(li);
	}


	clearErrors() {
		this.errors.innerHTML = '';
	}


	validate() {
		event.preventDefault();
		let key = this.setMasterKey(this.masterkey.value);

		this.clearErrors();

		// Installing the master key for the first time
		if (this.form['cipher'].value == '') {
			this.form['cipher'].value = CryptoJS.AES.encrypt('test', key).toString();
			this.setMasterKey(this.masterkey.value, true);
			this.form.submit();
		}

		let decrypt = CryptoJS.AES.decrypt(this.form['cipher'].value, key).toString(CryptoJS.enc.Utf8);

		// Master key failed test
		if (decrypt != 'test') {
			this.addError('Wrong master key.');
		}

		// Master key test is passed
		if (decrypt == 'test') {
			this.setMasterKey(this.masterkey.value, true);
			this.form.submit();
		}
	}


	events() {
		this.form.addEventListener('submit', this.validate.bind(this));
		this.masterkey.addEventListener('input', this.clearErrors.bind(this));
	}


	render() {
		let label = document.createElement('label');
		label.htmlFor = 'masterkey';
		label.innerText = 'Master Key';

		let input = document.createElement('input');
		input.id = 'masterkey';
		input.name = 'masterkey';
		input.type = 'password';
		input.required = true;
		input.autofocus = true;
		input.setAttribute('autocomplete', 'off');

		let errors = document.createElement('ul');
		errors.id = 'errors'
		errors.classList.add('errorlist');

		this.container.appendChild(label);
		this.container.appendChild(input);
		this.container.appendChild(errors);

		this.masterkey = document.getElementById(input.id);
		this.errors = document.getElementById(errors.id);
	}

}
