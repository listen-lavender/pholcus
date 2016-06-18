<template>
    <div class="vue-chart-container">
    <div class="vue-chart" id="{{chartId}}"></div>
    </div>
</template>
<script>
    import _ from 'lodash'
    import {bind, loadChart, deferred, listen} from '../util';

    const chartDeferred = deferred()

    export default {
      props: {
        packages: {
          type: Array,
          default: () => {
            return ['corechart']
          }
        },
        version: {
          default: 'current'
        },
        chartType: {
          type: String,
          default: () => {
            return 'LineChart'
          }
        },
        chartEvents: {
          type: Object,
          default: () => {
            return {}
          }
        },
        columns: {
          required: true,
          type: Array
        },
        rows: {
          type: Array,
          default: () => {
            return []
          }
        },
        options: {
          type: Object,
          default: () => {
            return {
              chart: {
                title: 'Chart Title',
                subtitle: 'Subtitle'
              },
              hAxis: {
                title: 'X Label'
              },
              vAxis: {
                title: 'Y Label'
              },
              width: '400px',
              height: '300px',
              animation: {
                duration: 500,
                easing: 'out'
              }
            }
          }
        }
      },
      data () {
        return {
          chart: null,
          chartId: 'X' + this._uid,
          wrapper: null,
          datatable: [],
          hiddenColumns: []
        }
      },
      ready () {
      }
    }
</script>
<style lang='less'>
</style>