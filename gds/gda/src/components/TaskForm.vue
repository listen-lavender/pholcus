<template>
  <div class="ui  segment">
    <div class="ui form basic segment">
      <h3>Basic</h3>
      <div class="field">
        <label>name</label>
        <input type="text" v-model="model.name">
      </div>
      <div class="field">
        <label>Description</label>
        <textarea class="ui input" v-model="model.extra" id="" cols="30" rows="5"></textarea>
      </div>
      <h3>Control</h3>
      <div class="two fields">
          <div class="field">
            <label>Category</label>
            <input type="text" v-model="model.category">
          </div>
          <div class="field">
            <label>Tag</label>
            <input type="text" v-model="model.tag">
          </div>
      </div>
      <div class="two fields">
          <div class="field">
            <label>Task type</label>
            <select class="ui dropdown" v-model="model.type">
              <option v-for="option in model.type_options" :value="option.value">{{option.text}}
              </option>
            </select>
          </div>
          <div class="field">
            <label>Exe span</label>
            <input type="text" v-model="model.period">
          </div>
      </div>
      <div class="three fields">
        <cascade :items="items"></cascade>
      </div>
      <div class="field">
        <label>params</label>
        <input type="text" v-model="model.params">
      </div>
      <div class="field">
        <label>Push interface</label>
        <input type="url" v-model="model.push_url">
      </div>
      <div class="field">
        <label>Pull interface</label>
        <p class="ui secondary basic segment">
          {{model.pull_url}}
        </p>
      </div>
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
      <div class="field">
        <div v-if="!model._id" class="ui green button" @click="save">
            <i class="save icon"></i>
            Save
        </div>
        <div v-if="model.updatable" class="ui green button" @click="update">
            <i class="save icon"></i>
            Update
        </div>
        <div v-if="saveorupdate" class="ui green button" @click="cancel">
            <i class="cancel icon"></i>
            Cancel
        </div>
        <div v-if="model._id" class="ui green button" @click="clone">
            <i class="copy icon"></i>
            Clone
        </div>
      </div>
    </div>
    
  </div>
</template>
<script>
    export default {
        data () {
            return {
              model:{
                '_id':null,
                'name':null,
                'extra':null,
                'category':null,
                'tag':null,
                'type':null,
                'period':null,
                'params':null,
                'push_url':null,
                'aid':null,
                'fid':null,
                'sid':null,
                'own':false,
                'updatable':false,
              },
              items:[]
            }
        },
        computed: {
            saveorupdate: function() {
                return this.model.updatable || !this.model._id;
            },
        },
        route: {
            data(transition){
                if(!(this.$route.params._id == ':_id'))
                  this.$set('model._id', this.$route.params._id);
                if(this.model._id)
                  this.$http.get('task/detail/'+this.model._id).then((response)=>{
                      let model = response.data.res.task;
                      let items = [];
                      items.push(model.article);
                      delete model['article'];
                      items.push(model.flow);
                      delete model['flow'];
                      items.push(model.section);
                      delete model['section'];
                      this.$set('items', items);

                      this.$set('model', model);

                      let select_updators = model.select_updators;
                      let select_queryers = model.select_queryers;
                      let all_options = model.creators;
                      this.set_options('updators', select_updators, all_options);
                      this.set_options('queryers', select_queryers, all_options);
                      this.$set('model.unselect_updators', '');
                      this.$set('model.unselect_queryers', '');
                  })
                else
                  console.log('null');
            }
            // data(transition){
            //     let response_data = {}
            //     return this.$http.get('p/task/detail/'+this.$route.params._id).then((response)=>{
            //         response_data.model = response.data.result.task
            //         return this.$http.get('p/task/flows', {'aid': response_data.model.aid})
            //     }).then((response)=>{
            //         response_data.flows = response.data
            //         return this.$http.get('p/task/sections', {'aid': response_data.model.aid, 'flow': response_data.model.flow})
            //     }).then((response)=>{
            //         response_data.sections = response.data
            //         return this.$http.get('p/task/articles')
            //     }).then((response)=>{
            //         response_data.articles = response.data
            //         return response_data
            //     })
            // }
        },
        methods: {
            update(){
              this.$http.post('task/detail/'+this.$route.params._id, {'name':this.model.name, 'extra':this.model.extra, 'category':this.model.category, 'tag':this.model.tag, 'type':this.model.type, 'period':this.model.period, 'aid':this.model.aid, 'fid':this.model.fid, 'sid':this.model.sid, 'params':this.model.params, 'push_url':this.model.push_url, 'select_updators':this.model.select_updators, 'unselect_updators':this.model.unselect_updators, 'select_queryers':this.model.select_queryers, 'unselect_queryers':this.model.unselect_queryers}).then((response)=>{
                  let user = response.data.res.user;
                  if(user == null){
                    console.log(response.data.res.msg);
                  }
                  else{
                    this.$route.router.go({name: 'task'});
                  }
              })
            },
            save(){
              this.$http.post('task/detail', {'name':this.model.name, 'extra':this.model.extra, 'category':this.model.category, 'tag':this.model.tag, 'type':this.model.type, 'period':this.model.period, 'aid':this.model.aid, 'fid':this.model.fid, 'sid':this.model.sid, 'params':this.model.params, 'push_url':this.model.push_url, 'select_updators':this.model.select_updators, 'unselect_updators':this.model.unselect_updators, 'select_queryers':this.model.select_queryers, 'unselect_queryers':this.model.unselect_queryers}).then((response)=>{
                  let user = response.data.res.user;
                  if(user == null){
                    console.log(response.data.res.msg);
                  }
                  else{
                    this.$route.router.go({name: 'task'});
                  }
              })
            },
            cancel(){
              
            },
            clone(){
              this.$set('model._id', null);
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
        },
        events: {
            modify:function(key, val) {
                this.$set('model.' + key, val);
            },
            selectmulti:function(mark, selectIds, unselectIds) {
                this.$set('model.select_'+mark, selectIds);
                this.$set('model.unselect_'+mark, unselectIds);
            },
        }
    }
</script>

<style lang='less'>
  
</style>