let count = 1;
document.getElementById("button-add")
        .addEventListener("click", function() {
			if(count == 1){
				document.getElementById("candidate-other-add").hidden = false;
				document.getElementById("start-date-add").disabled = false;
				document.getElementById("end-date-add").disabled = false;
				document.getElementById("grad-date-add").disabled = false;
				document.getElementById("com-degree-add").disabled = false;
				document.getElementById("institution-add").disabled = false;
				document.getElementById("study-field-add").disabled = false;
				document.getElementById("gpa-add").disabled = false;
				document.getElementById("button-add").innerHTML = "Remove Education";
				count=2;
			}else{
				document.getElementById("candidate-other-add").hidden = true;
				document.getElementById("start-date-add").disabled = true;
				document.getElementById("end-date-add").disabled = true;
				document.getElementById("grad-date-add").disabled = true;
				document.getElementById("com-degree-add").disabled = true;
				document.getElementById("institution-add").disabled = true;
				document.getElementById("study-field-add").disabled = true;
				document.getElementById("gpa-add").disabled = true;
				document.getElementById("button-add").innerHTML = "Add Education";
				count=1;
			} 
}, false);
// let counter = 0;

// function moreFields() {
// 	counter++;
// 	let newFields = document.getElementById('readroot').cloneNode(true);
// 	newFields.id = '';
// 	newFields.style.display = 'block';
// 	let newField = newFields.childNodes;
// 	for (let i=0;i<newField.length;i++) {
// 		let theName = newField[i].name
// 		if (theName)
// 			newField[i].name = theName + counter;
// 	}
// 	let insertHere = document.getElementById('writeroot');
// 	insertHere.parentNode.insertBefore(newFields,insertHere);
// }

// window.onload = moreFields;