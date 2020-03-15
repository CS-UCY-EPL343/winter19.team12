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
  </div>
</template>




<script>
import store from 'src/store/index'
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

    fetchUsersData(){
      let config = {
        headers:{
          'Content-Type': 'application/json',
          Authorization:"Bearer "+store().state.main.token
                }
      }

      let data = {
        username: this.$store.state.main.username,
      }

      this.$axios.post(this.$store.state.main.domain + '/retrieve_users',data,config).then(response =>{
            var data_patient = response.data.patient_list;
            // console.log(data_patient);
            for (var i = 0; i < data_patient.length; i++) {
              var info = data_patient[i]
              // console.log(info);
              var p_username = info['username']
              var p_date_joined = info['date_joined'].split("T")[0]
              this.data.push({name:p_username,date:p_date_joined})
            }
      })


    }
  },
  data () {
    return {
      filter: '',
      columns: [
        {
          name: 'name',
          required: true,
          label: 'Patients',
          align: 'left',
          field: row => row.name,
          format: val => `${val}`,
          sortable: true
        },
        { name: 'Register date', align: 'center', label: 'Register date', field: 'date', sortable: true },
        { name: 'age', label: 'Age', field: 'age' },

      ],
      data: []
    }
  },
  mounted(){
    this.fetchUsersData();
  }
}
</script>
