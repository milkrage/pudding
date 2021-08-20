class Pudding {

	getMasterKey() {
		let key = localStorage.getItem('key');

		if (key !== null) return key;

		let next = window.location.pathname + window.location.search;
		window.location.replace('/key/?next=' + next);
	}


	/*
	 * Recursive traversal for decryption (CryptoJS)
	 */
	decryptModel(model, recurse=false) {
		let self = this;
		let masterkey = this.getMasterKey();
	

		if (typeof(model) == 'object') {
			Object.keys(model).forEach(function(item, index, arr) {
				if (typeof(model[item]) == 'object') {
					model[item] = self.decryptModel(model[item], true);
				}
				else {
					model[item] = (model[item].startsWith('U2FsdGVkX1')) ? CryptoJS.AES.decrypt(model[item], masterkey).toString(CryptoJS.enc.Utf8) : model[item];
				}
			});
		}

		return model;
	}


	/*
	 * json model: {key: {param1: value, param2: value, ...}, ...}
	 * json query: {'param1': value, 'param2': value, ...}
	 * bool precise: if [true] search rule: ==, [else] search rule: includes()
	 * return: model structure
	 */
	filterModel(model, query, precise=false) {
		let query_keys = Object.keys(query);
		let result = {};

		for (let [key, value] of Object.entries(model)) {
			let match_count = 0;

			query_keys.forEach(function(item, index, arr) {
				if (precise==false) {
					if (model[key][item].includes(query[item])) {
						match_count += 1;
					}
				}

				if (precise==true) {
					if (model[key][item] == query[item]) {
						match_count += 1;
					}
				}
			});

			if (precise==false) {
				if (match_count > 0) {
					result[key] = value;
				}
			}

			if (precise==true) {
				if (match_count == query_keys.length) {
					result[key] = value;
				}
			}
			
		}

		return result;
	}

}
