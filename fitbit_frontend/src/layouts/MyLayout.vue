<template>
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
          Fitbit Monitoring System
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
        <template v-if='$store.state.main.loggedIn && !$store.state.main.is_specialist '>

          <q-item :to='{name: "dashboard"}' clickable tag="a" exact>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "history"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="history" />
            </q-item-section>
            <q-item-section>
              <q-item-label>History Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "edit"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="edit" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Edit Profile</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "select_doctor"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="supervised_user_circle" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Select Doctor</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "activity"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="directions_run" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Activity</q-item-label>
            </q-item-section>
          </q-item>


        </template>
        <template v-else-if='$store.state.main.loggedIn && $store.state.main.is_specialist'>

          <q-item :to='{name: "monitor"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="accessibility" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Monitor</q-item-label>
            </q-item-section>
          </q-item>

          <q-item :to='{name: "edit"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="edit" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Edit Profile</q-item-label>
            </q-item-section>
          </q-item>
        </template>

        <template v-else>
          <q-item :to='{name: "login"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Login</q-item-label>
              <q-item-label caption>Login to your account</q-item-label>
            </q-item-section>
          </q-item>
          <q-item :to='{name: "register"}' clickable tag="a">
            <q-item-section avatar>
              <q-icon name="person_add" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Register</q-item-label>
              <q-item-label caption>Create a user account</q-item-label>
            </q-item-section>
          </q-item>
        </template>
        <q-item :to='{name: "help"}' clickable tag="a">
          <q-item-section avatar>
            <q-icon name="help" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Help</q-item-label>
            <q-item-label caption>Find help on how to get started!</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable tag="a" target="_blank" href="https://github.com/CS-UCY-EPL343/winter19.team12">
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Github</q-item-label>
            <q-item-label caption>EPL343 - winter19.team12</q-item-label>
          </q-item-section>
        </q-item>

        <q-item @click='logout' clickable tag="a">
          <q-item-section avatar>
            <q-icon name="exit_to_app" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Log out</q-item-label>
          </q-item-section>
        </q-item>

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
    logout () {
      this.$q.loading.show()
      this.$axios.post(this.$store.state.main.domain + '/logout_api').then(response => {
        if (response.data.status === 1) {
          this.$store.commit('main/logout')
          this.$router.push({ name: 'login' })
          this.$q.notify(`You have logged out successfully.`)
        }
        this.$q.loading.hide()
      })
    }
  }
}
</script>
