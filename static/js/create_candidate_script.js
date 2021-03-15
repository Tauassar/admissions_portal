const inputName = document.getElementById("name");
const inputSurname = document.getElementById("surname");
const appDegree = document.getElementById("app-degree");
const diploma = document.getElementById("diploma");
const ieltsCert = document.getElementById("ielts");
const toeflCert = document.getElementById("toefl");
const gmatgreCert = document.getElementById("gmat-gre");
const statPurpose = document.getElementById("purpose");
const cv = document.getElementById("cv");
const recom1 = document.getElementById("recom-1");
const recom2 = document.getElementById("recom-2");
const ieltsScore = document.getElementById("ielts-score");
const toeflScore = document.getElementById("toefl-score");
const gregmatScore = document.getElementById("toefl-score");
const startDate = document.getElementById("start-date");
const endDate = document.getElementById("end-date");
const gradDate = document.getElementById("grad-date");
const comDeg = document.getElementById("com-degree");
const inst = document.getElementById("institution");
const studField = document.getElementById("study-field");
const gpa = document.getElementById("gpa");
const buttonUpload = document.getElementById("btn-upload");

buttonUpload.addEventListener("click", function() {
    const formData = new FormData();
    formData.append("name", inputName);
    formData.append("surname", inputSurname);
    formData.append("applying degree", appDegree);
    formData.append("diploma", appDegree);
    formData.append("diploma", diploma);
    formData.append("ielts certificate", ieltsCert);
    formData.append("toefl certificate", toeflCert);
    formData.append("gmat/gre certificate", gmatgreCert);
    formData.append("statement of purpose", statPurpose);
    formData.append("cv", cv);
    formData.append("recommendation #1", recom1);
    formData.append("recommendation #2", recom2);
    formData.append("ielts score", ieltsScore);
    formData.append("toefl score", toeflScore);
    formData.append("gre/gmat score", gregmatScore);
    formData.append("start date", startDate);
    formData.append("end date", endDate);
    formData.append("grad date", gradDate);
    formData.append("completed deg", comDeg);
    formData.append("institution", inst);
    formData.append("study field", studField);
    formData.append("gpa", gpa);

    fetch('', {
        method: 'POST',
        body: fd
    })
    .then(res => res.json())
    .then(json => console.log(json))
    .catch(err => console.error(err));
}
);
