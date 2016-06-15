<template>
  <form class="ui form" v-on:submit.prevent="save">
    <div class="ui sizer vertical segment" >
        <div class="ui large header">脚本数据源</div>
    </div>
    <div class="field">
        <label>name: </label><span>{{result.script.name}}</span>
    </div>
    <div class="field">
        <label>clsname: </label><span>{{result.script.clsname}}</span>
    </div>
    <div class="field">
        <label>desc: </label><input type="text" :value="result.script.desc" v-model="desc">
    </div>
    <div class="field">
        <label>script path: </label><span>{{result.script.filepath}}</span>
    </div>
    <div class="field">
        <label>script digest: </label><span>{{result.script.digest}}</span>
    </div>
    <div class="field" v-for="flow in result.script.flows">
        <a v-link="{name: 'step', query: {script_id: result.script._id, flow_id:flow['_id']}}">{{flow['name']}} flow</a>
    </div>
    <button class="ui primary button" type="submit">保存</button>
    <button class="ui button" v-on:click="reset">取消</button>
  </form>
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
                this.$http.get('script/'+this.$route.params._id).then((response)=>{
                    this.$set('result', response.data.res);
                })
            }
        },
        methods: {
            save(){
                this.$http.post('script/'+this.$route.params._id, {'desc':this.desc}).then((response)=>{
                    let user = response.data.res.user;
                    if(user == null){
                        console.log(response.data.res.msg);
                    }
                    else{
                        this.$route.router.go({name: 'script'});
                    }
                })
            },
            reset(){
                this.$set('desc', '')
            }
        }
    }
</script>
<style lang='less'>
</style>