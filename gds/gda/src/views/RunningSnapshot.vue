<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>状态</th>
          <th>步骤执行器</th>
          <th>优先级</th>
          <th>执行次数</th>
          <th>版本</th>
          <th>相关任务</th>
          <th>参数</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result.work">
            <td>{{item.status}}</td>
            <td>{{item.methodName}}</td>
            <td>{{item.priority}}</td>
            <td>{{item.times}}</td>
            <td>{{item.version}}</td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item.tid}}">查看任务</a>
            </td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item.tid}}">查看参数</a>
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