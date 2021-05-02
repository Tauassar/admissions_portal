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

const BACHELOR = 0;
const MASTER = 1;
const PHD = 2;
const DEGREE = {
    'bsc':BACHELOR,
    'msc': MASTER,
    'phd': PHD,
};

const csrftoken = getCookie('csrftoken');
const inputName = document.getElementById("first_name");
const inputSurname = document.getElementById("last_name");
const appDegree = document.getElementById("app_degree");
//files
const diploma = document.getElementById("diploma");
const ieltsCert = document.getElementById("ielts") ;
const toeflCert = document.getElementById("toefl") ;
const gmatgreCert = document.getElementById("gmat-gre") ;
const statPurpose = document.getElementById("purpose") ;
const cv = document.getElementById("cv") ;
const recom1 = document.getElementById("recom-1") ;
const recom2 = document.getElementById("recom-2") ;
//testing
const ieltsScore = document.getElementById("ielts-score") ;
const toeflScore = document.getElementById("toefl-score") ;
const gregmatScore = document.getElementById("toefl-score") ;
//education
const startDate = document.getElementById("start-date") ;
const endDate = document.getElementById("end-date") ;
const gradDate = document.getElementById("grad-date") ;
const comDeg = document.getElementById("com-degree") ;
const inst = document.getElementById("institution") ;
const studField = document.getElementById("study-field") ;
const gpa = document.getElementById("gpa") ;
const startDateAdd = document.getElementById("start-date-add") ;
const endDateAdd = document.getElementById("end-date-add") ;
const gradDateAdd = document.getElementById("grad-date-add") ;
const comDegAdd = document.getElementById("com-degree-add") ;
const instAdd = document.getElementById("institution-add") ;
const studFieldAdd = document.getElementById("study-field-add") ;
const gpaAdd = document.getElementById("gpa-add") ;
const myForm = document.getElementById("myForm");

myForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const request = new Request(
    'http://localhost:1337/api/candidate/',
    {headers: {'X-CSRFToken': csrftoken}}
    );
    let formData = new FormData();
    formData.append("first_name", inputName.value);
    formData.append("last_name", inputSurname.value);
    formData.append("applying degree", appDegree.value);
    formData.append("diploma", diploma.files[0]);
    formData.append("ielts_certificate", ieltsCert.files[0]);
    formData.append("toefl_certificate", toeflCert.files[0]);
    formData.append("gmat_or_gre", gmatgreCert.files[0]);
    formData.append("statement_of_purpose", statPurpose.files[0]);
    formData.append("cv", cv.files[0]);
    formData.append("recomendation_1", recom1.files[0]);
    formData.append("recomendation_2", recom2.files[0]);
    let testing_info = {
        ielts: ieltsScore.value,
        toefl: toeflScore.value,
        gre: gregmatScore.value
    };
    formData.append("testing", JSON.stringify(testing_info));
    let education_info =[
        {
            "start_date":startDate.value,
            "end_date":endDate.value,
            "grad_date":gradDate.value,
            "degree_type":DEGREE[comDeg.value],
            "institution":inst.value,
            "study_field":studField.value,
            "gpa":gpa.value
        }
    ]
    if (startDateAdd.value != '') {
        education_info.push({
            "start_date":startDateAdd.value,
            "end_date":endDateAdd.value,
            "grad_date":gradDateAdd.value,
            "degree_type":DEGREE[comDegAdd.value],
            "institution":instAdd.value,
            "study_field":studFieldAdd.value,
            "gpa":gpaAdd.value
        });
    }
    formData.append("education", JSON.stringify(education_info));

    fetch(request, {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(console.log(formData.entries()))
    .catch(error => console.error('Error:', error))
    .then(
        response =>
        window.location.replace('http://localhost:1337/')
    )
});
