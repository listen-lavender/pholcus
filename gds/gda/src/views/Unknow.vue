<template>
  <div>code: {{code}}</div>
  <div>msg: {{msg}}</div>
</template>
<script>
      import {getLocal} from '../util'
      export default {
        data () {
            return {
              code:-1,
              msg:'unknow',
            }
        },
        route: {
            data(transition){
                this.$set('code', getLocal('code'))
                this.$set('msg', getLocal('msg'))
            }
        }
      }
</script>
<style lang='less'>
</style>