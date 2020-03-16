<template>
  <div>

    <h6 id="head1" class=text-center>This is the list of specialists Accepted:</h6>
    <q-splitter
      v-model="splitterModel"
      style="height: 250px"
    >

      <template v-slot:before>
        <q-tabs
          v-model="tab"
          vertical
          class="text-teal"
        >
          <q-tab  v-for="res in children"  :name="res.label" :icon="res.icon" :label="res.label" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel v-for="res in children" :name="res.label">
            <div class="text-h4 q-mb-md">{{res.label}}</div>
            <p>
              Information about the doctor: {{res.username}}</br>
              My birthdate: {{res.birthday}}</br>
              Gender: {{res.gender}}</br>
              Email address: {{res.email}}</br>
              Contact number: {{res.telephone}}</br>
              My address: {{res.address}}</br>
            </p>
            <q-btn type='submit' id="cancel"  @click='cancel_request()' color="red" :value="res.username" icon="assignment_turned_in" icon-right="cancel" label="Delete Specialist" />
          </q-tab-panel>

        </q-tab-panels>
      </template>
    </q-splitter>


    <h6 id="head1" class=text-center>This is the list of specialists Pending:</h6>
    <q-splitter
      v-model="splitterModel"
      style="height: 250px"
    >

      <template v-slot:before>
        <q-tabs
          v-model="tab2"
          vertical
          class="text-teal"
        >
          <q-tab  v-for="res in children2"  :name="res.label" :icon="res.icon" :label="res.label" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab2"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel v-for="res in children2" :name="res.label">
            <div class="text-h4 q-mb-md">{{res.label}}</div>
            <p>
              Information about the doctor: {{res.username}}</br>
              My birthdate: {{res.birthday}}</br>
              Gender: {{res.gender}}</br>
              Email address: {{res.email}}</br>
              Contact number: {{res.telephone}}</br>
              My address: {{res.address}}</br>
            </p>
            <q-btn type='submit' id="cancel" @click='cancel_request()' color="brown-5" :value="res.username" icon-right="cancel_schedule_send" label="Pending/(Cancel request)" />
          </q-tab-panel>

        </q-tab-panels>
      </template>

    </q-splitter>

    <h6 id="head1" class=text-center>This is the list of remaining specialists:</h6>
    <q-splitter
      v-model="splitterModel"
      style="height: 250px"
    >

      <template v-slot:before>
        <q-tabs
          v-model="tab1"
          vertical
          class="text-teal"
        >
          <q-tab  v-for="res in children1"  :name="res.label" :icon="res.icon" :label="res.label" />
        </q-tabs>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="tab1"
          animated
          swipeable
          vertical
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel v-for="res in children1" :name="res.label">
            <div class="text-h4 q-mb-md">{{res.label}}</div>
            <p>
              Information about the doctor: {{res.username}}</br>
              My birthdate: {{res.birthday}}</br>
              Gender: {{res.gender}}</br>
              Email address: {{res.email}}</br>
              Contact number: {{res.telephone}}</br>
              My address: {{res.address}}</br>
            </p>
            <q-btn type='submit' id="per" ref="permission" @click='send_permission()' color="primary" :value="res.username" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
          </q-tab-panel>

        </q-tab-panels>
      </template>

    </q-splitter>


  </div>
</template>


<script>
import store from 'src/store/index'
import axios from 'axios'
export default {
  data () {
    return {
      splitterModel: 50,
      tab: '',
      tab1:'',
      tab2:'',
      //selected:'',
      children: [],
      children1: [],
      children2: []
    }
  },
  methods: {
    send_permission () {


    let config = {
        headers:{
          'Content-Type': 'application/json',
          Authorization:"Bearer "+store().state.main.token
        }
    }


    let data={
      username: document.getElementById("per").value
    }

      console.log(store().state.main.token);
      this.$axios.post(this.$store.state.main.domain + '/permission_request',data,config).then(response => {
        console.log(response);
        if (response.data.status == '1') {
          this.$q.notify(`Specialist selected successfully!`)
        }
      })
      location.reload();
    },

    cancel_request(){

      let config = {
          headers:{
            'Content-Type': 'application/json',
            Authorization:"Bearer "+store().state.main.token
          }
      }

      let data={
        username: document.getElementById("cancel").value,
        reject: true
      }
      console.log(data);

      this.$axios.post(this.$store.state.main.domain + '/permission_request',data,config).then(response => {
        console.log(response);
        if (response.data.status == '1') {
          this.$q.notify(`Specialist canceled!`)
        }
      })
      location.reload();
    }
  },
  mounted(){

    let config = {
      headers:{
        Authorization:"Bearer "+store().state.main.token
      }
    }

      axios.get(this.$store.state.main.domain + '/permission_request',config).then(response => {
        console.log(response);
        var data = response.data.specialists_sent;
        for (var i=0;i<data.length;i++){
          if(data[i].completed==true){
          var name = data[i].first_name;
          var lastname = data[i].last_name;
          var email = data[i].email;
          var telephone = data[i].telephone;
          var address = data[i].address;
          var gender = data[i].gender;
          var birthday = data[i].birthdate;
          var username = data[i].username;
          this.children.push({ "label":"Dr."+name+" "+lastname, "icon": 'assignment_ind',
          "telephone":telephone,"address":address,"gender":gender,"birthday":birthday,"email":email,"username":username})
        }else{
          var name1 = data[i].first_name;
          var lastname1 = data[i].last_name;
          var email1 = data[i].email;
          var telephone1 = data[i].telephone;
          var address1 = data[i].address;
          var gender1 = data[i].gender;
          var birthday1 = data[i].birthdate;
          var username1 = data[i].username;
          this.children2.push({ "label":"Dr."+name1+" "+lastname1, "icon": 'assignment_ind',
          "telephone":telephone1,"address":address1,"gender":gender1,"birthday":birthday1,"email":email1,"username":username1})
          }
        }
        var data1 = response.data.specialists_not_sent;
        for (var i=0;i<data1.length;i++){
          var name = data1[i].first_name;
          var lastname = data1[i].last_name;
          var email = data1[i].email;
          var telephone = data1[i].telephone;
          var address = data1[i].address;
          var gender = data1[i].gender;
          var birthday = data1[i].birthdate;
          var username = data1[i].username;
          this.children1.push({ "label":"Dr."+name+" "+lastname, "icon": 'assignment_ind',
          "telephone":telephone,"address":address,"gender":gender,"birthday":birthday,"email":email,"username":username})
          console.log(this.children1);
        }
      })
  }
}
</script>

<style>

</style>
