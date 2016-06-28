<template>
    <div v-if="model && model.name">
      <div class="ui form">
        <div class="ui sizer vertical segment" >
            <div class="ui large header"><h3>{{model.clsname}}</h3></div>
        </div>
        <br>
        <div class="field">
            <p class="ui small header">Name</p>
            <input type="text" :value="model.name" v-model="name">
        </div>
        <div class="field">
            <p class="ui small header">Description</p>
            <textarea :value="model.desc" v-model="desc" rows="5"></textarea>
        </div>
        <div class="field">
            <p class="ui small header">Script path</p>
            <p class="ui secondary basic segment">{{model.filepath}}</p>
        </div>
        <div class="field">
            <p class="ui small header">Script digest</p>
            <p class="ui secondary basic segment">{{model.digest}}</p>
        </div>
        <hr/>
        <div class="ui ordered list">
            <div class="item" v-for="flow in model.flows">
                <a v-link="{name: 'step', query: {script_id: model._id, flow_id:flow['_id']}}">{{flow['name']}} flow</a>
            </div>
        </div>
        <br>
        <br>
        <br>
        <div class="field">
            <div v-if="model.updatable" class="ui green button" @click="update">
                <i class="save icon"></i>
                Save
            </div>
        </div>
      </div>
    </div>
</template>
<script>
    export default {
        data () {
            return {
              model: null,
            }
        },
        route: {
            data(transition){
                this.$http.get('script/'+this.$route.params._id).then((response)=>{
                    this.$set('model', response.data.res.script);
                })
            }
        },
        methods: {
            update(){
                this.$http.post('script/'+this.$route.params._id, {'desc':this.desc, 'name':this.name}).then((response)=>{
                    let user = response.data.res.user;
                    if(user == null){
                        console.log(response.data.res.msg);
                    }
                    else{
                        this.$route.router.go({name: 'script'});
                    }
                })
            }
        }
    }
</script>
<style lang='less'>
</style>