//   function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// let csrftoken = getCookie('csrftoken');
//     $("#btn-upload").click(function (event) {
//         //stop submit the form, we will post it manually.

        
        
//         event.preventDefault();

//         // Get form
//         let form = $('#myForm')[0];

//         // Create an FormData object 
//         let data = new FormData(form);
//         const ieltsScore = document.getElementById("ielts-score") ;
//         const toeflScore = document.getElementById("toefl-score") ;
//         const gregmatScore = document.getElementById("toefl-score") ;
//         let  testing = {};
//         testing["ielts"] = ieltsScore.value;
//         testing["toefl"] =toeflScore.value;
//         testing["gre"] =gregmatScore.value;
//         console.log( testing);
//         // If you want to add an extra field for the FormData
//         data.append("CustomField", "This is some extra data, testing");
//         data.append("testing", testing);
//         // disabled the submit button
//         $("#btn-upload").prop("disabled", true);
//         console.log(JSON.stringify(data));
//         $.ajax({
//             type: "POST",
//             enctype: 'multipart/form-data',
//             url: "http://127.0.0.1:8000/api/candidate/",
//             headers: { "X-CSRFToken": csrftoken },
//             data: JSON.stringify(data),
//             processData: false,
//             cache: false,
//             timeout: 600000,
//             success: function (data) {

//                 console.log(data);
//                 console.log("SUCCESS : ", data);
//                 $("#btn-upload").prop("disabled", false);

//             },
//             error: function (e) {

//                 console.log(e.responseText);
//                 console.log("ERROR : ", e);
//                 $("#btn-upload").prop("disabled", false);

//             }
//         });

//     });



