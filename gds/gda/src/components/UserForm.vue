<template>
    <div class="ui card uspace" style="width:500px">
        <input type="hidden" id="_id" :value="result.creator._id">
        <form id="avatarform" action="" method="" enctype="multipart/form-data" >
            <input id="avatar" name="avatar" type="file" accept="" style="display:none">
     　　</form>
        <div class="ui image">
            <img class="ui image" :src="result.creator.avatar"/>
        </div>
        <div class="content">
            <a class="header">{{result.creator.username}}</a>
            <div class="meta">
              <span class="date">{{result.creator.create_time}}</span>
            </div>
            <div class="description">{{result.creator.desc}}</div>
        </div>
        <div class="content">
            <div><i class="users icon"></i>group：{{result.creator.group}}</div>
            <div><i class="privacy icon"></i>secret：{{result.creator.secret}}</div>
        </div>
        <div class="content">
            <div class="ui small buttons">
                <a class="ui green button" href="/gds/a/user/password"><i class="keyboard icon"></i>change password</a>
                <a v-link="{name: 'logout'}" class="ui blue button"><i class="sign out icon"></i>sign out</a>
            </div>
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
        route: {
            data(transition){
                this.$http.get('creator/'+this.$route.params._id).then((response)=>{
                    this.$set('result', response.data.res);
                })
            }
        }
    }
</script>
<style lang='less'>
    @import '../../../static/css/semantic/definitions/modules/dimmer.less';
</style>