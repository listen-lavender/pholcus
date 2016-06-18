<template>
  <div class="ui  segment">
    <div class="ui form basic segment">
      <h3>基本信息</h3>
      <div class="three fields">
          <div class="field">
            <label>名称</label>
            <input type="text" v-model="model.name">
          </div>
          <div class="field">
            <label>分类</label>
            <input type="text" v-model="model.category">
          </div>
      </div>
      <div class="field">
        <label>标签</label>
        <input type="text" v-model="model.tag">
      </div>
      <div class="field">
        <label>描述</label>
        <textarea class="ui input" v-model="model.extra" id="" cols="30" rows="5"></textarea>
      </div>
      <h3>任务信息</h3>
      <div class="two fields">
          <div class="field">
            <label>任务类型</label>
            <select class="ui dropdown" v-model="model.type">
              <option v-for="option in model.type_options" v-bind:value="option.value">{{option.text}}
              </option>
            </select>
          </div>
          <div class="field">
            <label>执行间隔</label>
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
        <label>推送接口</label>
        <input type="url" v-model="model.push_url">
      </div>
      <div class="field">
        <label>拉取接口</label>
        <p class="ui secondary basic segment">
          {{model.pull_url}}
        </p>
      </div>
      <button class="ui green button" alt="save" v-on:click="update">
        <i class="save icon"></i>
        保存
      </button>
    </div>
    
  </div>
</template>
<script>
    export default {
        data () {
            return {
              model: null,
              items:[]
            }
        },
        route: {
            data(transition){
                this.$http.get('task/detail/'+this.$route.params._id).then((response)=>{
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
            }
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