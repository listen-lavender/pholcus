<template>
  <top></top>
  <div class="ui bottom attached segment pushable">
    <div class="ui visible left vertical sidebar menu m-siderbar">
        <a class="item" v-link="{name: 'task'}">
          <i class="tasks icon"></i>
          任务
        </a>
        <a class="item" v-link="{name: 'script'}">
          <i class="code icon"></i>
          脚本
        </a>
        <a class="item" v-link="{name: 'creator'}">
          <i class="user icon"></i>
          用户
        </a>
        <a class="item" v-link="{name: 'setting', params: {_id: 1}}">
          <i class="settings icon"></i>
          设置
        </a>
    </div>
    <div class="pusher">
        <router-view></router-view>
    </div>
  </div>
</template>
<script>
</script>
<style lang='less'>
</style>