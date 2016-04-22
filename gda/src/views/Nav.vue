<template>
    <div class="ui red three item menu">
      <a class="active item">
        Home
      </a>
      <a class="item">
        Messages
      </a>
      <a class="item">
        Friends
      </a>
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
              msg: 'Hello Vue!'
            }
        }
    }
</script>

<style lang='less'>
  .m-siderbar {
    box-shadow: none !important;
    border-top: none !important;
    border-bottom: none !important;
  }
</style>