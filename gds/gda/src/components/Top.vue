<template>
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
    import LoginState from '../mixin/login';
    export default {
        mixins: [LoginState],
    }
</script>
<style lang='less'>
</style>