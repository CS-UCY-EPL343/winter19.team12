<template>
  <div >
    <p>Please select the day to present metrics</p>
    <functional-calendar  :is-modal='true' :is-date-range='true'></functional-calendar>
  </div>
</template>


<script>
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
