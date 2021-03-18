function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
document.addEventListener('DOMContentLoaded', () => {
    document
      .getElementById('myForm')
      .addEventListener('submit', handleForm);
  });

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
    let testing_info = {};
    testing_info["ielts"] = ieltsScore.value;
    testing_info["toefl"] =toeflScore.value;
    testing_info["gre"] =gregmatScore.value;
    console.log(testing_info);
    let testingInfoJson = JSON.stringify(testing_info);
     fd.append('testing_info', testing_info);
    let json = convertFD2JSON(fd);
    console.log(json);
    //send the request with the formdata
    let url = 'http://127.0.0.1:8000/api/candidate/';
    let h = new Headers();
    h.append('Content-type', 'application/json');
    h.append('X-CSRFToken', csrftoken);

    let req = new Request(url, {
      headers: h,
      body: json,
      method: 'POST',
    });
    //console.log(req);
    fetch(req)
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
//     formData.append("testing_info[ielts]", ieltsScore.value);
//     formData.append("testing_info[toefl]", toeflScore.value);
//     formData.append("testing_info[gre]", gregmatScore.value);
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
