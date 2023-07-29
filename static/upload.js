var developerKey = '';
var clientId = '';
var scope = ['https://www.googleapis.com/auth/drive.readonly'];
var pickerApiLoaded = false;
var oauthToken;

function onApiLoad() {
  gapi.load('auth', {'callback': onAuthApiLoad});
  gapi.load('picker', {'callback': onPickerApiLoad});
}

function onAuthApiLoad() {
  window.gapi.auth.authorize(
      {
        'client_id': clientId,
        'scope': scope,
        'immediate': false
      },
      handleAuthResult);
}

function onPickerApiLoad() {
  pickerApiLoaded = true;
  createPicker();
}

function handleAuthResult(authResult) {
  if (authResult && !authResult.error) {
    oauthToken = authResult.access_token;
    createPicker();
  }
}

function createPicker() {
  if (pickerApiLoaded && oauthToken) {
    var picker = new google.picker.PickerBuilder()
        .addView(google.picker.ViewId.DOCS)
        .setOAuthToken(oauthToken)
        .setDeveloperKey(developerKey)
        .setCallback(pickerCallback)
        .build();
    picker.setVisible(true);
  }
}

function pickerCallback(data) {
  if (data.action == google.picker.Action.PICKED) {
    var fileId = data.docs[0].id;
    downloadFile(fileId);
  }
}

function downloadFile(fileId) {
  var request = gapi.client.drive.files.get({
    fileId: fileId,
    alt: 'media'
  });
  request.execute(function(file) {
    console.log('File downloaded:', file);
    // Here you can handle the downloaded file content,
    // you can send it to your server or something.
  });
}