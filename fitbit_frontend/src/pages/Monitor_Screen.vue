<template>
  <div class="q-pa-md">
    <q-table
      title="Patients"
      :data="data"
      :columns="columns"
      row-key="name"
      :filter="filter"
      no-data-label="I didn't find anything for you"
    >

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
             class="text-italic text-blue"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="accent" round dense @click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'" />
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">
              <q-btn color="primary" label="Select patient" class="q-mt-md" @click='clickSelect(props.row.name)'>
                <q-tooltip content-class="bg-accent">See {{ props.row.name }} data </q-tooltip>
              </q-btn>
              <q-btn color="red" label="Delete patient" class="q-mt-md" @click='delete_patient(props.row.name)'>
                <q-tooltip content-class="bg-accent">Delete {{ props.row.name }}</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>

      <template v-slot:no-data="{ icon, message, filter }">
        <div class="full-width row flex-center text-accent q-gutter-sm">
          <q-icon size="2em" name="sentiment_dissatisfied" />
          <span>
            Well this is sad... {{ message }}
          </span>
          <q-icon size="2em" :name="filter ? 'filter_b_and_w' : icon" />
        </div>
      </template>
    </q-table>


    <q-table
      title="Request sent from patients"
      :data="data1"
      :columns="columns1"
      row-key="name"
      :filter="filter1"
      no-data-label="I didn't find anything for you"
    >

      <template v-slot:header="props">
        <q-tr :props="props">
          <q-th auto-width />
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
             class="text-italic text-blue"
          >
            {{ col.label }}
          </q-th>
        </q-tr>
      </template>

      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter1" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td auto-width>
            <q-btn size="sm" color="accent" round dense @click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'" />
          </q-td>
          <q-td
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
          >
            {{ col.value }}
          </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
          <q-td colspan="100%">
            <div class="text-left">
              <q-btn type='submit' id="patient" :value="props.row.name" color="primary" @click='accept_patient()' icon="done" label="Accept" class="q-mt-md">
                <q-tooltip content-class="bg-accent">Accept {{ props.row.name }}</q-tooltip>
              </q-btn>
              <q-btn color="red" id="reject" icon="delete_forever" :value="props.row.name" @click='reject_patient()' label="Reject" class="q-mt-md">
                <q-tooltip content-class="bg-accent">Reject {{ props.row.name }}</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </q-tr>
      </template>

      <template v-slot:no-data="{ icon, message, filter }">
        <div class="full-width row flex-center text-accent q-gutter-sm">
          <q-icon size="2em" name="sentiment_dissatisfied" />
          <span>
            Well this is sad... {{ message }}
          </span>
          <q-icon size="2em" :name="filter1 ? 'filter_b_and_w' : icon" />
        </div>
      </template>

    </q-table>

  </div>
</template>




<script>
import store from 'src/store/index'
import axios from 'axios'

export default {
  methods: {
    clickSelect(name){
      this.$store.state.main.view_user = name
      console.log(this.$store.state.main);
      // console.log(name);
      this.$store.commit('main/change_view', {'view_user':name})
      this.$router.push({path:'/track_user', name: 'track_user/dashboard'})
      // this.$q.notify(`You have logged in successfully as Specialist.`)


    },
      accept_patient () {

            let config = {
                headers:{
                  'Content-Type': 'application/json',
                  Authorization:"Bearer "+store().state.main.token
                }
            }


            let data={
              username: document.getElementById("patient").value
            }

              this.$axios.post(this.$store.state.main.domain + '/permission_request',data,config).then(response => {
                console.log(response);
                if (response.data.status == '1') {
                  this.$q.notify(`Patient accepted!`)
                }
              })
              location.reload();
      },
        reject_patient (){

          let config = {
              headers:{
                'Content-Type': 'application/json',
                Authorization:"Bearer "+store().state.main.token
              }
          }

          let data={
            username: document.getElementById("reject").value,
            reject: true
          }
          console.log(data);

          this.$axios.post(this.$store.state.main.domain + '/permission_request',data,config).then(response => {
            console.log(response);
            if (response.data.status == '1') {
              this.$q.notify(`Patient rejected!`)
            }
          })
          location.reload();
        },
        delete_patient(name){

          let config = {
              headers:{
                'Content-Type': 'application/json',
                Authorization:"Bearer "+store().state.main.token
              }
          }

          let data={
            username: name,
            reject: true
          }
          console.log(data);

          this.$axios.post(this.$store.state.main.domain + '/permission_request',data,config).then(response => {
            console.log(response);
            if (response.data.status == '1') {
              this.$q.notify(`Patient deleted!`)
            }
          })
          location.reload();
        }

  },
  data () {
    return {
      filter: '',
      filter1:'',
      columns: [
        {
          name: 'name',
          required: true,
          label: 'Patients_Id',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'firstName', align: 'center', label: 'First name', field: 'firstName', sortable: true },
        { name: 'surname', label: 'Surname', field: 'surname' ,sortable: true },
        { name: 'telephone', label: 'Telephone', field: 'telephone'  },
      ],
      columns1:[
        {
          name: 'name',
          required: true,
          label: 'Patients_Id',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'firstName', align: 'center', label: 'First name', field: 'firstName', sortable: true },
        { name: 'surname', label: 'Surname', field: 'surname' ,sortable: true },
        { name: 'telephone', label: 'Telephone', field: 'telephone'  },
      ]
      ,data: [],
       data1:[]
    }
  },
  mounted(){

          let config = {
                headers:{
                    Authorization:"Bearer "+store().state.main.token
                  }
              }

          axios.get(this.$store.state.main.domain + '/permission_request',config).then(response => {
                var data = response.data.users;
                console.log(data)
                for (var i=0;i<data.length;i++){
                        if(data[i].completed==false){
                          var name = data[i].username;
                          var first_name = data[i].username;
                          var surname = data[i].surname;
                          var telephone = data[i].telephone;
                          this.data1.push({ "name":name , "firstName":first_name, "surname":surname, "telephone":telephone })
                        }else{
                          var name = data[i].username;
                          var first_name = data[i].username;
                          var surname = data[i].surname;
                          var telephone = data[i].telephone;
                          this.data.push({ "name":name , "firstName":first_name, "surname":surname, "telephone":telephone })
                        }
                }
          })


      }
}
</script>
