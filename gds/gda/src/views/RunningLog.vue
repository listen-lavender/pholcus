<template>
    <div class="ui items">
      <div class="item">
        <div class="content">
          <a class="header">Args</a>
          <div class="meta">
            <span></span>
          </div>
          <div class="description">
            <p>{{result.log.args}}</p>
          </div>
          <div class="extra">
          </div>
        </div>
      </div>

      <div class="item">
        <div class="content">
          <a class="header">Kwargs</a>
          <div class="meta">
            <span></span>
          </div>
          <div class="description">
            <p>{{result.log.kwargs}}</p>
          </div>
          <div class="extra">
          </div>
        </div>
      </div>

      <div class="item">
        <div class="content">
          <a class="header">Exception</a>
          <div class="meta">
            <span></span>
          </div>
          <div class="description">
            <p>{{result.log.exception}}</p>
          </div>
          <div class="extra">
          </div>
        </div>
      </div>
      <a v-link="{name: 'task_detail', params: {_id: result.log.tid}}">view task</a>
    </div>
</template>
<script>
    export default {
        data() {
            return {
              result: null,
            }
        },
        route: {
            data(transition){
                this.$http.get('running/log/' + this.$route.params._id).then((response)=>{
                    this.$set('result', response.data.res);
                })
            }
        }
    }
</script>
<style lang='less'>
</style>