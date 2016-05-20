<template>
  <router-view :_id=_id></router-view>
</template>
<script>
    export default {
        props: {
          _id: {
            type: String
          }
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