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
import { HeartRateSensor } from "heart-rate";

import { me as appbit } from "appbit";
import { minuteHistory, dayHistory } from "user-activity";
import userActivity from "user-activity";

//console.log("Minute history metrics are undefined and the reason is explained: https://dev.fitbit.com/blog/2019-10-29-announcing-fitbit-os-sdk-4.0/");
//console.log("AverageHeartRate and active minutes are undefined and the reason is explained: https://community.fitbit.com/t5/SDK-Development/Interface-ActivityHistoryRecord-Example/td-p/3991847");

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
if (HeartRateSensor) {
   const hrm = new HeartRateSensor({ frequency: 0.5 });
   hrm.addEventListener("reading", () => {
     console.log(`Current heart rate: ${hrm.heartRate}`);
   });
   hrm.start();
   const maxHeartRate=200;
  if (hrm.heartRate<((60/100)*maxHeartRate)) {
    console.log(`Very light exercise or not at all.`);
  }
  else if (hrm.heartRate>((60/100)*maxHeartRate) && hrm.heartRate<((70/100)*maxHeartRate) ) {
    console.log(`Light exercise.`);
  }
  else if (hrm.heartRate>((70/100)*maxHeartRate) && hrm.heartRate<((80/100)*maxHeartRate) ) {
    console.log(`Moderate exercise.`);
  }
  else if (hrm.heartRate>((80/100)*maxHeartRate) && hrm.heartRate<((90/100)*maxHeartRate) ) {
    console.log(`Hard exercise.`);
  }
  else if (hrm.heartRate>((90/100)*maxHeartRate) && hrm.heartRate<((100/100)*maxHeartRate) ) {
    console.log(`Extreme exercise.`);
  }
} else {
   console.log("This device does NOT have a HeartRateSensor!");
}
if(appbit.permissions.granted("access_activity")){
  console.log(`${today.adjusted.steps} Steps`);
  const steps = new Barometer({ frequency: 0.5 });
  steps.addEventListener("reading", () => {
        stepsData.text = JSON.stringify({
        steps: today.adjusted.steps
      });
      sendMessage({
        'type':'steps',
        'value': today.adjusted.steps
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
          'value': today.adjusted.calories
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
          'value': today.adjusted.activeMinutes
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
          'value': today.adjusted.distance
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
          'value': today.adjusted.elevationGain
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
