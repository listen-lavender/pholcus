<template>
  <table class="ui fixed celled table">
    <thead>
        <tr>
          <th>状态</th>
          <th>步骤执行器</th>
          <th>优先级</th>
          <th>执行次数</th>
          <th>相关任务</th>
          <th>参数</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="item in result.work">
            <td>{{item.status}}</td>
            <td>{{item.methodName}}</td>
            <td>{{item.priority}}</td>
            <td>{{item.times}}</td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item._id}}">查看任务</a>
            </td>
            <td>
                <a v-link="{name: 'task_detail', params: {_id: item._id}}">查看参数</a>
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
            this.$http.get('task/activity').then((response)=>{
                this.$set('result', response.data.res);
            })
        },
    }
</script>
<style lang='less'>
</style>