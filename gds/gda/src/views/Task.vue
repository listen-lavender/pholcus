<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>name</th>
          <th>description</th>
          <th colspan="4">detail and statistic</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result.task">
            <td>{{item.name}}</td>
            <td>{{item.extra}}</td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item._id}}">view detail</a>
            </td>
            <td>
                <a v-link="{name: 'data', params: {_id: item._id}}">view data</a>
            </td>
            <td>
                <a v-link="{name: 'time', params: {_id: item._id}}">time statistic</a>
            </td>
            <td>
                <a v-link="{name: 'total', params: {_id: item._id}}">quantity statistic</a>
            </td>
        </tr>
    </tbody>
  </table>
  <paginator :index="index" :size="size" :total="result.total"></paginator>
</template>
<script>
    import Paginator from '../mixin/load';
    import Filter from '../mixin/search';
    export default {
        mixins: [Paginator, Filter],
        computed: {
            url: function () {
                let link = 'task/list?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            }
        }
    }
</script>
<style lang='less'>
</style>