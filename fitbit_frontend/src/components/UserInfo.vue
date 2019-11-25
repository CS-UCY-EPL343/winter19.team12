<template>
  <span v-if='$store.state.main.username !== ""'>
    Welcome {{$store.state.main.username}}!
  </span>
</template>

<script>
export default {
  name: 'UserInfo'
}
</script>
