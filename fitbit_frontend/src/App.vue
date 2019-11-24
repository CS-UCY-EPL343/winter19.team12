<template>
  <div id="q-app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  created () {
    if (this.$q.localStorage.has('username')) {
      this.$store.commit('main/login', this.$q.localStorage.getItem('username'))
    }
  }
}
</script>
