<template>
    <div class="ui sizer vertical segment">
        <div class="ui large header"><h3>{{model.name}}</h3></div>
    </div>
    <br>
    <div class="ui form">
        <div class="field" v-if="model.next_id">
            <div class="ui small header">Next</div>
            <a v-link="{name: 'step_detail', params: {_id: model.next_id}}">{{model.next}}</a>
        </div>
        <div class="field">
            <div class="ui small header">Description</div>
            <textarea class="ui input" rows="5" v-model="model.desc"></textarea>
        </div>
        <div class="four fields">
            <div class="field" v-if="model.index">
                <div class="ui small header">Index</div>
                <input type="text" class="ui input" v-model="model.index">
            </div>
            <div class="field">
                <div class="ui small header">Retry</div>
                <input type="text" class="ui input" v-model="model.retry">
            </div>
            <div class="field">
                <div class="ui small header">Timelimit</div>
                <input type="text" v-model="model.timelimit">
            </div>
            <div class="field">
                <div class="ui small header">Store</div>
                <input type="text" v-model="model.store">
            </div>
        </div>
        <div class="field">
            <div class="ui small header">Additions</div>
            <textarea id="" cols="30" rows="15" v-model="model.additions"></textarea>
        </div>
        <div v-if="model.current" class="field">
            <div class="ui small header">Authorize</div>
            <select class="ui search selection dropdown" multiple id="multi-select">
            </select>
        </div>
        <div class="field">
            <div class="ui green button" @click="update">
                <i class="save icon"></i>
                Save
            </div>
        </div>
        <br>
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