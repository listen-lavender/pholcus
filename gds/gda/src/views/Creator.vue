<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>名称</th>
          <th>级别</th>
        </tr>
    </thead>
    <tbody >
        <tr v-for="item in result.creator">
            <td>
                <a v-link="{name: 'creator_detail', params: {_id: item._id}}">{{item.username}}</a>
            </td>
            <td>{{item.group}}</td>
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
            this.$http.get('creator/list').then((response)=>{
                this.$set('result', response.data.res);
            })
        },
    }
</script>
<style lang='less'>
</style>