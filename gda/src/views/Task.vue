<template>
  <div class="ui secondary pointing menu" >
    <a v-link="{name: item.name}" class="item" v-for="item in nav" >{{item.label}}</a>
  </div>
  <div class="ui basic segment">
    <router-view></router-view>
  </div>
</template>
<script>
    export default {
        data () {
            return {
              // note: changing this line won't causes changes
              // with hot-reload because the reloaded component
              // preserves its current state and we are modifying
              // its initial state.
                msg: 'Hello Vue!',
                'nav': [
                    {name: 'active', label: '活动任务', path: '/active',}, 
                    {name: 'monitor', label: '任务监控', path: '/monitor'},
                    {name: 'manage', label: '任务管理', path: '/manage'}
                ]
            }
        },
        route: {
          data: function(){
            
          }
        }
    }
</script>

<style lang='less'>
  
</style>