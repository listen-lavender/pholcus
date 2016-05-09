<template>
  <a>abc</a>
  <top :loggined="loggined"></top>
  <nav-menu :loggined="loggined"></nav-menu>
  <router-view :loggined="loggined"></router-view>
  <!-- <login :loggined="loggined"></login> -->
</template>
<script>
    export default {
        props: {
            loggined: {
                type: Boolean,
                default: false,
            }
        },
    }
</script>
<style lang='less'>
</style>