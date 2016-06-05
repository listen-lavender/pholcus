<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>名称</th>
          <th>描述</th>
        </tr>
    </thead>
    <tbody >
        <tr v-for="item in result.script">
            <td>
                <a v-link="{name: 'script_detail', params: {_id: item._id}}">{{item.name}}</a>
            </td>
            <td>{{item.desc}}</td>
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
                default: 'script'
            }
        },
        computed: {
            url: function () {
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