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
             <q-tab name="Live graph Heartbeat"  label="Heartbeat" />
             <q-tab name="Calories"  label="Calories" />
             <q-tab name="Distance Covered" label="Distance" />
             </q-tabs>
          </template>
        </div>
      </div>


      <div class="col fit row wrap justify-end items-start content-start">

      </div>
    </div>

      <template >
              <q-tab-panels
                v-model="tab"
                animated
                transition-prev="jump-up"
                transition-next="jump-up"
              >
                  <q-tab-panel name="Live graph Heartbeat">
                    <div>
                    <graph />
                    </div>
                  </q-tab-panel>

                  <q-tab-panel name="Calories">
                    <div>
                    <graphC />
                  </div>
                  </q-tab-panel>


                  <q-tab-panel name="Activity">
                    <div>
                      Activity
                    </div>
                  </q-tab-panel>

                <q-tab-panel name="Distance Covered">
                  <div>
                    <graphDistance />
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
import History_Graph from 'src/components/History_Graph'
import History_Calories_Graph from 'src/components/History_Calories_Graph'
import History_Distance_Graph from 'src/components/History_Distance_Graph'


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
 components: {
    'add-note': AddNote,
    'notes-list': NotesList,
    'graph': History_Graph,
    'graphC': History_Calories_Graph,
    'graphDistance': History_Distance_Graph,
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
