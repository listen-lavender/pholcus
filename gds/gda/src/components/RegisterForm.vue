<template>
  <div class="ui bottom attached segment pushable" v-if="!loggined">
    <div class="ui raised segment signup inactive">
      <h3 class="ui inverted blue block header"> SIGN UP </h3>
      <div class="ui blue stacked segment">
        <!-- form here -->
        <div class="ui form">
          <div class="two fields">
            <div class="field">
              <!-- Username here -->
              <label> Username </label>
              <div class="ui left labeled icon input">
                <input id="username" placeholder="e.g., Tarzan" type="text">
                <i class="user icon"></i>
                <div class="ui corner label">
                  <i class="asterisk icon"></i>
                </div>
              </div>
            </div>
            <div class="field">
              <!-- Email here -->
              <label> Email </label>
              <div class="ui left labeled icon input">
                <input id="email" placeholder="e.g., tarzan@jungle.org" type="text">
                <i class="mail icon"></i>
                <div class="ui corner label">
                  <i class="asterisk icon"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="two fields">
            <div class="field">
              <!-- Password here -->
              <label> Password </label>
              <div class="ui left labeled icon input">
                <input id="password" placeholder="e.g., !@#$%^&amp;*()_+:)" type="password">
                <i class="lock icon"></i>
                <div class="ui corner label">
                  <i class="asterisk icon"></i>
                </div>
              </div>
            </div>
            <div class="field">
              <!-- Confirm Password here -->
              <label> Confirm Password </label>
              <div class="ui left labeled icon input">
                <input id="confirm-password" placeholder="e.g., !@#$%^&amp;*()_+:)" type="password">
                <i class="lock icon"></i>
                <div class="ui corner label">
                  <i class="asterisk icon"></i>
                </div>
              </div>
            </div>
          </div>
          <div class="inline field">
            <!-- checkbox here -->
            <div class="ui checkbox">
              <input id="terms" type="checkbox">
              <label for="terms"> I agree to the <a href="#"> Terms and Conditions </a></label>
            </div>
          </div>
          <div class="ui red submit button"> Sign Up </div>
          <div class="ui error message"></div>
        </div>
      </div>
      <div class="ui divider"></div>
      <div class="footer">
        <div class="text"> Already a member? </div>
        <div class="ui vertical animated blue mini button signin">
          <div class="visible content"> Log In </div>
          <div class="hidden content">
            <i class="sign in icon"></i>
          </div>
        </div>
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