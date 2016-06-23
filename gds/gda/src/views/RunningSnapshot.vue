<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>status</th>
          <th>executor</th>
          <th>priority</th>
          <th>times</th>
          <th>version</th>
          <th>log</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result.work">
            <td>{{item.status}}</td>
            <td>{{item.name}}</td>
            <td>{{item.priority}}</td>
            <td>{{item.times}}</td>
            <td>{{item.version}}</td>
            <td>
                <a v-link="{name: 'runninglog', params: {_id: item._id}}">view</a>
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
            getUrl: function () {
                let link = 'running/snapshot?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            }
        }
    }
</script>
<style lang='less'>
</style>