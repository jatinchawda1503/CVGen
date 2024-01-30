import { pdfParser,docxParser } from "./parser.js";


const realFileBtn = document.getElementById("pdfFile-input");
const customBtn = document.getElementById("pdfFile-btn");
const customTxt = document.getElementById("file-text");
const submitButton = document.getElementById("submitButton");
const errorContainer = document.getElementById("errorContainer"); 
const outputArea = document.getElementById("outputArea"); 
const OutputSection = document.getElementById("OutputSection"); 
const RadioArea = document.getElementById("RadioArea")
const detectByUrlRadio = document.getElementById('detectByUrl');
const enterManuallyRadio = document.getElementById('enterManually');
const urlInput = document.getElementById('urlInput');
const manualEntry = document.getElementById('manualEntry');
const JDUrl = document.getElementById('JDUrl');
const JDManual = document.getElementById('JDManual');


var resumeData = "";
var resumeFilename = "";
var dataURL = '';


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

detectByUrlRadio.addEventListener('change', function() {
    urlInput.style.display = 'block';
    manualEntry.style.display = 'none';
});

enterManuallyRadio.addEventListener('change', function() {
    urlInput.style.display = 'none';
    manualEntry.style.display = 'block';
});

async function getCurrentTabAPI() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    let url = tab.url;
    if (isLinkedInJobUrl(url)) {
        const jobId = extractJobIdFromUrl(url);
        if (jobId) {
            const newUrl = `https://www.linkedin.com/jobs/view/${jobId}`;
            dataURL = newUrl;
            JDUrl.value = dataURL;
            console.log("New LinkedIn Job URL:", newUrl);
        } else {
            displayError("Cannot extract jobId from the URL.");
        }
    } else {
        dataURL = tab.url;
        JDUrl.value = dataURL;
    }
    
  }
  
  function isLinkedInJobUrl(url) {
    // Define the regex pattern for LinkedIn job URLs
    const linkedInJobUrlPattern = /^https:\/\/www\.linkedin\.com\/jobs\/(view\/\d+|search\/\?currentJobId=\d+)/;

    // Test if the URL matches the pattern
    if (linkedInJobUrlPattern.test(url)) {
        return true;
    }

    // Additional check for general LinkedIn URLs
    const linkedInGeneralUrlPattern = /^https:\/\/www\.linkedin\.com\//;
    if (linkedInGeneralUrlPattern.test(url)) {
        displayError("Cannot extract jobId from the URL. Please open a LinkedIn job posting URL.");
        return false;
    }

    return false;
}


function extractJobIdFromUrl(url) {
    // Extract jobId from the URL
    const match = url.match(/(?:view\/|currentJobId=)(\d+)/);

    // If a match is found, return the jobId
    if (match && match[1]) {
        return match[1];
    }

    return null;
}



submitButton.addEventListener("click", GenerateCV);

async function GenerateCV() {
    clearErrors();
    OutputSection.style.display = "none";
    outputArea.innerHTML = '';
    submitButton.disabled = true;
   
    const maxWordsValue = document.getElementById("maxWords").value;
    const positionValue = document.getElementById("position").value;
    const additionalInstructionsValue = document.getElementById("additionalInstructions").value;
    const Radiovalue = document.querySelector('input[name="JDOption"]:checked').value;
    let JD

    if (Radiovalue == "detectByUrl") {
        JD = JDUrl.value;
    } else if (Radiovalue == "enterManually") {
        JD = JDManual.value;
    }

    if (!resumeData && !realFileBtn.files[0]) {
        displayError("Please upload a resume (PDF file).");
        return;
    }

    if (!maxWordsValue && !isNaN(maxWordsValue)) {
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
    formData.append("option", Radiovalue)
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
                OutputSection.style.display = "block";
                OutputSection.scrollIntoView({behavior: "smooth", duration: 1000});
                let token = decoder.decode(result.value);
                outputArea.innerHTML += token.replace(/\n/g, '<br>');
                return reader.read().then(processResult);
            })
        }).finally(()=>{
        submitButton.disabled = false;
    })
}

document.addEventListener('DOMContentLoaded', function() {
    new ClipboardJS('.btn-clipbord');
    getCurrentTabAPI();
})

