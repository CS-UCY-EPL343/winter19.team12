import * as messaging from "messaging";
const SERVER_URL = "http://localhost";
messaging.peerSocket.onopen = () => {
  console.log("startt");
  sendMessage();
}

messaging.peerSocket.onerror = (err) => {
  console.log(`Connection error: ${err.code} - ${err.message}`);
}

messaging.peerSocket.onmessage = (evt) => {
  console.log("got metric "+JSON.stringify(evt.data));
  fetch(SERVER_URL).then(function(response) {
      return response.text();
    }).then(function(text) {
      console.log("Got JSON response from server: " + text); });
}

function sendMessage() {
  if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
    // Send the data to peer as a message
    messaging.peerSocket.send({
      sampleData: 123456
    });
  }
}
