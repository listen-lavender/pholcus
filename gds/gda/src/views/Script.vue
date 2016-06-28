<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>name</th>
          <th>description</th>
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
            <td>
                <a v-if="item.queryable" v-link="{name: 'script_detail', params: {_id: item._id}}">{{item.name}}</a>
                <span v-else>{{item.name}}</span>
            </td>
            <td>{{item.desc}}</td>
            <td>
                <div v-if="item.own" class="ui checkbox">
                    <input type="checkbox" v-model="item.deleted">
                    <label><a v-on:click="remove(item)"><i class="remove icon"></i></a></label>
                </div>
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
            datakey: {
                type: String,
                default: 'script'
            },
        },
        computed: {
            getUrl: function () {
                let link = 'script/list?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            }
        }
    }
</script>
<style lang='less'>
</style>