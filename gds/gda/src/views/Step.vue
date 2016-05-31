<template>
    <div class="ui sizer vertical segment">
        <div class="ui large header">脚本分步抓取流</div>
    </div>
    <div class="ui input" v-for="(index, step) in result.step">
        <span>{{index+1}}.</span><span>{{step.name}}
        <a v-link="{name: 'step_detail', params: {_id: step._id}}">详情</a></span>
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
                this.$http.get('script/step/list?script_id='+this.$route.query.script_id+'&flow_id='+this.$route.query.flow_id).then((response)=>{
                    this.$set('result', response.data.res);
                })
            }
        }
    }
</script>
<style lang='less'>
</style>