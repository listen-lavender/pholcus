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
            <div class="ui small header">Authorize</div>
            <select class="ui search selection dropdown" multiple id="multi-select">
            </select>
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
                      this.$set('model', model);
                      this.$set('items', items);
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
              this.$http.post('task/detail/'+this.$route.params._id, {'name':this.model.name, 'extra':this.model.extra, 'category':this.model.category, 'tag':this.model.tag, 'type':this.model.type, 'period':this.model.period, 'aid':this.model.aid, 'fid':this.model.fid, 'sid':this.model.sid, 'params':this.model.params, 'push_url':this.model.push_url}).then((response)=>{
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
              this.$http.post('task/detail', {'name':this.model.name, 'extra':this.model.extra, 'category':this.model.category, 'tag':this.model.tag, 'type':this.model.type, 'period':this.model.period, 'aid':this.model.aid, 'fid':this.model.fid, 'sid':this.model.sid, 'params':this.model.params, 'push_url':this.model.push_url}).then((response)=>{
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
        },
        events: {
            modify:function(key, val) {
                this.$set('model.' + key, val);
            }
        }
    }
</script>

<style lang='less'>
  
</style>