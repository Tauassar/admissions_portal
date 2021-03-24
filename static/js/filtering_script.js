let candContainer = document.getElementsByClassName("candidates");
let textContent = candContainer.getElementsByClassName("status");
let candidate = candContainer.getElementsByClassName("candidate-eval");
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(){
    var current = document.getElementsByClassName("active");
    current[0].className = current[0].className.replace(" active", "");
    this.className += " active";
  });
}
filterSelection("all") // Execute the function and show all columns
function filterSelection(filterParam) {
    for(let i = 0; i < candidate.length; i++) {
        if (textContent.innerText == "Status: In progress") {
            candidate[i].style.display = "";
        } else {
            candidate[i].style.display = "none";
        }
    }
}


// Add active class to the current button (highlight it)
