let pbufClass = document.location.pathname.slice(1);

function loadFileClicked() {
    $("#input").click();
}

function saveFileClicked() {
    let encodeURL = window.location.pathname + '/encode';
    $.ajax({
        type: 'POST',
        url: encodeURL,
        data: $("#editor textarea").val(),
        contentType: 'text/plain',
        success: receiveEncodedFile,
        dataType: 'json',
    });
}

function handleFileUpload(files) {
    let reader = new FileReader();
    reader.onload = ev => {
        let binaryString = ev.target.result;

        let decodeURL = window.location.pathname + '/decode';

        $.ajax({
            type: 'POST',
            url: decodeURL,
            data: btoa(binaryString),
            contentType: 'text/plain',
            success: receiveDecodedFile,
            dataType: 'json',

        });
    };
    reader.readAsBinaryString(files[0]);
}

function receiveDecodedFile(data) {
    $("#error").text(data.error);
    if (!data.error) {
        $("#editor textarea").val(data.text);
    } else {
        $("#errorOutput").text(data.text);
    }
}

function receiveEncodedFile(data) {
    $("#error").text(data.error);
    if (!!data.error) {
        $("#errorOutput").text(data.text);
        return;
    }

    let filename = $('#saveAs').val() || 'protocolBuffer.data';
    let pbufClass = document.location.pathname.slice(1);

    var blob = b64toBlob(data.data, 'application/protobuf;proto=' + pbufClass);

    var element = document.createElement('a');
    var url = window.URL.createObjectURL(blob);
    element.setAttribute('href', url);
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
}

// https://stackoverflow.com/a/16245768
function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;
  
    var byteCharacters = atob(b64Data);
    var byteArrays = [];
  
    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      var slice = byteCharacters.slice(offset, offset + sliceSize);
  
      var byteNumbers = new Array(slice.length);
      for (var i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
  
      var byteArray = new Uint8Array(byteNumbers);
  
      byteArrays.push(byteArray);
    }
  
    var blob = new Blob(byteArrays, {type: contentType});
    return blob;
  }