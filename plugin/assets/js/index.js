import { pdfParser,docxParser } from "./parser.js";


const realFileBtn = document.getElementById("pdfFile-input");
const customBtn = document.getElementById("pdfFile-btn");
const customTxt = document.getElementById("file-text");
const submitButton = document.getElementById("submitButton");
const errorContainer = document.getElementById("errorContainer"); // Container to display errors
const outputArea = document.getElementById("outputArea"); // Container to display output

var resumeData = "";
var resumeFilename = "";

chrome.storage.local.get(['filename', 'resume'], function(result) {
    if (result['filename'] !== undefined) {
        customTxt.innerHTML = result['filename'];
        resumeFilename = result['filename'];
    } else {
        customTxt.innerHTML = "No file chosen yet";
    }

    if (result['resume'] !== undefined) {
        resumeData = result['resume'];
    }
});


function extractContent(file){
    var ext = file.name.split('.').pop();
    if(ext=="pdf"){
      var fileReader = new FileReader();
      fileReader.onload = function () {
        var typedarray = new Uint8Array(this.result);
        pdfParser(typedarray).then(function (text) {
          resumeData = text;
        }, function (reason)
          {
            displayError('Seems this file is broken, please upload another file');
          });
      };
      fileReader.readAsArrayBuffer(file);
    }else if(ext=="docx"){
        function setResumeData(result) {
            var text = result.value;
            resumeData = text;
            console.log(resumeData)
        }
        docxParser(setResumeData, file);
    }
    else{
        displayError("Please upload a pdf or docx file");
    }
}

customBtn.addEventListener("click", function() {
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
    if (realFileBtn.value) {
        console.log(realFileBtn.value)
        const fileName = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
        customTxt.innerHTML = fileName;
        extractContent(realFileBtn.files[0])
        chrome.storage.local.set({'resume': resumeData}, function() {});
        chrome.storage.local.set({'filename': fileName}, function() {});
        
    } else {
        customTxt.innerHTML = "No file chosen yet.";
    }
});

function displayError(message) {
    errorContainer.innerHTML = `<div class="alert alert-danger" role="alert">${message}</div>`;
}

function clearErrors() {
    errorContainer.innerHTML = '';
}

submitButton.addEventListener("click", GenerateCV);

async function GenerateCV() {
    clearErrors();
    outputArea.innerHTML = '';
    outputArea.style.display = "none";
    submitButton.disabled = true;
   
    const maxWordsValue = document.getElementById("maxWords").value;
    const positionValue = document.getElementById("position").value;
    const additionalInstructionsValue = document.getElementById("additionalInstructions").value;
    const JD = document.getElementById("JD").value;
    

    if (!resumeData && !realFileBtn.files[0]) {
        displayError("Please upload a resume (PDF file).");
        return;
    }

    if (!maxWordsValue) {
        displayError("Please enter the maximum words.");
        return;
    }

    if (!positionValue) {
        displayError("Please enter the position.");
        return;
    }

    // Add additional validation for other fields as needed

    const formData = new FormData();
    
    if (resumeData != undefined || resumeData != null || resumeData != "") {
        formData.append('resume', resumeData);
    } 
    formData.append('position', positionValue);
    formData.append('words', maxWordsValue);
    formData.append('jd', JD);
    formData.append('additional_instructions', additionalInstructionsValue);

    var response = await fetch('http://127.0.0.1:8000/CvGen/', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'multipart/form-data'
        }
    }).then(
        function(response){
            var reader = response.body.getReader();
            var decoder = new TextDecoder('utf-8');
            reader.read().then(function processResult(result) {
                if (result.done) return;
                outputArea.style.display = "block";
                outputArea.scrollIntoView({behavior: "smooth", block: "start", inline: "start"});
                let token = decoder.decode(result.value);
                outputArea.innerHTML += token;
                return reader.read().then(processResult);
            });
            submitButton.disabled = false;
        }
    )

    
}
