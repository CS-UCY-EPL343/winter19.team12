/*
Fitbit Monitoring is a free software that helps you interact with your 
Fitbit device and keep track of all your daily activity.
Copyright (C) 2020  Christodoulos Constantinides, Kristian Litsis, Paris Constantinides, Giannis Alexandrou, Leonidas Vokos
	
Fitbit Monitoring System is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fitbit Monitoring System is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
import { Accelerometer } from "accelerometer";
import { Barometer } from "barometer";
import { BodyPresenceSensor } from "body-presence";
import { display } from "display";
import document from "document";
import { Gyroscope } from "gyroscope";
import { HeartRateSensor } from "heart-rate";
import { OrientationSensor } from "orientation";
import { me as appbit} from "appbit";
import { today } from "user-activity";
import * as messaging from "messaging";

import { me as appbit } from "appbit";
import { dayHistory } from "user-activity";

console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_heart_rate")){
  const dayRecordsAverageHeartRate = dayHistory.query();
  dayRecordsAverageHeartRate.forEach((day,index) => {
    console.log(`${day.averageHeartRate || 0} averageHeartRate. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_activity")){
  const dayRecordsSteps = dayHistory.query();
  dayRecordsSteps.forEach((day,index) => {
    console.log(`${day.steps || 0} steps. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
 if(appbit.permissions.granted("access_activity")){
  const dayRecordsCalories = dayHistory.query();
  dayRecordsCalories.forEach((day,index) => {
    console.log(`${day.calories || 0} calories. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_activity")){
  const dayRecordsActiveMinutes = dayHistory.query();
  dayRecordsActiveMinutes.forEach((day,index) => {
    console.log(`${day.activeMinutes || 0} activeMinutes. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_activity")){
  const dayRecordsDistance = dayHistory.query();
  dayRecordsDistance.forEach((day,index) => {
    console.log(`${day.distance || 0} distance. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_activity")){
  const dayRecordsElevationGain = dayHistory.query();
  dayRecordsElevationGain.forEach((day,index) => {
    console.log(`${day.elevationGain || 0} elevationGain. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
if(appbit.permissions.granted("access_heart_rate")){
  const dayRecordsRestingHeartRate = dayHistory.query();
  dayRecordsRestingHeartRate.forEach((day,index) => {
    console.log(`${day.restingHeartRate || 0} restingHeartRate. ${index + 1} day(s) ago.`);
  });
}
console.log("------------------------------------------------------------------");
//Trying to find a way to get user-id ot even specific device-id but not model
/*
console.log("------------------------------------------------------------------");
import { me as device } from "device";
console.log("ID that I get, supposing it's the model so always static: " + device.modelId);
import { me } from "appbit";
console.log("Application ID:" + me.applicationId);
console.log("Build ID:" + me.buildId);
import { user } from "user-profile";
console.log("------------------------------------------------------------------");
console.log("User's age:" + user.age);
console.log("User's bmr:" + user.bmr);
console.log("User's gender:" + user.gender);
console.log("User's height:" + user.height);
console.log("User's restingHeartRate:" + user.restingHeartRate);
console.log("User's weight:" + user.weight);
console.log("Maybe we can create a id with all the data: " + user.age+user.bmr+user.gender+user.height+user.restingHeartRate+user.weight);
console.log("------------------------------------------------------------------");
*/

messaging.peerSocket.onopen = function() {
  // Ready to send messages
  //sendMessage();
}
messaging.peerSocket.onerror = function(err) {
  // Handle any errors
  console.log("Connection error: " + err.code + " - " + err.message);
}
function sendMessage(msg) {
  if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
    // Send the data to peer as a message
    messaging.peerSocket.send(msg);
  }
}

const accelLabel = document.getElementById("accel-label");
const accelData = document.getElementById("accel-data");

const stepsLabel = document.getElementById("steps-label");
const stepsData = document.getElementById("steps-data");

const caloriesLabel = document.getElementById("calories-label");
const caloriesData = document.getElementById("calories-data");

const activeMinutesLabel = document.getElementById("activeMinutes-label");
const activeMinutesData = document.getElementById("activeMinutes-data");

const distanceLabel = document.getElementById("distance-label");
const distanceData = document.getElementById("distance-data");

const elevationGainLabel = document.getElementById("elevationGain-label");
const elevationGainData = document.getElementById("elevationGain-data");

const barLabel = document.getElementById("bar-label");
const barData = document.getElementById("bar-data");

const bpsLabel = document.getElementById("bps-label");
const bpsData = document.getElementById("bps-data");

const gyroLabel = document.getElementById("gyro-label");
const gyroData = document.getElementById("gyro-data");

const hrmLabel = document.getElementById("hrm-label");
const hrmData = document.getElementById("hrm-data");

const orientationLabel = document.getElementById("orientation-label");
const orientationData = document.getElementById("orientation-data");

const sensors = [];

if(appbit.permissions.granted("access_activity")){
  console.log(`${today.adjusted.steps} Steps`);
  const steps = new Barometer({ frequency: 0.5 });
  steps.addEventListener("reading", () => {
        stepsData.text = JSON.stringify({
        steps: today.adjusted.steps
      });
      sendMessage({
        'type':'steps',
        'steps': today.adjusted.steps
      })
  });
  sensors.push(steps);
  steps.start();
} else {
  stepsLabel.style.display = "none";
  stepsLabel.style.display = "none";
  console.log(`No steps metrics were recorded`);
}


