<template>
  <q-page class='q-pa-md'>
    <div class='row q-mb-md'>

    <div class=" row">
      <div class="col">
        <q-btn-toggle
          v-model="model"
          toggle-color="primary"
          :options="[
            {label: 'Live graph Heartbeat', value: 'Heartbeat'},
            {label: 'Calories', value: 'Calories'},
            {label: 'Activity', value: 'Activity'},
            {label: 'Distance Covered', value: 'Distance'}
          ]"
        />
      </div>
      <div class="col fit row wrap justify-end items-start content-start">
        <calendar/>
      </div>
    </div>
    
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
import FunctionalCalendar from 'src/components/FunctionalCalendar'

export default {
  name: 'Dashboard',
  components: {
    'add-note': AddNote,
    'notes-list': NotesList,
    'graph': Graph,
    'calendar': FunctionalCalendar
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
