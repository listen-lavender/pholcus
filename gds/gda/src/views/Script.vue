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
  <a class="item" v-link="{name: 'setting', params: {_id: 1}}">
      <i class="settings icon"></i>
      设置
    </a>
</template>
<script>
    export default {
        data () {
            return {
              result: null,
            }
        },
        ready(){
            this.$http.get('script/list').then((response)=>{
                this.$set('result', response.data.res);
            })
        },
    }
</script>
<style lang='less'>
</style>