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
</template>
<script>
    export default {
        data () {
            return {
              result: null,
            }
        },
        ready(){
            this.$http.get('task/'+this.$route.params._id+'/data').then((response)=>{
                this.$set('result', response.data.res);
            })
        },
    }
</script>
<style lang='less'>
</style>