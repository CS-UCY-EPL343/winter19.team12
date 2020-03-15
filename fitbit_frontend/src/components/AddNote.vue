<template>
  <q-card class='bg-yellow-2'>
    <q-card-section>
      <div class="text-h6">Add note</div>
    </q-card-section>
    <q-separator />
    <q-card-section class='no-padding'>
      <q-input v-model='noteTitle'
               type='text'
               borderless
               placeholder='Note title...'
               class='q-px-md'
      />
    </q-card-section>

    <q-separator />
    <q-card-section class='no-padding'>
      <q-input v-model='noteContent'
               type='textarea'
               borderless
               autogrow
               placeholder='Note content...'
               class='q-px-md'
      />
    </q-card-section>
    <q-separator />
    <q-card-actions>
      <q-btn label='Save' icon='save' @click='clickSave'/>
      <q-btn label='Clear' icon='clear' @click='clearButton' />
    </q-card-actions>
  </q-card>
</template>

<script>
import store from 'src/store/index'

export default {
  name: 'AddNote',
  data () {
    return {
      noteTitle: '',
      noteContent: ''
    }
  },
  methods: {
      clearButton(){
        this.noteTitle = '';
        this.noteContent = '';
      },


      clickSave(){

        let config = {
          headers:{
            'Content-Type': 'application/json',
            Authorization:"Bearer "+store().state.main.token
                  }
        }

        let data = {
          owner: this.$store.state.main.username,
          reader : this.$store.state.main.view_user,
          description : this.noteTitle + "\n" + this.noteContent
        }

        if (this.noteTitle==='' || this.noteContent === '') {
          alert("Please fill all the gaps to the Note List");
        }
        else {
          this.$q.loading.show()
          this.$axios.post(this.$store.state.main.domain + '/save_note',data,config).then(response => {
            if (response.data.error === '0') {
              alert("Error")
            }
            else {
              this.$q.notify('Your note has saved successfully')
              location.reload();
              this.noteTitle = '';
              this.noteContent = '';
            }
          })
          this.$q.loading.hide()
        }
      }

  }
}

</script>
