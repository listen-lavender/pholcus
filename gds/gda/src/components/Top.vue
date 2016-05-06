<template v-if="loggined">
  <div class="ui top attached large menu">
    <a class="item">
      <i class="home icon"></i>
      Home
    </a>
    <div class="right menu" v-if="loggined">
      <div class="ui mini icon input">
        <input type="text" placeholder="Search...">
        <i class="search icon"></i>
      </div>
    </div>
  </div>
</template>
<script>
    export default {
        props: {
            loggined: {
                type: Boolean,
                default: false,
            },
        },
    }
</script>
<style lang='less'>
</style>