if (today.local.calories != undefined) {
  console.log(`${today.adjusted.calories} Calories`);
  const calories = new Barometer({ frequency: 0.5 });
    calories.addEventListener("reading", () => {
          caloriesData.text = JSON.stringify({
          calories: today.adjusted.calories
        });
        sendMessage({
          'type':'calories',
          'calories': today.adjusted.calories
        })
    });
    sensors.push(calories);
    calories.start();
} else {
  caloriesLabel.style.display = "none";
  caloriesLabel.style.display = "none";
  console.log(`No calories metrics were recorded`);
}
  
if (today.local.activeMinutes != undefined) {
   console.log(`${today.adjusted.activeMinutes} Active Minutes`);
   const activeMinutes = new Barometer({ frequency: 0.5 });
    activeMinutes.addEventListener("reading", () => {
          activeMinutesData.text = JSON.stringify({
          activeMinutes: today.adjusted.activeMinutes
        });
        sendMessage({
          'type':'activeMinutes',
          'activeMinutes': today.adjusted.activeMinutes
        })
    });
    sensors.push(activeMinutes);
    activeMinutes.start();
} else {
  activeMinutesLabel.style.display = "none";
  activeMinutesLabel.style.display = "none";
  console.log(`No activeMinutes metrics were recorded`);
}


if (today.local.distance != undefined) {
   console.log(`${today.adjusted.distance} Distance`);
   const distance = new Barometer({ frequency: 0.5 });
    distance.addEventListener("reading", () => {
          distanceData.text = JSON.stringify({
          distance: today.adjusted.distance
        });
        sendMessage({
          'type':'distance',
          'distance': today.adjusted.distance
        })
    });
    sensors.push(distance);
    distance.start();
} else {
  distanceLabel.style.display = "none";
  distanceLabel.style.display = "none";
  console.log(`No distance metrics were recorded`);
}

if (today.local.elevationGain != undefined) {
  console.log(`${today.adjusted.elevationGain} Elevation Gain`);
  const elevationGain = new Barometer({ frequency: 0.5 });
    elevationGain.addEventListener("reading", () => {
          elevationGainData.text = JSON.stringify({
          elevationGain: today.adjusted.elevationGain
        });
        sendMessage({
          'type':'elevationGain',
          'elevationGain': today.adjusted.elevationGain
        })
    });
    sensors.push(elevationGain);
    elevationGain.start();
} else {
  elevationGainLabel.style.display = "none";
  elevationGainLabel.style.display = "none";
  console.log(`No elevationGain metrics were recorded`);
}


if (Accelerometer) {
  const accel = new Accelerometer({ frequency: 0.5 });
  accel.addEventListener("reading", () => {
    accelData.text = JSON.stringify({
      x: accel.x ? accel.x.toFixed(1) : 0,
      y: accel.y ? accel.y.toFixed(1) : 0,
      z: accel.z ? accel.z.toFixed(1) : 0
    });
    sendMessage({
      'type':'accel',
      'x':accel.x,
      'y':accel.y,
      'z':accel.z
    })
  });
  sensors.push(accel);
  accel.start();
} else {
  accelLabel.style.display = "none";
  accelData.style.display = "none";
}

if (Barometer) {
  const barometer = new Barometer({ frequency: 0.5 });
  barometer.addEventListener("reading", () => {
    barData.text = JSON.stringify({
      pressure: barometer.pressure ? parseInt(barometer.pressure) : 0
    });
  });
  sensors.push(barometer);
  barometer.start();
} else {
  barLabel.style.display = "none";
  barData.style.display = "none";
}

if (BodyPresenceSensor) {
  const bps = new BodyPresenceSensor();
  bps.addEventListener("reading", () => {
    bpsData.text = JSON.stringify({
      presence: bps.present
    })
  });
  sensors.push(bps);
  bps.start();
} else {
  bpsLabel.style.display = "none";
  bpsData.style.display = "none";
}

if (Gyroscope) {
  const gyro = new Gyroscope({ frequency: 0.5 });
  gyro.addEventListener("reading", () => {
    gyroData.text = JSON.stringify({
      x: gyro.x ? gyro.x.toFixed(1) : 0,
      y: gyro.y ? gyro.y.toFixed(1) : 0,
      z: gyro.z ? gyro.z.toFixed(1) : 0,
    });
  });
  sensors.push(gyro);
  gyro.start();
} else {
  gyroLabel.style.display = "none";
  gyroData.style.display = "none";
}

if (HeartRateSensor) {
  const hrm = new HeartRateSensor({ frequency: 0.5 });
  hrm.addEventListener("reading", () => {
    hrmData.text = JSON.stringify({
      heartRate: hrm.heartRate ? hrm.heartRate : 0
    });
    sendMessage({
      'type':'heart',
      'value':hrm.heartRate
    });
  });
  sensors.push(hrm);
  
  hrm.start();
} else {
  hrmLabel.style.display = "none";
  hrmData.style.display = "none";
}

if (OrientationSensor) {
  const orientation = new OrientationSensor({ frequency: 0.5 });
  orientation.addEventListener("reading", () => {
    orientationData.text = JSON.stringify({
      quaternion: orientation.quaternion ? orientation.quaternion.map(n => n.toFixed(1)) : null
    });
  });
  sensors.push(orientation);
  orientation.start();
} else {
  orientationLabel.style.display = "none";
  orientationData.style.display = "none";
}

display.addEventListener("change", () => {
  // Automatically stop all sensors when the screen is off to conserve battery
  display.on ? sensors.map(sensor => sensor.start()) : sensors.map(sensor => sensor.stop());
});
