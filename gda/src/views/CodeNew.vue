<template>
<div class="ui image">
    <img v-bind:src="wallpaper.thumb" alt="">
</div>
  <form class="ui form" v-on:submit.prevent="save" >
    <div class="field">
      <label>name</label>
      <input type="text" name="name" v-model="model.name" placeholder="name">
    </div>
    <div class="field">
      <label>clsname</label>
      <input type="text" name="clsname" v-model="model.clsname" placeholder="clsname">
    </div>
    <div class="field">
      <label>desc</label>
      <textarea name="desc" v-model="desc" placeholder="model.desc" ></textarea>
    </div>
    <button class="ui green button" type="submit">保存</button>
  </form>
</template>
<script>
    export default {
        data () {
            return {
              'nav': [
                    {name: 'new', label: '创建脚本', path: '/active',}, 
                ]
            }
        },
        ready(){
            this.$http.get('v1/wallpaper/wallpaper').then((response)=>{
                this.$set('wallpaper', response.data.res.wallpaper[0]);
            }, (reason)=>{
                console.log(reason)
            })
        },
        props: {
          model: {
            type: Object,
            default(){
              return {name: '', 'clsname': '', 'desc': ''}
            }
          }
        },
        methods: {
          save(){
            console.log(JSON.stringify(this.model));
          }
        }
    }
</script>

<style lang='less'>
  
</style>