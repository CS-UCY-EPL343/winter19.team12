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
        if (this.noteTitle==='' || this.noteContent === '') {
          alert("Please fill all the gaps to the Note List");
        }
        else {
          this.$q.loading.show()
          this.$axios.post(this.$store.state.main.domain + '/save_note', {
            'owner': this.$store.state.main.username,
            'reader' : this.$store.state.main.username,
            'description': this.noteTitle + "\n" + this.noteContent,
          }).then(response => {
            if (response.data.error === '0') {
              alert("Error")
            }
            else {
              alert("You successfully save your note");
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
