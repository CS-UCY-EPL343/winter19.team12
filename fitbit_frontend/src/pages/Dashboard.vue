<template>
  <q-page class='q-pa-md'>

    <div class=" row">
      <div class="col">
        <template >
          <q-tabs
           v-model="tab"
           inline-label
           class="bg-primary text-white shadow-2"
           >
           <q-tab name="Live graph Heartbeat"  label="Live Heartbeat graph" />
           <q-tab name="Compare Metrics" label="Compare Metrics graph" />
           </q-tabs>
        </template>
      </div>
    </div>

      <template >
              <q-tab-panels
                v-model="tab"
                animated
                transition-prev="jump-up"
                transition-next="jump-up">
                  <q-tab-panel name="Live graph Heartbeat">
                    <div>
                    <graph />
                    </div>
                  </q-tab-panel>

                  <q-tab-panel name="Compare Metrics">
                    <div>
                    <graphCom />
                  </div>
                  </q-tab-panel>
              </q-tab-panels>
      </template>

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
import Calories_graph from 'src/components/Calories_graph'
import Compare_metrics from 'src/components/Compare_metrics'


export default {
  name: 'Dashboard',
  data () {
   return {
    tab: 'Live graph Heartbeat'
    }
  },
  mounted(){
    var same_user = this.$store.state.main.username.localeCompare(this.$store.state.main.view_user);
    var is_specialist = this.$store.state.main.is_specialist
    if (same_user==0 && is_specialist){
      this.$q.notify(`You do not have access to this link.`)
      this.$router.push({ path: 'track_user/error',name: 'error'})
    }
  },
  destroyed:function(){
    console.log("detroyed dashboard");
  },
 components: {
    'add-note': AddNote,
    'notes-list': NotesList,
    'graph': Graph,
    'graphC': Calories_graph,
    'graphCom': Compare_metrics
  },
  beforeRouteEnter (to, from, next) {
    if (store().state.main.view_user === '') {
      if (from.path === '/login') {
        next('/ulogin')
      }
      next('/login')
    }
    next()
  }
}
</script>
