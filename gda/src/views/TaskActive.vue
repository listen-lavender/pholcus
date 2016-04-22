<template>
  <ul>
    <li>
      active
    </li>
  </ul>
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
  
</style>