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
        <!--<q-item-label header>Essential Links</q-item-label>-->
        <q-item :to='{name: "dashboard"}' clickable tag="a" exact>
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>
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
        <q-item :to='{name: "edit"}' clickable tag="a">
          <q-item-section avatar>
            <q-icon name="edit_profile" />
          </q-item-section>
          <q-item-section>
            <q-item-label>EditProfile</q-item-label>
            <q-item-label caption>Edit a user profile account</q-item-label>
          </q-item-section>
        </q-item>
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
        <q-item clickable tag="a" target="_blank" href="https://quasar.dev">
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Quasar Docs</q-item-label>
            <q-item-label caption>quasar.dev</q-item-label>
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
  }
}
</script>
