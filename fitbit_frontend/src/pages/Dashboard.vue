<template>
  <q-page class='q-pa-md'>
    <div class='row q-mb-md'>
      <graph />
    </div>
    <div class='row q-col-gutter-md'>
      <div class='col'>
        <notes-list />
      </div>
      <div class='col'>
        <add-note />
      </div>
    </div>
  </q-page>
</template>

<script>
import store from 'src/store/index'
import AddNote from 'src/components/AddNote'
import NotesList from 'src/components/NotesList'
import Graph from 'src/components/Graph'

export default {
  name: 'Dashboard',
  components: {
    'add-note': AddNote,
    'notes-list': NotesList,
    'graph': Graph
  },
  beforeRouteEnter (to, from, next) {
    if (store().state.main.username === '') {
      if (from.path === '/login') {
        next('/ulogin')
      }
      next('/login')
    }
    next()
  }
}
</script>
