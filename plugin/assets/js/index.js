// const inputForm = document.getElementById("inputForm");
// const advancedMode = document.getElementById("advancedMode");
// const advancedOptions = document.getElementById("advancedOptions");
// const maxWords = document.getElementById("maxWords");
// const position = document.getElementById("position");
// const additionalInstructions = document.getElementById("additionalInstructions");
// const inputTextArea = document.getElementById("inputTextArea");
// const submitButton = document.getElementById("submitButton");
// const outputArea = document.getElementById("outputArea");

// advancedMode.addEventListener("change", () => {
//     if (advancedMode.checked) {
//         advancedOptions.style.display = "block";
//     } else {
//         advancedOptions.style.display = "none";
//     }
// });

// inputForm.addEventListener("submit", (e) => {
//     e.preventDefault();

//     // Generate cover letter based on input
//     const coverLetter = generateCoverLetter();

//     // Display cover letter in output area
//     outputArea.value = coverLetter;
// });

// function generateCoverLetter() {
//     // Get input values
//     const pdfFile = document.getElementById("pdfFile").value;
//     const maxWordsValue = maxWords.value;
//     const positionValue = position.value;
//     const additionalInstructionsValue = additionalInstructions.value;
//     const inputTextAreaValue = inputTextArea.value;

//     // Generate cover letter based on input values
//     let coverLetter = `PDF File: ${pdfFile}\n`;
//     coverLetter += `Max Words: ${maxWordsValue}\n`;
//     coverLetter += `Position: ${positionValue}\n`;
//     coverLetter += `Additional Instructions: ${additionalInstructionsValue}\n`;
//     coverLetter += `Input Text Area: ${inputTextAreaValue}\n`;

//     return coverLetter;
// }

const realFileBtn = document.getElementById("pdfFile-input");
const customBtn = document.getElementById("pdfFile-btn");
const customTxt = document.getElementById("file-text");
const submitButton = document.getElementById("submitButton");

customBtn.addEventListener("click", function() {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
  if (realFileBtn.value) {
    customTxt.innerHTML = realFileBtn.value.match(
      /[\/\\]([\w\d\s\.\-\(\)]+)$/
    )[1];
  } else {
    customTxt.innerHTML = "No file chosen, yet.";
  }
});




function GenerateCV(){
    const pdfFile = document.getElementById("pdfFile-input").files[0];
    const maxWordsValue = document.getElementById("maxWords").value;
    const positionValue = document.getElementById("position").value;
    const additionalInstructionsValue = document.getElementById(
        "additionalInstructions"
    ).value;
    
    
    const formData = new FormData();
    // formData.append('pdfFile', pdfFile);
    formData.append('maxWords', maxWordsValue);
    formData.append('position', positionValue);
    formData.append('additionalInstructions', additionalInstructionsValue);

    console.log(formData)

    fetch('http://127.0.0.1:8000/CvGen/', {
        method: 'POST',
        body: formData,
        // headers:{
        //     'Access-Control-Allow-Origin': '*',
        //     'Content-Type': 'multipart/form-data'
        // }
 
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error sending POST request:', error);
    });

    
    
}





