import * as messaging from "messaging";
const SERVER_URL = "https://fitbit.eastus.cloudapp.azure.com/insert_metrics";//insert_metrics url
messaging.peerSocket.onopen = () => {
  console.log("startt");
  sendMessage();
}

messaging.peerSocket.onerror = (err) => {
  console.log(`Connection error: ${err.code} - ${err.message}`);
}

messaging.peerSocket.onmessage = (evt) => {
  console.log("got metric "+JSON.stringify(evt.data));
  var dest_url = SERVER_URL+"?type="+evt.data.type+"&value="+evt.data.value;
  console.log(dest_url);
  fetch(dest_url, {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  }).then(function(text) {
      if (text.ok) {
        text.json().then(json => {
          console.log(json);
        });
      }
      console.log("Got JSON response from server: " + JSON.stringify(text)); }
  ).catch(function(err) {
      console.log('ERROR: ' + err)
  });
}

function sendMessage() {
  if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
    // Send the data to peer as a message
    messaging.peerSocket.send({
      sampleData: 123456
    });
  }
}
