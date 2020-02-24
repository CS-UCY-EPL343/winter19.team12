<template>
  <q-card class='full-width'>
    <q-card-section>
      <div class="text-h6">Metric Comparison {{$store.state.main.username}}</div>
    </q-card-section>
    <q-separator />

  <div id="controls" style="width: 100%; overflow: hidden;">
     <div style="float: left; margin-left: 15px;">
     From: <input type="date" id="fromfield"class="amcharts-input" />
     To: <input type="date" id="tofield" class="amcharts-input" />
     </div>

     <div style="float: right; margin-right: 15px;">
       <q-btn id="b1m" class="amcharts-input" style="background: goldenrod; color: white" label="1m" />
       <q-btn id="b3m" class="amcharts-input" style="background: goldenrod; color: white" label="3m" />
       <q-btn id="b6m" class="amcharts-input" style="background: goldenrod; color: white" label="6m" />
       <q-btn id="b1y" class="amcharts-input" style="background: goldenrod; color: white" label="1y" />
       <q-btn id="bytd" class="amcharts-input" style="background: goldenrod; color: white" label="YTD" />
       <q-btn id="bmax" class="amcharts-input" style="background: goldenrod; color: white" label="MAX" />
     </div>
   </div>
    <q-card-section class='no-padding'>
      <div class='graphCom' ref='chartdiv' />
    </q-card-section>
  </q-card>
</template>

<script>
import * as am4core from '@amcharts/amcharts4/core'
import * as am4charts from '@amcharts/amcharts4/charts'
// eslint-disable-next-line camelcase
import am4themes_animated from '@amcharts/amcharts4/themes/animated'
import axios from 'axios'

am4core.useTheme(am4themes_animated)

export default {
  name: 'GraphCom',
  data () {
    return {
      graphCom: ''
    }
  },
  mounted () {

    const domain = this.$store.state.main.domain
    const user = this.$store.state.main.username
    let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart)
    am4core.useTheme(am4themes_animated);


    chart.paddingRight = 20;

    // Add data
    chart.data = [{
      "date": new Date(2018, 3, 20),
      "calories": 90,
      "heartbeat": 45
    }, {
      "date": new Date(2018, 3, 21),
      "calories": 102,
      "heartbeat": 90,
      "activity" : 102,
      "distance" : 310
    }, {
      "date": new Date(2018, 3, 22)
    }, {
      "date": new Date(2018, 3, 23),
      "calories": 125,
      "activity" : 102
    }, {
      "date": new Date(2018, 3, 24),
      "calories": 55,
      "heartbeat": 90,
      "activity" : 102,
      "distance" : 403
    }, {
      "date": new Date(2018, 3, 25),
      "calories": 81,
      "heartbeat": 60,
      "activity" : 102
    }, {
      "date": new Date(2018, 3, 26),
      "distance" : 403
    }, {
      "date": new Date(2018, 3, 27),
      "calories": 63,
      "heartbeat": 87,
      "activity" : 102,
      "distance" : 403
    }, {
      "date": new Date(2018, 3, 28),
      "calories": 113,
      "heartbeat": 62,
      "activity" : 102,
      "distance" : 403
    }];


    function updateGraph (start,end) {
      console.log(start +" "+end);

      var request = {
      params: {
        from: start,
        to: end,
        username: user
      }
    }

  axios.get(domain + '/get_all_metrics', request).then(response => {
      console.log(response);

    })
  }


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


    var series1 = chart.series.push(new am4charts.LineSeries());
    series1.dataFields.valueY = "heartbeat";
    series1.dataFields.dateX = "date";
    series1.name = "heartbeat";
    series1.tooltipText = "{name}: [bold]{valueY}[/]";
    series1.strokeWidth = 3;
    series1.stroke = am4core.color("#FF6F91");
    series1.tooltip.fill = am4core.color("#FF6F91");
    series1.tooltip.getFillFromObject = false;
    series1.tooltip.background.fill = am4core.color("#FF6F91");

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueY = "activity";
    series2.dataFields.dateX = "date";
    series2.name = "activity";
    series2.tooltipText = "{name}: [bold]{valueY}[/]";
    series2.strokeWidth = 3;
    series2.stroke = am4core.color("#D65DB1");
    series2.tooltip.getFillFromObject = false;
    series2.tooltip.background.fill = am4core.color("#D65DB1");



    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.valueY = "distance";
    series3.dataFields.dateX = "date";
    series3.name = "distance";
    series3.tooltipText = "{name}: [bold]{valueY}[/]";
    series3.strokeWidth = 3;
    series3.stroke = am4core.color("#845EC2");
    series3.tooltip.getFillFromObject = false;
    series3.tooltip.background.fill = am4core.color("#845EC2");


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

    document.getElementById("b1m").addEventListener("click", function() {
      let max = dateAxis.groupMax["day1"];
      let date = new Date(max);
      am4core.time.add(date, "month", -1);
      zoomToDates(date);
    });

    document.getElementById("b3m").addEventListener("click", function() {
      let max = dateAxis.groupMax["day1"];
      let date = new Date(max);
      am4core.time.add(date, "month", -3);
      zoomToDates(date);
    });

    document.getElementById("b6m").addEventListener("click", function() {
      let max = dateAxis.groupMax["day1"];
      let date = new Date(max);
      am4core.time.add(date, "month", -6);
      zoomToDates(date);
    });

    document.getElementById("b1y").addEventListener("click", function() {
      let max = dateAxis.groupMax["day1"];
      let date = new Date(max);
      am4core.time.add(date, "year", -1);
      zoomToDates(date);
    });

    document.getElementById("bytd").addEventListener("click", function() {
      let max = dateAxis.groupMax["day1"];
      let date = new Date(max);
      am4core.time.round(date, "year", 1);
      zoomToDates(date);
    });

    document.getElementById("bmax").addEventListener("click", function() {
      let min = dateAxis.groupMin["day1"];
      let date = new Date(min);
      zoomToDates(date);
    });

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

        //call the function with dates
        updateGraph(start,end);

        if ((start.length < inputFieldFormat.length) || (end.length < inputFieldFormat.length)) {
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
.graphCom {
  height: 350px;
  width: 100%;
}
</style>
