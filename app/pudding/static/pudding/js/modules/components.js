class Clipboard {

	constructor(trigger, field) {
		this.trigger = document.getElementById(trigger);
		this.field = document.getElementById(field);
		this.events();
	}
	

	clipboard() {
		let buffer = document.createElement('textarea');

		buffer.setAttribute('readonly', '');
		buffer.style.position = 'absolute';
		buffer.style.left = '-9999px';
		buffer.value = this.field.value;

		document.body.appendChild(buffer);
		buffer.select();
		document.execCommand('copy');
		buffer.remove();
	}


	events() {
		this.trigger.addEventListener('click', this.clipboard.bind(this));
	}
}


class ShowPassword {

	constructor(trigger, field) {
		this.trigger = document.getElementById(trigger);
		this.field = document.getElementById(field);
		this.events();
	}


	changeType(event) {
		if (event.target.checked) {
			this.field.type = 'text';
		}
		else {
			this.field.type = 'password';
		}
	}


	events() {
		this.trigger.addEventListener('click', this.changeType.bind(this));
	}
}


class SiteURI {

	constructor(scheme, uri, name, model_host, model_uri) {
		this.scheme = document.getElementById(scheme);
		this.uri = document.getElementById(uri);
		this.name = document.getElementById(name);
		this.model_host = document.getElementById(model_host);
		this.model_uri = document.getElementById(model_uri);

		this.events();
	}


	determineScheme(link) {
		link = link.toLowerCase();
		let result = null;

		if (link.startsWith('http://')) result = 'http://';
		if (link.startsWith('https://')) result = 'https://';

		return result
	}


	showScheme() {
		if (this.scheme.innerText != '') {
			this.scheme.classList.remove('hidden');
			this.uri.classList.add('input-right');
		}
		else {
			this.scheme.classList.add('hidden');
			this.uri.classList.remove('input-right');
		}
	}


	validateURI(link) {
		let validator = document.createElement('input');
		validator.setAttribute('type','url');
		validator.setAttribute('maxlength', 254);
		validator.value = link;

		return validator.validity.valid;
	}


	assemblyURI(obj) {
		let user_password = (obj.username && obj.password) ? obj.username + ':' + obj.password + '@' : '';
		return obj.protocol + '//' + user_password + punycode.toUnicode(obj.hostname) + obj.port + obj.pathname + obj.search + obj.hash;
	}


	disassemblyURI() {
		let scheme = this.determineScheme(this.uri.value);

		if (scheme) {
			this.scheme.innerText = scheme;
			this.uri.value = this.uri.value.slice(scheme.length);
		}

		this.showScheme();


		let link = this.scheme.innerText + this.uri.value;

		if (this.validateURI(link)) {
			try {
				let url = new URL(link);

				let host = (url.host.startsWith('xn--')) ? punycode.toUnicode(url.host) : url.host;
				this.model_host.value = this.name.innerText = host;

				this.model_uri.value = (url.host.startsWith('xn--')) ? assemblyURI(url) : url.href;
				this.model_uri.value = decodeURI(this.model_uri.value);
			}
			catch {
				this.name.innerText = '_';
				this.model_host.value = '';
				this.model_uri.value = '';
			}
		}
		else {
			this.name.innerText = '_';
			this.model_host.value = '';
			this.model_uri.value = '';
		}
	}


	setDefaultScheme() {
		let scheme = this.determineScheme(this.uri.value);

		if (scheme === null && this.scheme.innerText == '') {
			this.uri.value = 'http://' + this.uri.value;
		}

		this.disassemblyURI();
	}


	invertScheme() {
		let scheme = this.scheme.innerText

		if (scheme == 'http://') {
			this.scheme.innerText = 'https://';
			this.model_uri.value = (this.model_uri.value != '') ? 'https://' + this.model_uri.value.slice(7) : '';
		}

		if (scheme == 'https://') {
			this.scheme.innerText = 'http://';
			this.model_uri.value = (this.model_uri.value != '') ? 'http://' + this.model_uri.value.slice(8) : '';
		}
	}


	events() {
		this.uri.addEventListener('input', this.disassemblyURI.bind(this));
		this.uri.addEventListener('change', this.setDefaultScheme.bind(this));
		this.scheme.addEventListener('click', this.invertScheme.bind(this));
	}

}
