<template>
    <div v-if="model && model.name">
      <div class="ui form">
        <div class="ui sizer vertical segment" >
            <div class="ui large header"><h3>{{model.clsname}}</h3></div>
        </div>
        <br>
        <div class="field">
            <p class="ui small header">Name</p>
            <input type="text" v-model="model.name">
        </div>
        <div class="field">
            <p class="ui small header">Description</p>
            <textarea v-model="model.desc" rows="5"></textarea>
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
        <div v-if="model.own" class="field">
            <div class="ui small header">Update authorize</div>
            <input type="hidden" v-model="model.select_updators">
            <input type="hidden" v-model="model.unselect_updators">
            <multiselect mark="updators" :selectitems="model.select_updators_options" :unselectitems="model.unselect_updators_options"></multiselect>
        </div>
        <div v-if="model.own" class="field">
            <div class="ui small header">Query authorize</div>
            <input type="hidden" v-model="model.select_queryers">
            <input type="hidden" v-model="model.unselect_queryers">
            <multiselect mark="queryers" :selectitems="model.select_queryers_options" :unselectitems="model.unselect_queryers_options"></multiselect>
        </div>
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
                    let model = response.data.res.script;
                    this.$set('model', model);
                    
                    let select_updators = model.select_updators;
                    let select_queryers = model.select_queryers;
                    let all_options = model.creators;
                    this.set_options('updators', select_updators, all_options);
                    this.set_options('queryers', select_queryers, all_options);
                    this.$set('model.unselect_updators', '');
                    this.$set('model.unselect_queryers', '');
                })
            }
        },
        events: {
            selectmulti:function(mark, selectIds, unselectIds) {
                this.$set('model.select_'+mark, selectIds);
                this.$set('model.unselect_'+mark, unselectIds);
            },
        },
        methods: {
            update(){
                this.$http.post('script/'+this.$route.params._id, {'desc':this.model.desc, 'name':this.model.name, 'select_updators':this.model.select_updators, 'unselect_updators':this.model.unselect_updators, 'select_queryers':this.model.select_queryers, 'unselect_queryers':this.model.unselect_queryers}).then((response)=>{
                    let user = response.data.res.user;
                    if(user == null){
                        console.log(response.data.res.msg);
                    }
                    else{
                        this.$route.router.go({name: 'script'});
                    }
                })
            },
            set_options(mark, select_ids, all_options){
                let select_options = [];
                let unselect_options = [];
                for(let k=0; k<all_options.length; k++)
                    if(select_ids.indexOf(all_options[k].value) > -1)
                        select_options.push(all_options[k]);
                    else
                        unselect_options.push(all_options[k]);
                this.$set('model.select_'+mark+'_options', select_options);
                this.$set('model.unselect_'+mark+'_options', unselect_options);
            }
        }
    }
</script>
<style lang='less'>
</style>