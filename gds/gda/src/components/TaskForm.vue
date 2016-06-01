<template>
  <form class="ui form" v-on:submit.prevent="update">
    <div class="four fields">
        <div class="field">
          <label>名称</label>
          <input type="text" v-model="model.name">
        </div>
        <div class="field">
          <label>描述</label>
          <input type="text" v-model="model.desc">
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
    <div class="two fields">
        <div class="field">
          <label>任务类型</label>
          <select>
          </select>
        </div>
        <div class="field">
          <label>执行间隔</label>
          <input type="text" v-model="model.period">
        </div>
    </div>
    <div class="field">
      <label>推送接口</label>
      <input type="text" v-model="model.push_url">
    </div>
    <div class="field">
      <label>拉取接口</label>
      <span>{{model.pull_url}}</span>
    </div>
    <div class="field">
      <label>article</label>
      <select>
      </select>
    </div>
    <div class="field">
      <label>flow</label>
      <select>
      </select>
    </div>
    <div class="field">
      <label>section</label>
      <select>
      </select>
    </div>
    <div class="field">
      <label>params</label>
      <input type="text" v-model="model.params">
    </div>
    <button class="ui green button" alt="save" v-on:click="update">保存</button>
    <button class="ui button" v-on:click="cancel" >取消</button>
  </form>
</template>
<script>
    export default {
        data () {
            return {
              model: null,
              articles:[],
              flows:[],
              sections:[],
            }
        },
        route: {
            data(transition){
                this.$http.get('task/detail/'+this.$route.params._id).then((response)=>{
                    this.$set('model', response.data.res.task);
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
              this.$http.post('task/detail/'+this.$route.params._id, {'desc':this.model.desc, 'retry':this.model.retry, 'timelimit':this.model.timelimit, 'store':this.model.store, 'additions':this.model.additions}).then((response)=>{
              })
            }
        }
    }
</script>

<style lang='less'>
  
</style>