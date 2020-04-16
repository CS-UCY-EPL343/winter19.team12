<template>
  <div class='text-h6'>
    The user is now <br>
    {{text}}
  </div>
</template>

<script>
import store from 'src/store/index'
import axios from 'axios'
export default {
  data () {
    return {
      text: 'HERE'
    }
  },
  mounted(){

    let config = {
        headers:{
          'Content-Type': 'application/json',
          Authorization:"Bearer "+store().state.main.token
        }
    }

    axios.get(this.$store.state.main.domain + '/activity',config).then(response => {
      console.log(response);
    })
  }
}
</script>
