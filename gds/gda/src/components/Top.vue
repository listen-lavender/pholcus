<template>
  <div class="ui top attached large menu">
    <a class="item" v-on:click="goindex">
      <i class="home icon"></i>
      Home
    </a>
    <div class="right menu" v-if="loggined">
      <div class="ui mini icon input">
        <input type="text" placeholder="Search..." v-on:keyup.enter="search" v-model="keyword">
        <i class="search icon"></i>
      </div>
    </div>
  </div>
</template>
<script>
    import LoginState from '../mixin/login';
    export default {
        mixins: [LoginState],
        props: {
            model: {
                type: String,
                default: ''
            },
        },
        events: {
            getModel:function(model) {
              if(this.model != model){
                this.$set('model', model);
                this.$set('keyword', '');
              }
            }
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