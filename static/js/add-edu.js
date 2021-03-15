

let counter = 0;

function moreFields() {
	counter++;
	let newFields = document.getElementById('readroot').cloneNode(true);
	newFields.id = '';
	newFields.style.display = 'block';
	let newField = newFields.childNodes;
	for (let i=0;i<newField.length;i++) {
		let theName = newField[i].name
		if (theName)
			newField[i].name = theName + counter;
	}
	let insertHere = document.getElementById('writeroot');
	insertHere.parentNode.insertBefore(newFields,insertHere);
}

window.onload = moreFields;