<template>
  <q-card class='bg-yellow-2'>
    <q-card-section>
      <div class="text-h6">Notes</div>
    </q-card-section>
    <q-separator />
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
export default {
  name: 'NotesList',
  methods: {
    clickDelete(item){
      this.$q.loading.show();
      let idx = this.messages.indexOf(item)
      this.messages.splice(idx,1)
      this.$axios.post(this.$store.state.main.domain + '/delete_note', {
        'username': this.$store.state.main.username,
        'text' : item["title"] + "\n" + item ["text"],
        'timestamp' : item["timestamp"],
        'note_id' : item["note_id"],
      }).then(response => {
        if (response.data.error === '0') {
          alert("Error")
        }
        else {
          alert("You successfully delete your note");
        }
      })
      console.log(item["title"]);
      this.$q.loading.hide();
    },
    fetchNotesData(){
      this.$q.loading.show();
      this.$axios.post(this.$store.state.main.domain + '/retrieve_notes', {
        'username': this.$store.state.main.username
      }).then(response => {
          console.log(response);
          var data = response.data.note_list;
          for (var i=0;i<data.length;i++){
            var note_id = data[i].id;
            var writer = data[i].id_writer_id;
            var timestamp = data[i].timestamp;
            timestamp = timestamp.split("T");
            var date = timestamp[0];
            var time = timestamp[1].split(".")[0];

            var text = data[i].text;
            var array = text.split("\n");
            var title = array[0];
            var content = array[1];
            this.messages.push({"note_id":note_id,"timestamp":date+" "+time,"title":title,"text":content});
          }
      })
      this.$q.loading.hide();
    }
  },
  data() {
    return{
      messages: []
    }
  },

  mounted(){
    this.fetchNotesData();
  },
  template: '<p>{{ message }}</p>'
  }

</script>
