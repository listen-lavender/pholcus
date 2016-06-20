<template>
  <div class="ui top attached large menu">
    <a class="item" v-on:click="goindex">
      <i class="home icon"></i>
      Home
    </a>
    <div class="right menu" v-if="flag">
      <div class="ui mini icon input">
        <input type="text" placeholder="Search..." v-on:keyup.enter="search" v-model="keyword">
        <i class="search icon"></i>
      </div>
    </div>
  </div>
</template>
<script>
    export default {
        props: {
            model: {
                type: String,
                default: ''
            },
            flag: {
                type: Boolean,
                default: false
            },
        },
        events: {
            getModel:function(model) {
              if(this.model != model){
                this.$set('model', model);
                this.$set('keyword', '');
              }
            },
            updateFlag: function(flag){
              this.$set('flag', flag);
            },
        },
        methods: {
            goindex(){
              this.$route.router.go({name:'index'});
            },
            search(){
              this.$dispatch('setFilter', this.model, this.keyword);
            }
        }
    }
</script>
<style lang='less'>
</style>