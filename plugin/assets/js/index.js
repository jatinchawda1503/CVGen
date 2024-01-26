const realFileBtn = document.getElementById("pdfFile-input");
const customBtn = document.getElementById("pdfFile-btn");
const customTxt = document.getElementById("file-text");
const submitButton = document.getElementById("submitButton");
const errorContainer = document.getElementById("errorContainer"); // Container to display errors

// Check if a file is stored in localStorage and update the UI accordingly
const storedFileName = localStorage.getItem("storedFileName");

if (storedFileName) {
  customTxt.innerHTML = storedFileName;
}

// chrome.storage.local.get(["filename"]).then((result) => {
//   console.log("Value is " + result.key);
//   customTxt.innerHTML = result.key
// });

customBtn.addEventListener("click", function() {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
  if (realFileBtn.value) {
    const fileName = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    customTxt.innerHTML = fileName;
    // Store the file name in localStorage
    //chrome.storage.local.set({'resume': realFileBtn.files[0]}, function(){})
    //chrome.storage.local.set({'filename': fileName}, function(){})
    // localStorage.setItem("storedFileName", realFileBtn.files[0]);
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


submitButton.addEventListener("click", GenerateCV)

function GenerateCV() {
  // Clear previous errors
  clearErrors();

  // Validate form fields
  const storedPdfFile = localStorage.getItem("storedPdfFile"); // Retrieve stored file from localStorage
  const pdfFile = storedPdfFile ? new Blob([storedPdfFile]) : document.getElementById("pdfFile-input").files[0];
  const maxWordsValue = document.getElementById("maxWords").value;
  const positionValue = document.getElementById("position").value;
  const additionalInstructionsValue = document.getElementById("additionalInstructions").value;
  const JD = document.getElementById("JD").value;

  if (!pdfFile) {
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
  formData.append('file', pdfFile);
  formData.append('position', positionValue);
  formData.append('words', maxWordsValue);
  formData.append('jd', JD);
  formData.append('additional_instructions', additionalInstructionsValue);

  fetch('http://127.0.0.1:8000/CvGen', {
    method: 'POST',
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    console.log('Server response:', data);
  })
  .catch(error => {
    console.error('Error sending POST request:', error);
  });
}
