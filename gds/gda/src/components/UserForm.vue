<template>
    <div class="ui card" style="width:500px">
        <input type="hidden" id="_id" :value="result.user._id">
        <form id="avatarform" action="" method="" enctype="multipart/form-data" >
            <input id="avatar" name="avatar" type="file" accept="" style="display:none">
     　　</form>
        <div class="ui image">
            <img class="ui image" :src="result.user.avatar"/>
        </div>
        <div class="content">
            <a class="header">{{result.user.username}}</a>
            <div class="meta">
              <span class="date">{{result.user.create_time}}</span>
            </div>
            <div class="description">{{result.user.desc}}</div>
        </div>
        <div class="content">
            <div><i class="users icon"></i>类别：{{result.user.group}}</div>
            <div><i class="privacy icon"></i>密钥：{{result.user.secret}}</div>
            <div><i class="cube icon"></i>状态：{{result.user.status}}</div>
            <div><i class="keyboard icon"></i><a class="item" href="/gds/a/user/password">更换密码</a></div>
            <div><i class="sign out icon"></i><a class="item" v-link="{name: 'logout'}">sign out</a></div>
        </div>
    </div>
</template>
<script>
    export default {
        data () {
            return {
              result: null,
            }
        },
        ready(){
            this.$http.post('creator/login').then((response)=>{
                this.$set('result', response.data.res);
            })
        },
    }
</script>
<style lang='less'>
    @import '../../../static/css/semantic/definitions/modules/dimmer.less';
</style>