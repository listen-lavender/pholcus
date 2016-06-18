<template>
    <div v-if="result.script && result.script.name">
      <form class="ui form" v-on:submit.prevent="save">
        <div class="ui sizer vertical segment" >
            <div class="ui large header">脚本数据源</div>
        </div>
        <br>
        <div class="field">
            <p class="ui small header">Name</p>
            <p class="ui secondary basic segment">{{result.script.name}}</p>
        </div>
        <div class="field">
            <p class="ui small header">Clsname</p>
            <p class="ui secondary basic segment">{{result.script.clsname}}</p>
        </div>
        <div class="field">
            <p class="ui small header">Desc</p>
            <textarea :value="result.script.desc" v-model="desc" rows="5"></textarea>
        </div>
        <div class="field">
            <p class="ui small header">Script path</p>
            <p class="ui secondary basic segment">{{result.script.filepath}}</p>
        </div>
        <div class="field">
            <p class="ui small header">Script digest</p>
            <p class="ui secondary basic segment">{{result.script.digest}}</p>
        </div>
        <h3>脚本抓取流</h3>
        <div class="ui ordered list">
            <div class="item" v-for="flow in result.script.flows">
                <a v-link="{name: 'step', query: {script_id: result.script._id, flow_id:flow['_id']}}">{{flow['name']}} flow</a>
            </div>
        </div>
        <button class="ui green button" type="submit">
            <i class="save icon"></i>
            保存
        </button>
        <button class="ui button" v-on:click="reset">取消</button>
      </form>
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