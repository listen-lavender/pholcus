<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th v-for="col in result.column">{{col}}</th>
        </tr>
    </thead>
    <tbody >
        <tr v-for="row in result.data">
            <td v-for="col in result.column">
                <a href='{{row[col]}}' target="_blank" v-if="row[col].indexOf('http') == 0">{{row[col]}}</a>
                <span v-else>{{row[col]}}</span>
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
                let link = 'task/'+this.$route.params._id+'/data?skip='+((this.index-1) * this.size)+'&limit='+this.size;
                if(this.keyword)
                    link = link + '&keyword=' + this.keyword;
                return link;
            }
        }
    }
</script>
<style lang='less'>
</style>