<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>name</th>
          <th>description</th>
          <th>edit</th>
          <th colspan="3">statistic</th>
          <th>
            <div class="ui checkbox">
                <input type="checkbox" v-model="deleted">
                <label><a v-on:click="removeAll"><i class="remove icon"></i></a></label>
            </div>
          </th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result">
            <td>{{item.name}}</td>
            <td>{{item.extra}}</td>
            <td>
                <a v-if="item.queryable" v-link="{name: 'task_detail', params: {_id: item._id}}"><i class="edit icon"></i></a>
            </td>
            <td>
                <a v-if="item.queryable" v-link="{name: 'data', params: {_id: item._id}}"><i class="database icon"></i></a>
            </td>
            <td>
                <a v-link="{name: 'time', params: {_id: item._id}}">timeline</a>
            </td>
            <td>
                <a v-link="{name: 'total', params: {_id: item._id}}">quantityline</a>
            </td>
            <td>
                <div v-if="item.own" class="ui checkbox">
                    <input type="checkbox" v-model="item.deleted">
                    <label><a v-on:click="remove(item)"><i class="remove icon"></i></a></label>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="7" align="center">
                <a v-link="{name: 'task_detail'}"><i class="plus icon"></i></a>
            </td>
        </tr>
    </tbody>
  </table>
  <paginator :index="index" :size="size" :total="total"></paginator>
</template>
<script>
    import Paginator from '../mixin/load';
    import Filter from '../mixin/search';
    export default {
        mixins: [Paginator, Filter],
        props: {
            datakey: {
                type: String,
                default: 'task'
            },
        },
        computed: {
            getUrl: function () {
                let link = 'task/list?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            },
        }
    }
</script>
<style lang='less'>
</style>