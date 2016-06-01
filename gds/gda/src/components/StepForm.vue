<template>
    <div class="ui sizer vertical segment">
        <div class="ui large header">脚本分步抓取流</div>
    </div>
    <div class="ui styled accordion">
        <div class="title active">{{model.name}}</div>
        <div class="content active">
            <div class="ui input">
                <span>desc:</span><input type="text" v-model="model.desc">
            </div>
            <div class="ui input">
                <span v-if="model.next_id">next:</span>
                <span>
                    <a v-if="model.next_id" v-link="{name: 'step_detail', params: {_id: model.next_id}}">{{model.next}}</a>
                </span>
            </div>
            <div class="ui input">
                <span>index:</span><span>{{model.index}}</span>
            </div>
            <div class="ui input">
                <span>retry:</span><input type="text" v-model="model.retry">
            </div>
            <div class="ui input">
                <span>timelimit:</span><input type="text" v-model="model.timelimit">
            </div>
            <div class="ui input">
                <span>store:</span><input type="text" v-model="model.store">
            </div>
            <div class="ui input">
                <span>additions:</span><input type="text" v-model="model.additions">
            </div>
        </div>
    </div>
    <div class="ui container">
        <i class="save icon" alt="save" v-on:click="update"></i>
    </div>
    <div v-if="model.current" class="ui">
        <span>授权:</span>
        <select class="ui search selection dropdown" multiple id="multi-select">
        </select>
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
                this.$http.get('script/step/detail/'+this.$route.params._id).then((response)=>{
                    this.$set('model', response.data.res.step);
                })
            }
        },
        methods: {
            update(){
              this.$http.post('script/step/detail/'+this.$route.params._id, {'desc':this.model.desc, 'retry':this.model.retry, 'timelimit':this.model.timelimit, 'store':this.model.store, 'additions':this.model.additions}).then((response)=>{
              })
            }
        }
    }
</script>
<style lang='less'>
</style>