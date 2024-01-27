function pdfParser(typedarray){

    var pdf = pdfjsLib.getDocument(typedarray);
    return pdf.promise.then(function (pdf) {

      // get all pages text
      var maxPages = pdf._transport.pdfDocument.numPages;
      var countPromises = [];
      // collecting all page promises
      for (var j = 1; j <= maxPages; j++) {
        var page = pdf._transport.pdfDocument.getPage(j);

        var txt = "";
        countPromises.push(page.then(function (page) {
          // add page promise
          var textContent = page.getTextContent();

          return textContent.then(function (text) {
            // return content promise
            return text.items.map(function (s) {
              return s.str;
            }).join(''); // value page text
          });
        }));
      }

      // Wait for all pages and join text
      return Promise.all(countPromises).then(function (texts) {
        return texts.join('');
      });
    });
}

function docxParser(setResumeData, file) {
    var reader = new FileReader();
    reader.onload = function (loadEvent) {
        var arrayBuffer = loadEvent.target.result;
        mammoth.extractRawText({ arrayBuffer: arrayBuffer })
            .then(setResumeData)
            .catch(function (error) {
                displayError('Error extracting text from docx file.');
                console.error(error);
            });
    };
    reader.readAsArrayBuffer(file);
}

export {
  pdfParser,
  docxParser
}