document.addEventListener('DOMContentLoaded', () => {
    document
      .getElementById('myForm')
      .addEventListener('submit', handleForm);
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrftoken = getCookie('csrftoken');
  function handleForm(ev) {
    ev.preventDefault(); //stop the page reloading
    //console.dir(ev.target);
    let myForm = ev.target;
    let fd = new FormData(myForm);

    //add more things that were not in the form


    //look at all the contents
    // for (let key of fd.keys()) {
    //   console.log(key, fd.get(key));
    // }

    const ieltsScore = document.getElementById("ielts-score") ;
    const toeflScore = document.getElementById("toefl-score") ;
    const gregmatScore = document.getElementById("toefl-score") ;
    let  testing = {};
     testing["ielts"] = ieltsScore.value;
     testing["toefl"] =toeflScore.value;
     testing["gre"] =gregmatScore.value;
    console.log( testing);
    let testingInfoJson = JSON.stringify( testing);
     fd.append('testing',  testing);
    let json = convertFD2JSON(fd);
    console.log(json);
    //send the request with the formdata
    let url = 'http://127.0.0.1:8000/api/candidate/';
    // let h = new Headers();
    // // h.append('Content-type', 'multipart/form-data', 'boundary="gc0pJq0M:08jU534c0p"');
    // h.append('X-CSRFToken', csrftoken);

//     let req = new Request({  
//         url: 'http://127.0.0.1:8000/api/candidate/',
//         method: 'POST',  
//         headers: {  
//           'Content-type': 'multipart/form-data; charset=UTF-8; boundary="gc0pJq0M:08jU534c0p"',
//           'X-CSRFToken': csrftoken
//         },
//         body: json
// });
    //console.log(req);
    fetch(url, {
        method: 'POST',  
        headers: {  
          'Content-type': 'multipart/form-data; charset=UTF-8; boundary="gc0pJq0M:08jU534c0p"',
          "X-CSRFToken": csrftoken 
        },
        body: json
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('Response from server');
        console.log(data);
      })
      .catch(console.warn);
  }

  function convertFD2JSON(formData) {
    let obj = {};
    for (let key of formData.keys()) {
      obj[key] = formData.get(key);
    }
    return JSON.stringify(obj);
  }

  // const csrftoken = getCookie('csrftoken');
// const inputName = document.getElementById("name");
// const inputSurname = document.getElementById("surname");
// const appDegree = document.getElementById("app-degree");
// const diploma = document.getElementById("diploma");
// const ieltsCert = document.getElementById("ielts") ;
// const toeflCert = document.getElementById("toefl") ;
// const gmatgreCert = document.getElementById("gmat-gre") ;
// const statPurpose = document.getElementById("purpose") ;
// const cv = document.getElementById("cv") ;
// const recom1 = document.getElementById("recom-1") ;
// const recom2 = document.getElementById("recom-2") ;
// const ieltsScore = document.getElementById("ielts-score") ;
// const toeflScore = document.getElementById("toefl-score") ;
// const gregmatScore = document.getElementById("toefl-score") ;
// const startDate = document.getElementById("start-date") ;
// const endDate = document.getElementById("end-date") ;
// const gradDate = document.getElementById("grad-date") ;
// const comDeg = document.getElementById("com-degree") ;
// const inst = document.getElementById("institution") ;
// const studField = document.getElementById("study-field") ;
// const gpa = document.getElementById("gpa") ;
// const startDateAdd = document.getElementById("start-date-add") ;
// const endDateAdd = document.getElementById("end-date-add") ;
// const gradDateAdd = document.getElementById("grad-date-add") ;
// const comDegAdd = document.getElementById("com-degree-add") ;
// const instAdd = document.getElementById("institution-add") ;
// const studFieldAdd = document.getElementById("study-field-add") ;
// const gpaAdd = document.getElementById("gpa-add") ;
// const buttonUploadAdd = document.getElementById("btn-upload") ;
// const myForm = document.getElementById("myForm");

// myForm.addEventListener("submit", function(e) {
//     e.preventDefault();
//     let formData = new FormData();
//     formData.append("first_name", inputName.value);
//     formData.append("last_name", inputSurname);
//     formData.append("applying degree", appDegree);
//     formData.append("diploma", diploma.files[0]);
//     formData.append("ielts_certificate", ieltsCert.files[0]);
//     formData.append("toefl_certificate", toeflCert.files[0]);
//     formData.append("gmat_or_gre", gmatgreCert.files[0]);
//     formData.append("statement_of_purpose", statPurpose.files[0]);
//     formData.append("cv", cv.files[0]);
//     formData.append("recomendation_1", recom1.files[0]);
//     formData.append("recomendation_2", recom2.files[0]);
//     formData.append(" testing[ielts]", ieltsScore.value);
//     formData.append(" testing[toefl]", toeflScore.value);
//     formData.append(" testing[gre]", gregmatScore.value);
//     formData.append("education_info[start_date]", startDate.value);
//     formData.append("education_info[end_date]", endDate.value);
//     formData.append("education_info[grad_date]", gradDate.value);
//     formData.append("education_info[degree_type]", comDeg.value);
//     formData.append("education_info[institution]", inst.value);
//     formData.append("education_info[study_field]", studField.value);
//     formData.append("education_info[gpa]", gpa.value);
//     formData.append("start date additional", startDateAdd);
//     formData.append("end date additional", endDateAdd);
//     formData.append("grad date additional", gradDateAdd);
//     formData.append("completed deg additional", comDegAdd);
//     formData.append("institution additional", instAdd);
//     formData.append("study field additional", studFieldAdd);
//     formData.append("gpa additional", gpaAdd);
//     const request = new Request(
//         'http://127.0.0.1:8000/api/candidate/',
//         {headers: {'X-CSRFToken': csrftoken}}
//     );
// fetch(request, {
//   method: 'POST',
//   body: formData
// })
// .then(response => response.json())
// .then(console.log(formData.getAll()))
// .catch(error => console.error('Error:', error))
// .then(
//     response =>
//     console.log('Success:', JSON.stringify(response)))
// }
// );
