<template>
  <q-card class='full-width'>
    <q-card-section>
      <div class="text-h6">History Calories data for {{$store.state.main.username}}</div>
    </q-card-section>
    <q-separator />

    <div id="controls" style="width: 100%; overflow: hidden;">
    <div style="float: left; margin-left: 15px;">
      From: <input type="date" id="fromfield"class="amcharts-input" />
      To: <input type="date" id="tofield" class="amcharts-input" />
    </div>
    </div>

    <q-card-section class='no-padding'>
      <div class='graphC' ref='chartdiv' />
    </q-card-section>
  </q-card>
</template>

<script>

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
  name: 'GraphC',
  data () {
    return {
      graphC: '',
      graph_list: [],
    }
  },
  methods: {
    retrieveHistoryCalories(){
      this.$axios.post(this.$store.state.main.domain + '/retrieve_history_metrics', {
        'username': this.$store.state.main.username,
        'type_metric' : 'calories',
      }).then(response => {
        if (response.data.error === '0') {
          alert("Error")
        }
        else {
          var data = response.data.metric_list;
          for (var i=0;i<data.length;i++){
            var timestamp = data[i].timestamp;
            timestamp = timestamp.split("T");
            var date = timestamp[0];

            var amount = data[i].amount;
            this.graph_list.push({"Calories":amount,"Date":date});
          }
        }
      })
    },
  },
  mounted () {
    let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
    chart.data = [];
    this.retrieveHistoryCalories();

    const domain = this.$store.state.main.domain
    chart.hiddenState.properties.opacity = 0

    chart.padding(0, 0, 0, 0)

    chart.zoomOutButton.disabled = true

    // Create chart instance
    chart.scrollbarX = new am4core.Scrollbar();

    // Add data
    chart.data = this.graph_list

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.location = 0.5;
    dateAxis.startLocation = 0.5;
    dateAxis.endLocation = 0.5;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Metrics";

    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = "calories";
    series.dataFields.dateX = "date";
    series.name = "Calories";
    series.tooltipText = "{name}: [bold]{valueY}[/]";


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

    function zoomToDates(date) {
      let min = dateAxis.groupMin["day1"];
      let max = dateAxis.groupMax["day1"];
      dateAxis.keepSelection = true;
      //dateAxis.start = (date.getTime() - min)/(max - min);
      //dateAxis.end = 1;

      dateAxis.zoom({start:(date.getTime() - min)/(max - min), end:1});
    }

    this.graphCom=chart



    },



    beforeDestroy () {
    if (this.graphCom) {
      this.Com.dispose()
    }
    }
}

</script>

<style scoped>
    .graphC {
      height: 350px;
      width: 100%;
    }
</style>
