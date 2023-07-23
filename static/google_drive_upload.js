// google drive file submissoins handler

document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission
  
    const form = event.target;
    const fileInput = form.querySelector('#file-input');
    const file = fileInput.files[0];
  
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }
  
    // Create a FormData object to send the file to the server
    const formData = new FormData();
    formData.append('file', file);
  
    // Use fetch or an XMLHttpRequest to send the file to the server
    fetch('/upload_google_drive', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Process the response data if needed
        alert('File uploaded to Google Drive successfully!');
        // Optionally, update the UI to reflect the successful upload
      })
      .catch((error) => {
        alert('Error uploading file: ' + error);
        // Optionally, handle errors and display an error message to the user
      });
  });
  