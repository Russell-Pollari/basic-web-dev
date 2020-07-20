function handleButtonClick() {
	fetch('/submit-json', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			'name': document.getElementById('name').value
		})
	}).then(response => {
		return response.json();
	}).then(result => {
		document.getElementById('reverse-name').innerHTML = result.reversed_name;
	});
}


function handleNameChange(value) {
	console.log(value);
	document.getElementById('show-name').innerHTML = value;
}
