<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>name</th>
          <th>group</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result.creator">
            <td>
                <a v-link="{name: 'creator_detail', params: {_id: item._id}}">{{item.username}}</a>
            </td>
            <td>{{item.group}}</td>
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
                default: 'creator'
            }
        },
        computed: {
            getUrl: function() {
                let link = 'creator/list?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            }
        }
    }
</script>
<style lang='less'>
</style>