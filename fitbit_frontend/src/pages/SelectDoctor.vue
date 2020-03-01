<!-- <template>
  <div>
    <q-splitter
      v-model="splitterModel"
      style="height: 400px"
    >

      <template v-slot:before>
        <h6 id="head1">This is the list of our specialists:</h6>
        <div class="q-pa-md">
          <q-tree
            :nodes="children"
            node-key="label"
            selected-color="primary"
            :selected.sync="selected"
            default-expand-all
          />
        </div>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="selected"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >

          <q-tab-panel v-ripple v-for="res in children" :name="res.label" >
            <div class="text-h4 q-mb-md">{{res.label}}</div>
            <p>
              Information about the doctor</br>
              My birtdate: {{res.birthday}}</br>
              Gender: {{res.gender}}</br>
              Email address: {{res.email}}</br>
              Contact number: {{res.telephone}}</br>
              My address: {{res.address}}</br>
            </p>
            <q-btn color="red" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
          </q-tab-panel>
        </q-tab-panels>

      </template>
    </q-splitter>
  </div>
</template> -->




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
              Information about the doctor</br>
              My birtdate: {{res.birthday}}</br>
              Gender: {{res.gender}}</br>
              Email address: {{res.email}}</br>
              Contact number: {{res.telephone}}</br>
              My address: {{res.address}}</br>
            </p>
            <q-btn color="red" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
          </q-tab-panel>

        </q-tab-panels>
      </template>

    </q-splitter>
  </div>
</template>


<script>
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
  mounted(){

      axios.get(this.$store.state.main.domain + '/get_specialist').then(response => {
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
          this.children.push({ "label":"Dr."+name+" "+lastname, "icon": 'assignment_ind',
          "telephone":telephone,"address":address,"gender":gender,"birthday":birthday,"email":email})
          console.log(this.children);
        }
      })
  }
}
</script>

<style>

</style>
