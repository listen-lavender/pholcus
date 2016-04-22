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
              'nav': [
                    {name: 'new', label: '创建脚本', path: '/active',}, 
                ]
            }
        }
    }
</script>

<style lang='less'>
  
</style>