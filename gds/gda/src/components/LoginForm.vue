<template>
  <top></top>
  <div class="ui bottom attached segment pushable">
    <div class="ui raised segment signin">
      <h3 class="ui inverted blue block header"> SIGN IN </h3>
      <div class="ui two column grid basic segment">
        <div class="column">
          <div class="ui blue stacked segment">
              <!-- form here -->
              <div class="ui form">
                <div class="field">
                  <label> Username </label>
                  <div class="ui left labeled icon input">
                    <input type="text" v-model="username">
                    <i class="user icon"></i>
                  </div>
                </div>
                <div class="field">
                  <label> Password </label>
                  <div class="ui left labeled icon input">
                    <input type="password" v-on:keyup.enter="login" v-model="password">
                    <i class="lock icon"></i>
                  </div>
                </div>
                <div class="inline field">
                  <div class="ui checkbox">
                    <input id="remember" type="checkbox">
                    <label for="remember"> Remember me </label>
                  </div>
                </div>
                <div class="ui red submit button" v-on:click="login"> Sign In </div>
              </div>
          </div>
        </div>
        <div class="ui vertical divider"> OR </div>
        <div class="center aligned column">
          <h4 class="ui header"> Sign in with: </h4>
          <a class="item" href='https://github.com/'>Github</a>
          <a class="item" href='https://github.com/'>微信</a>
          <a class="item" href='https://github.com/'>微博</a>
          <a class="item" href='https://github.com/'>QQ</a>
          <!-- <div class="ui button">
            <i class="icon"></i>
            Github
          </div>
          <div class="ui button">
            <i class="icon"></i>
            微信
          </div>
          <div class="ui button">
            <i class="icon"></i>
            微博
          </div>
          <div class="ui button">
            <i class="icon"></i>
            QQ
          </div> -->
        </div>
      </div>
      <div class="ui divider"></div>
      <div class="footer">
        <!-- text plus button here -->
        <div class="text"> Not a member? </div>
        <a class="item" v-link="{name: 'register'}">
          <div class="ui vertical animated blue mini button signup">
            <div class="visible content"> Join Us </div>
            <div class="hidden content">
              <i class="users icon"></i>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>
<script>
    export default {
        methods: {
            sendUid(_id){
              this.$dispatch('receiveUid', _id)
            },
            login(){
              if(this.username == ''){
                  return
              }
              if(this.password == ''){
                  return
              }
              this.$http.post('creator/login', {'username':this.username, 'password':this.password}).then((response)=>{
                  let user = response.data.res.user;
                  if(user == null){
                    console.log(response.data.res.msg);
                  }
                  else{
                    this.$route.router.go({name: 'home'});
                    this.$dispatch('receiveUid', user._id);
                    // sendUid(user._id)
                  }
              })
            }
        }
    }
</script>
<style lang='less'>
</style>