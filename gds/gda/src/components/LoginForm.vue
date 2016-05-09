<template>
  <div class="ui bottom attached segment pushable" v-if="!loggined">
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
                    <input type="text">
                    <i class="user icon"></i>
                  </div>
                </div>
                <div class="field">
                  <label> Password </label>
                  <div class="ui left labeled icon input">
                    <input type="password">
                    <i class="lock icon"></i>
                  </div>
                </div>
                <div class="inline field">
                  <div class="ui checkbox">
                    <input id="remember" type="checkbox">
                    <label for="remember"> Remember me </label>
                  </div>
                </div>
                <div class="ui red submit button"> Sign In </div>
              </div>
          </div>
        </div>
        <div class="ui vertical divider"> OR </div>
        <div class="center aligned column">
          <h4 class="ui header"> Sign in with: </h4>
          <div class="ui button">
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
          </div>
        </div>
      </div>
      <div class="ui divider"></div>
      <div class="footer">
        <!-- text plus button here -->
        <div class="text"> Not a member? </div>
        <a class="item" v-link="{name: 'register'}">
          <i class="settings icon"></i>
          设置
        </a>
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