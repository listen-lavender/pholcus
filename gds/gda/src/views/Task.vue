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
               msg: 'Hello Vue!',
                'nav': [
                    {name: 'active', label: '活动任务', path: '/active',}, 
                    {name: 'monitor', label: '任务监控', path: '/monitor'},
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