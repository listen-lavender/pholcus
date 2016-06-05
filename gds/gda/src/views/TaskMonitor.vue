<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>名称</th>
          <th>描述</th>
          <th colspan="5">详情统计</th>
        </tr>
    </thead>
    <tbody >
        <tr v-for="item in result.task">
            <td>{{item.name}}</td>
            <td>{{item.extra}}</td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item._id}}">任务详情</a>
            </td>
            <td>
                <a v-link="{name: 'data', params: {_id: item._id}}">任务数据</a>
            </td>
            <td>
                <a v-link="{name: 'time', params: {_id: item._id}}">任务耗时</a>
            </td>
            <td>
                <a v-link="{name: 'total', params: {_id: item._id}}">任务结果</a>
            </td>
            <td>
                <a v-link="{name: 'log', params: {_id: item._id}}">任务日志</a>
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
        props: {
            model: {
                type: String,
                default: 'task'
            }
        },
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