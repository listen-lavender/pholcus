<template>
  <div class="ui grid">
    <div class="row">
        <top></top>
    </div>
  </div>
  <div class="ui grid basic segment">
    <div class="three wide column">
        <div class="ui secondary vertical pointing fluid menu m-siderbar">
            <a class="item" v-link="{name: 'runningsnapshot'}">
              <i class="tasks icon"></i>
              Running Snapshot
            </a>
            <a class="item" v-link="{name: 'task'}">
              <i class="tasks icon"></i>
              Task
            </a>
            <a class="item" v-link="{name: 'script'}">
              <i class="code icon"></i>
              Script
            </a>
            <a class="item" v-link="{name: 'creator'}">
              <i class="user icon"></i>
              User
            </a>
            <a class="item" v-link="{name: 'setting', 'params':{'_id':_id}}">
              <i class="settings icon"></i>
              Setting
            </a>
        </div>
    </div>
    <div class="thirteen wide stretched column">
        <router-view></router-view>
    </div>
  </div>
</template>
<script>
    export default {
        props: {
          _id: {
            type: String
          }
        },
        events: {
            getModel:function(model) {
              this.$broadcast('getModel', model);
            },
            setFilter:function(model, keyword) {
              this.$broadcast('setFilter', model, keyword);
            },
            updateFlag:function(flag) {
              this.$broadcast('updateFlag', flag);
            },
        },
    }
</script>
<style lang='less'>
</style>