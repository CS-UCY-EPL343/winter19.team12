<template>
  <q-card class='full-width'>
    <q-card-section>
      <div class="text-h6">Heartbeat data for {{$store.state.main.username}}</div>
    </q-card-section>
    <q-separator />
    <q-card-section class='no-padding'>
      <div class='graph' ref='chartdiv' />
    </q-card-section>
  </q-card>
</template>

<script>
import * as am4core from '@amcharts/amcharts4/core'
import * as am4charts from '@amcharts/amcharts4/charts'
// eslint-disable-next-line camelcase
import am4themes_animated from '@amcharts/amcharts4/themes/animated'
import axios from 'axios'
import store from 'src/store/index'
am4core.useTheme(am4themes_animated)
let interval
export default {
  name: 'Graph',
  data () {
    return {
      graph: ''
    }
  },
  destroyed:function(){
    if (interval) {
      clearInterval(interval)
    }
    console.log("destroyed tab");
  },
  mounted () {
    const domain = this.$store.state.main.domain
    let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart)
    chart.hiddenState.properties.opacity = 0

    chart.padding(0, 0, 0, 0)

    chart.zoomOutButton.disabled = true

    let data = []
    let visits = 10
    let i = 0

    for (i = 0; i <= 30; i++) {
      visits -= Math.round((Math.random() < 0.5 ? 1 : -1) * Math.random() * 10)
      data.push({ date: new Date().setSeconds(i - 30), value: visits })
    }

    chart.data = data

    let dateAxis = chart.xAxes.push(new am4charts.DateAxis())
    dateAxis.renderer.grid.template.location = 0
    dateAxis.renderer.minGridDistance = 30
    dateAxis.dateFormats.setKey('second', 'ss')
    dateAxis.periodChangeDateFormats.setKey('second', '[bold]h:mm a')
    dateAxis.periodChangeDateFormats.setKey('minute', '[bold]h:mm a')
    dateAxis.periodChangeDateFormats.setKey('hour', '[bold]h:mm a')
    dateAxis.renderer.inside = true
    dateAxis.renderer.axisFills.template.disabled = true
    dateAxis.renderer.ticks.template.disabled = true

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis())
    valueAxis.tooltip.disabled = true
    valueAxis.interpolationDuration = 500
    valueAxis.rangeChangeDuration = 500
    valueAxis.renderer.inside = true
    valueAxis.renderer.minLabelPosition = 0.05
    valueAxis.renderer.maxLabelPosition = 0.95
    valueAxis.renderer.axisFills.template.disabled = true
    valueAxis.renderer.ticks.template.disabled = true

    let series = chart.series.push(new am4charts.LineSeries())
    series.dataFields.dateX = 'date'
    series.dataFields.valueY = 'value'
    series.interpolationDuration = 500
    series.defaultState.transitionDuration = 0
    series.tensionX = 0.8

    chart.events.on('datavalidated', function () {
      dateAxis.zoom({ start: 1 / 15, end: 1.2 }, false, true)
    })

    dateAxis.interpolationDuration = 500
    dateAxis.rangeChangeDuration = 500

    document.addEventListener('visibilitychange', function () {
      console.log("visibilitychange");
      if (document.hidden) {
        if (interval) {
          clearInterval(interval)
        }
      } else {
        startInterval()
      }
    }, false)

    function updateGraph () {
      let config = {
        headers:{
          Authorization:"Bearer "+store().state.main.token
        }
      }
      console.log(store().state.main.token)
      axios.get(domain + '/get_latest_metric?type=heart',config).then(response => {
        let lastdataItem = series.dataItems.getIndex(series.dataItems.length - 1)
        chart.addData(
          { date: new Date(lastdataItem.dateX.getTime() + 2000), value: response.data.value },
          1
        )
      })
    }

    // add data
    function startInterval () {
      interval = setInterval(function () {
        updateGraph()
      }, 2000)
    }

    startInterval()

    // all the below is optional, makes some fancy effects
    // gradient fill of the series
    series.fillOpacity = 1
    let gradient = new am4core.LinearGradient()
    gradient.addColor(chart.colors.getIndex(0), 0.2)
    gradient.addColor(chart.colors.getIndex(0), 0)
    series.fill = gradient

    // this makes date axis labels to fade out
    dateAxis.renderer.labels.template.adapter.add('fillOpacity', function (fillOpacity, target) {
      let dataItem = target.dataItem
      return dataItem.position
    })

    // need to set this, otherwise fillOpacity is not changed and not set
    dateAxis.events.on('validated', function () {
      am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
        // eslint-disable-next-line no-self-assign
        label.fillOpacity = label.fillOpacity
      })
    })

    // this makes date axis labels which are at equal minutes to be rotated
    dateAxis.renderer.labels.template.adapter.add('rotation', function (rotation, target) {
      let dataItem = target.dataItem
      // eslint-disable-next-line eqeqeq
      if (dataItem.date && dataItem.date.getTime() == am4core.time.round(new Date(dataItem.date.getTime()), 'minute').getTime()) {
        target.verticalCenter = 'middle'
        target.horizontalCenter = 'left'
        return -90
      } else {
        target.verticalCenter = 'bottom'
        target.horizontalCenter = 'middle'
        return 0
      }
    })

    // bullet at the front of the line
    let bullet = series.createChild(am4charts.CircleBullet)
    bullet.circle.radius = 5
    bullet.fillOpacity = 1
    bullet.fill = chart.colors.getIndex(0)
    bullet.isMeasured = false

    series.events.on('validated', function () {
      bullet.moveTo(series.dataItems.last.point)
      bullet.validatePosition()
    })

    this.graph = chart
  },
  beforeDestroy () {
    if (this.graph) {
      this.graph.dispose()
    }
  }
}
</script>

<style scoped>
.graph {
  height: 350px;
  width: 100%;
}
</style>
