<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th class="sorted descending" >id</th>
          <th>名称</th>
        </tr>
    </thead>
    <tbody >
        <tr v-for="item in result.tasks"  >
            <td>{{item._id}}</td>
            <td>
                <a v-link="{name: 'detail', params: {_id: item._id}}">{{item.name}}</a>
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
            this.$http.get('p/task/list').then((response)=>{
                this.$set('result', response.data.result);
            })
        },
    }
</script>

<style lang='less'>
  
</style>