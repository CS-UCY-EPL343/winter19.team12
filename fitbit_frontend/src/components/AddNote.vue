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
  }
}
</script>
