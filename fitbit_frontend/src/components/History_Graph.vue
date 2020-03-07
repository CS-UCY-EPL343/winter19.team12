<template>
  <q-card class='full-width'>
    <q-card-section>
      <div class="text-h6">History Heartbeat data for {{$store.state.main.username}}</div>
    </q-card-section>
    <q-separator />

    <div id="controls" style="width: 100%; overflow: hidden;">
    <div style="float: left; margin-left: 15px;">
      From: <input type="date" id="fromfield"class="amcharts-input" />
      To: <input type="date" id="tofield" class="amcharts-input" />
    </div>
    <div style="float: left; margin-left: 15px;">
      <q-btn color="primary" label="Search"  @click='clickSearch()'/>
    </div>
    </div>

    <q-card-section class='no-padding'>
      <div class='graph' ref='chartdiv' />
    </q-card-section>
  </q-card>
</template>

<script>
import store from 'src/store/index'
/* Imports */
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import axios from 'axios'

/* Chart code */
// Themes begin
import am4themes_animated from '@amcharts/amcharts4/themes/animated'
am4core.useTheme(am4themes_animated)
// Themes end

export default {
  name: 'Graph',
  data () {
    return {
      graph: '',
      graph_list: [],
    }
  },
  methods: {
    clickSearch(){
      const domain = this.$store.state.main.domain
      const user = this.$store.state.main.username

      let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart)
      chart.hiddenState.properties.opacity = 0

      chart.padding(0, 0, 0, 0)

      chart.zoomOutButton.disabled = true

      // Create chart instance
      chart.scrollbarX = new am4core.Scrollbar();

      chart.data = []

      let inputFieldFormat = "yyyy-MM-dd";
      let start = document.getElementById("fromfield").value;
      let end = document.getElementById("tofield").value;
      if ((start.length < inputFieldFormat.length) || (end.length < inputFieldFormat.length)) {
        alert("Please set correct dates")
        return;
      }

      if (start>end){
        alert("Please set the dates correctly")
        return;
      }

      let config = {
        headers:{
          'Content-Type': 'application/json',
          Authorization:"Bearer "+store().state.main.token
                }
      }

      let data = {
        username: this.$store.state.main.username,
        type_metric : 'calories',
        startDate : start,
        endDate : end
      }

      this.$axios.post(this.$store.state.main.domain + '/retrieve_history_metrics',data,config).then(response => {
        if (response.data.error === '0') {
          alert("Error")
        }
        else {
          const distinct = (value,index,self) => {
            return self.indexOf(value) === index;
          }
          var unique_dates = response.data.dates_list;
          var data = response.data.metric_list;
          console.log(data);
          for (var j=0;j<unique_dates.length;j++){
            let sum = 0;
            let count_sum = 0;
            for (var i=0;i<data.length;i++){
              var timestamp = data[i].timestamp;
              timestamp = timestamp.split("T");
              var date = timestamp[0];
              if (unique_dates[j]===date) {
                count_sum+=1
                var amount = data[i].amount;
                sum+=amount;
              }
            }
            chart.data.push({"Heartbeat":sum/count_sum,"Date":unique_dates[j]});
          }
          console.log(chart.data);
          update();

        }
      })

      function update(){
        // Create axes
        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 50;
        dateAxis.renderer.grid.template.location = 0.5;
        dateAxis.startLocation = 0.5;
        dateAxis.endLocation = 0.5;


        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "Metrics";

        // Create series
        var series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = "Heartbeat";
        series.dataFields.dateX = "Date";
        series.name = "Average Heartbeat (bpm)";
        series.tooltipText = "{name}: [bold]{valueY}[/]";
        series.strokeWidth = 3;
        series.stroke = am4core.color("#FF6F91");
        series.tooltip.fill = am4core.color("#FF6F91");
        series.tooltip.getFillFromObject = false;
        series.tooltip.background.fill = am4core.color("#FF6F91");

        // Add legend
        chart.legend = new am4charts.Legend();

        // Add cursor
        chart.cursor = new am4charts.XYCursor();

        // Add simple vertical scrollbar
        chart.scrollbarY = new am4core.Scrollbar();

        // Add horizotal scrollbar with preview
        var scrollbarX = new am4charts.XYChartScrollbar();
        scrollbarX.series.push(series);
        chart.scrollbarX = scrollbarX;

        /**
         * Set up external controls
         */

        // Date format to be used in input fields
        let inputFieldFormat = "yyyy-MM-dd";

        dateAxis.events.on("selectionextremeschanged", function() {
          updateFields();
        });

        dateAxis.events.on("extremeschanged", updateFields);

        function updateFields() {
          let minZoomed = dateAxis.minZoomed + am4core.time.getDuration(dateAxis.mainBaseInterval.timeUnit, dateAxis.mainBaseInterval.count) * 0.5;
          document.getElementById("fromfield").value = chart.dateFormatter.format(minZoomed, inputFieldFormat);
          document.getElementById("tofield").value = chart.dateFormatter.format(new Date(dateAxis.maxZoomed), inputFieldFormat);
        }

        document.getElementById("fromfield").addEventListener("keyup", updateZoom);
        document.getElementById("tofield").addEventListener("keyup", updateZoom);


        let zoomTimeout;
        function updateZoom() {
          if (zoomTimeout) {
            clearTimeout(zoomTimeout);
          }
          zoomTimeout = setTimeout(function() {
            let start = document.getElementById("fromfield").value;
            let end = document.getElementById("tofield").value;

            if ((start.length < inputFieldFormat.length) || (end.length < inputFieldFormat.length)) {
              alert("Please set correct dates")
              return;
            }

            if (start>end){
              alert("Please set the dates correctly")
              return;
            }


            let startDate = chart.dateFormatter.parse(start, inputFieldFormat);
            let endDate = chart.dateFormatter.parse(end, inputFieldFormat);

            if (startDate && endDate) {
              dateAxis.zoomToDates(startDate, endDate);
            }
          }, 500);
        }

      }
    }
  },
  mounted () {

    },
}

</script>

<style scoped>
    .graph {
      height: 350px;
      width: 100%;
    }
</style>
