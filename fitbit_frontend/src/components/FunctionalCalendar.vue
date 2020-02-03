<template>
  <div >
    <p>Please select the day to present metrics</p>
    {{new Date().getDate() }} {{new Date().getMonth() }}

    <functional-calendar  :is-modal='true' :is-date-range='true'></functional-calendar>
  </div>
</template>


<script>
  var a = new Date().getDate()+":"+new Date().getMonth()+"apoel"
  console.log(a)
  // Introduced in vue file
  import { FunctionalCalendar } from 'vue-functional-calendar';

export default {
    components: {
        FunctionalCalendar
    },
    data() {
        return {
            calendarData: {}
        }
    }
}
</script>
