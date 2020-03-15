<template>
  <q-card class='full-width'>
    <q-card-section>
      <div class="text-h6">Calories data for {{$store.state.main.view_user}}</div>
    </q-card-section>
    <q-separator />
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
      graphC: ''
    }
  },
  mounted () {

    const domain = this.$store.state.main.domain
    const user = this.$store.state.main.view_user

    let chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart)
    chart.hiddenState.properties.opacity = 0

    chart.padding(0, 0, 0, 0)

    chart.zoomOutButton.disabled = true

    // Create chart instance
    chart.scrollbarX = new am4core.Scrollbar();

    chart.data = []

    function updateGraph () {

      var request = {
      params: {
        type: 'calories',
        username: user
      }
    }

  axios.get(domain + '/get_metrics', request).then(response => {
      console.log(response);
      console.log(new Date(response.data.metrics[0].timestamp));

      chart.data = []
      response.data.metrics.forEach(function(metric){
        chart.data.push({'timestamp': (new Date(metric.timestamp)).toISOString() ,'amount':metric.amount});
      });
      console.log(chart.data);
      update();
    })
  }

  updateGraph();


function update(){
              // Create axes
              let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
              categoryAxis.dataFields.category = "timestamp";
              categoryAxis.renderer.grid.template.location = 0;
              categoryAxis.renderer.minGridDistance = 30;
              categoryAxis.renderer.labels.template.horizontalCenter = "right";
              categoryAxis.renderer.labels.template.verticalCenter = "middle";
              categoryAxis.renderer.labels.template.rotation = 270;
              categoryAxis.tooltip.disabled = true;
              categoryAxis.renderer.minHeight = 110;

              let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
              valueAxis.renderer.minWidth = 50;

              // Create series
              let series = chart.series.push(new am4charts.ColumnSeries());
              series.sequencedInterpolation = true;
              series.dataFields.valueY = "amount";
              series.dataFields.categoryX = "timestamp";
              series.tooltipText = "[{categoryX}: bold]{valueY}[/]";
              series.columns.template.strokeWidth = 0;

              series.tooltip.pointerOrientation = "vertical";

              series.columns.template.column.cornerRadiusTopLeft = 10;
              series.columns.template.column.cornerRadiusTopRight = 10;
              series.columns.template.column.fillOpacity = 0.8;

              // on hover, make corner radiuses bigger
              let hoverState = series.columns.template.column.states.create("hover");
              hoverState.properties.cornerRadiusTopLeft = 0;
              hoverState.properties.cornerRadiusTopRight = 0;
              hoverState.properties.fillOpacity = 1;

              series.columns.template.adapter.add("fill", function(fill, target) {
                return chart.colors.getIndex(target.dataItem.index);
              });



                // Cursor
                chart.cursor = new am4charts.XYCursor();


                this.graphC = chart
              }
        },

      beforeDestroy () {
        if (this.graphC) {
          this.graphC.dispose()
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
