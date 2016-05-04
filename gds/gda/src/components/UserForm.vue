<template>
  <form class="ui form" v-on:submit.prevent="save" >
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
          <select v-model="model.type" >
              <option value="ONCE" >临时任务</option>
              <option value="FOREVER" >周期任务</option>
          </select>
        </div>
        <div class="field">
          <label>执行间客</label>
          <input type="text" v-model="model.period">
        </div>
    </div>
    <div class="field">
      <label>推送接口</label>
      <input type="text" v-model="model.push_url">
    </div>
    <div class="field">
      <label>拉取接口</label>
      <input type="text" v-model="model.pull_url">
    </div>
    <div class="field">
      <label>article</label>
      <select v-model="model.aid" >
        <option v-bind:value="item._id" v-for="item in articles" >{{item.filepath}}</option>
      </select>
    </div>
    <div class="field">
      <label>flow</label>
      <select v-model="model.flow" >
        <option v-bind:value="item" v-for="item in flows" >{{item}}</option>
      </select>
    </div>
    <div class="field">
      <label>section</label>
      <select v-model="model.sid" >
        <option v-bind:value="item._id" v-for="item in sections" >{{item.section_name}}</option>
      </select>
    </div>
    <div class="field">
      <label>params</label>
      <input type="text" v-model="model.params">
    </div>
    <button class="ui green button" type="submit">保存</button>
    <button class="ui button" v-on:click="cancel" >取消</button>
  </form>
</template>
<script>
    export default {
        data: function(){
            return {'model': {}, 'flows': [], 'sections': [], 'articles': []}
        },
        route: {
            data(transition){
                let response_data = {}
                return this.$http.get('p/task/detail/'+this.$route.params._id).then((response)=>{
                    response_data.model = response.data.result.task
                    return this.$http.get('p/task/flows', {'aid': response_data.model.aid})
                }).then((response)=>{
                    response_data.flows = response.data
                    return this.$http.get('p/task/sections', {'aid': response_data.model.aid, 'flow': response_data.model.flow})
                }).then((response)=>{
                    response_data.sections = response.data
                    return this.$http.get('p/task/articles')
                }).then((response)=>{
                    response_data.articles = response.data
                    return response_data
                })
            }
        },
        methods: {
          save(){
            console.log(JSON.stringify(this.model));
          },
          cancel(){
            this.$route.router.go({name: 'manage'})
          }
        }
    }
</script>
<style lang='less'>
</style>