<template>
  <q-card class='bg-yellow-2'>
    <q-card-section>
      <div class="text-h6">Notes</div>
    </q-card-section>
    <q-separator />

    <q-card-section class='no-padding'>
      <q-list separator >
        <q-item class='bg-blue-2' clickable v-ripple v-for="msg in specialist_messages">
          <q-item-section>
            <q-item-label> <b>{{msg.title}}</b>
            </q-item-label>
            <q-item-label caption> {{msg.text}}</q-item-label>
            <q-item-label caption> <i>{{msg.timestamp}}</i>
            </q-item-label>
            <q-item-label caption> <i>#PK {{msg.note_id}}</i>
            </q-item-label>
          </q-item-section>
          <q-item-section>
            <q-btn flat round dense color="black" icon="delete" @click='clickDeleteSpecialist(msg)'/>
          </q-item-section>
        </q-item>
    </q-list>
    </q-card-section>

    <q-card-section class='no-padding'>
      <q-list separator >
        <q-item clickable v-ripple v-for="msg in messages">
          <q-item-section>
            <q-item-label> <b>{{msg.title}}</b>
            </q-item-label>
            <q-item-label caption> {{msg.text}}</q-item-label>
            <q-item-label caption> <i>{{msg.timestamp}}</i>
            </q-item-label>
            <q-item-label caption> <i>#PK {{msg.note_id}}</i>
            </q-item-label>
          </q-item-section>
          <q-item-section>
            <q-btn flat round dense color="black" icon="delete" @click='clickDelete(msg)'/>
          </q-item-section>
        </q-item>
    </q-list>
    </q-card-section>

  </q-card>
</template>


<script>
import store from 'src/store/index'
import axios from 'axios'
export default {
  name: 'NotesList',
  methods: {
    clickDeleteSpecialist(item){
      if (!this.$store.state.main.is_specialist) {
        this.$q.notify('You do not have the permission to delete this note');
      }
      else {
        let config = {
          headers:{
            'Content-Type': 'application/json',
            Authorization:"Bearer "+store().state.main.token
                  }
        }

        let data = {
          username: this.$store.state.main.view_user,
          text : item["title"] + "\n" + item ["text"],
          timestamp : item["timestamp"],
          note_id : item["note_id"]
        }

        this.$q.loading.show();
        let idx = this.specialist_messages.indexOf(item)
        this.specialist_messages.splice(idx,1)
        this.$axios.post(this.$store.state.main.domain + '/delete_note',data,config).then(response => {
          if (response.data.error === '0') {
            this.$q.notify('Error')
          }
          else {
            this.$q.notify('You successfully delete your note')
          }
        })
        console.log(item["title"]);
        this.$q.loading.hide();
      }
    },
    clickDelete(item){
      if (this.$store.state.main.view_user.localeCompare(this.$store.state.main.username)!=0) {
        this.$q.notify('You do not have the permission to delete this note');
      }
      else {
        let config = {
          headers:{
            'Content-Type': 'application/json',
            Authorization:"Bearer "+store().state.main.token
                  }
        }

        let data = {
          username: this.$store.state.main.view_user,
          text : item["title"] + "\n" + item ["text"],
          timestamp : item["timestamp"],
          note_id : item["note_id"]
        }

        this.$q.loading.show();
        let idx = this.messages.indexOf(item)
        this.messages.splice(idx,1)
        this.$axios.post(this.$store.state.main.domain + '/delete_note',data,config).then(response => {
          if (response.data.error === '0') {
            this.$q.notify('Error')
          }
          else {
            this.$q.notify('You successfully delete your note')
          }
        })
        console.log(item["title"]);
        this.$q.loading.hide();
    }
  },
    fetchNotesData(){
      let config = {
        headers:{
          'Content-Type': 'application/json',
          Authorization:"Bearer "+store().state.main.token
                }
      }

      let data = {
        username: this.$store.state.main.view_user,
      }

      this.$axios.post(this.$store.state.main.domain + '/retrieve_notes',data,config).then(response => {
          var data_patient = response.data.patient_list;
          for (var i=0;i<data_patient.length;i++){
            var note_id = data_patient[i].id;
            var writer = data_patient[i].id_writer_id;
            var timestamp = data_patient[i].timestamp;
            timestamp = timestamp.split("T");
            var date = timestamp[0];
            var time = timestamp[1].split(".")[0];

            var text = data_patient[i].text;
            var array = text.split("\n");
            var title = array[0];
            var content = array[1];
            this.messages.push({"note_id":note_id,"timestamp":date+" "+time,"title":title,"text":content});
          }

          var data_specialist = response.data.specialist_list;
          for (var i=0;i<data_specialist.length;i++){
            var note_id = data_specialist[i].id;
            var writer = data_specialist[i].id_writer_id;
            var timestamp = data_specialist[i].timestamp;
            timestamp = timestamp.split("T");
            var date = timestamp[0];
            var time = timestamp[1].split(".")[0];

            var text = data_specialist[i].text;
            var array = text.split("\n");
            var title = array[0];
            var content = array[1];
            this.specialist_messages.push({"note_id":note_id,"timestamp":date+" "+time,"title":title,"text":content});
          }
      })
      // this.$q.loading.hide();
    }
  },
  data() {
    return{
      messages: [],
      specialist_messages : []
    }
  },

  mounted(){
    this.fetchNotesData();
  },
  template: '<p>{{ message }}</p>'
  }

</script>
