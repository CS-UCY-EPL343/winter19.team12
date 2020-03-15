<template>
  <div>
    <h6 id="head1" class=text-center>This is the list of our specialists:</h6>
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
            <q-btn type='submit' id="per" ref="permission" @click='send_permission()' color="red" :value="res.username" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
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
      //selected:'',
      children: [
      ]
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
    }
  },
  mounted(){

    let config = {
      headers:{
        Authorization:"Bearer "+store().state.main.token
      }
    }

      axios.get(this.$store.state.main.domain + '/get_specialist',config).then(response => {
        //console.log(response);
        var data = response.data.docs;
        for (var i=0;i<data.length;i++){
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
          console.log(this.children);
        }
      })
  }
}
</script>

<style>

</style>
