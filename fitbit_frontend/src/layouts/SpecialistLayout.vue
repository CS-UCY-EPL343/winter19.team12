<template v-if='$store.state.main.loggedIn && $store.state.main.is_specialist'>
  <q-layout view="hHh lpR lfr" class='bg-blue-grey-1'>
    <q-header reveal elevated class='bg-indigo'>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="$refs.sidebar.toggle()"
          icon="menu"
          aria-label="Menu"
        />

        <q-toolbar-title>
          Fitbit Monitoring System (View-Only)
        </q-toolbar-title>

        <user-info />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftSidebar"
      ref='sidebar'
      show-if-above
      bordered
    >
      <q-list padding>
        <template>

          <q-item :to='{name: "track_user/dashboard"}' clickable tag="a" exact>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "track_user/history"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="history" />
            </q-item-section>
            <q-item-section>
              <q-item-label>History Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item @click='back' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="keyboard_backspace" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Back</q-item-label>
              <q-item-label caption>Back to the patient's selection</q-item-label>
            </q-item-section>
          </q-item>


        </template>


      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import UserInfo from 'src/components/UserInfo'

export default {
  name: 'MyLayout',

  components: {
    'user-info': UserInfo
  },
  data () {
    return {
      leftSidebar: false
    }
  },
  methods: {
    back(){
      this.$q.loading.show()
      this.$store.commit('main/change_view', {'view_user':this.$store.state.main.username})
      this.$router.push({ path: '',name: 'monitor'})
      this.$q.loading.hide()
    }
  }
}
</script>
