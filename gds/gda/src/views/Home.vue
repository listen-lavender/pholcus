<template>
  <router-view :_id=_id></router-view>
</template>
<script>
    import {getLocal} from '../util'
    export default {
        props: {
          _id: {
            type: String
          }
        },
        ready(){
            this.$set('_id', getLocal('uid'))
        },
        events: {
            receiveUid:function(_id) {
                this.$set('_id', _id)
            }
        }
    }
</script>
<style lang='less'>
</style>