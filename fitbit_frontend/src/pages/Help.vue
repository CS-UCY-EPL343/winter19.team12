<template>
<div class="q-pa-md">

  <q-card class="my-card bg-secondary text-white">
   <q-card-section>
     <div class="text-h6">Frequently Asked Questions</div>
     <div class="text-subtitle2">by Fitbit users</div>
   </q-card-section>
   <q-card-section>
     How do I track my heart rate with my Fitbit device?</br>
     -Track your heart rate day and night with Fitbit's PurePulse technology.</br>
     </br>
     How do I get notifications from my phone on my Fitbit device?</br>
     -Receive call, text message, calendar, and other notifications on your Fitbit watch or tracker if you have a compatible phone.</br>
     </br>
     How do I turn off my Fitbit device?</br>
     -Learn how to turn off your device.</br>
     </br>
     How do I use the Fitbit app to track my period?</br>
     -Track your menstrual cycle to uncover patterns and gain insights.</br>
  </q-card-section>

   <q-separator dark />
 </q-card>

    <q-card class="my-card">
      <q-card-section>
        <div class="text-h6">General Data Protection Regulation (GDPR)</div>
        <div class="text-subtitle2">by Fitbit Developers</div>
      </q-card-section>
      <q-separator />

      <q-card-actions vertical>
        <q-btn flat>Delete Data</q-btn>
        <q-btn flat>Retrive Data</q-btn>
      </q-card-actions>
    </q-card>
</div>
</template>

<script>
export default {
  name: 'Help'
}
</script>
