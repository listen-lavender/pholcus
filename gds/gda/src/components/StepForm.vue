<template>
    <div class="ui sizer vertical segment">
        <div class="ui large header">脚本分步抓取流</div>
    </div>
    <div class="ui container">
        <i class="save icon" alt="save" onclick="savesection(this)"></i>
    </div>
    <div class="ui styled accordion">
        <div id="section_title" class="title active">{{result.step.name}}</div>
        <div class="content active">
            <input id="sid" type="hidden" :value="result.sid"/>
            <div class="ui input">
                <span>section_name:</span><span>{{result.step.name}}</span>
            </div>
            <div class="ui input">
                <span>desc:</span><input id="desc" type="text" value="{{result.step.desc}}">
            </div>
            <div class="ui input">
                <span v-if="result.step.next_id">next:</span>
                <span>
                    <a v-if="result.step.next_id" v-link="{name: 'step_detail', params: {_id: result.step.next_id}}">{{result.step.next}}</a>
                </span>
            </div>
            <div class="ui input">
                <span>index:</span><input id="index" type="text" value="{{result.step.index}}">
            </div>
            <div class="ui input">
                <span>retry:</span><input id="retry" type="text" value="{{result.step.retry}}">
            </div>
            <div class="ui input">
                <span>timelimit:</span><input id="timelimit" type="text" value="{{result.step.timelimit}}">
            </div>
            <div class="ui input">
                <span>store:</span><input id="store" type="text" value="{{result.step.store}}">
            </div>
            <div class="ui input">
                <span>additions:</span><input id="additions" type="text" value="{{result.step.additions}}">
            </div>
        </div>
    </div>
    <div v-if="result.step.current" class="ui">
        <span>授权:</span>
        <select class="ui search selection dropdown" multiple id="multi-select">
        </select>
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
                this.$http.get('script/step/detail/'+this.$route.params._id).then((response)=>{
                    this.$set('result', response.data.res);
                })
            }
        },
        methods: {
            save(){
                this.$http.post('script/step/detail/'+this.$route.params._id, {'desc':this.desc}).then((response)=>{
                    console.log(response.data.msg);
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