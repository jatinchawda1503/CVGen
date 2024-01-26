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
    customTxt.innerHTML = "No file chosen yet.";
  }
});




function GenerateCV(){
    const pdfFile = document.getElementById("pdfFile-input").files[0];
    const maxWordsValue = document.getElementById("maxWords").value;
    const positionValue = document.getElementById("position").value;
    const additionalInstructionsValue = document.getElementById(
        "additionalInstructions"
    ).value;
    const JD = document.getElementById("JD").value
    
    
    const formData = new FormData();
    formData.append('file', pdfFile);  // Ensure the key matches the expected name on the server side
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





