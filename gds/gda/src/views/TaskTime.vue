<template>
    <div class="ui segment">
        <vue-chart
            :columns="columns"
            :rows="rows"
            :options="options"
        ></vue-chart>
    </div>
</template>
<script>
    export default {
        data(){
            return {
                columns: [{
                    'type': 'string',
                    'label': 'Hour'
                }, {
                    'type': 'number',
                    'label': 'elapse'
                }],
                rows: [],
                options: {
                    vAxis: {
                        title: '',
                        minValue: 0,
                        maxValue: 1
                    },
                    width: '100%',
                    height: 800,
                    curveType: 'function'
                }
            }
        },
        created(){
            this.loadData();
        },
        methods: {
            loadData(){
                this.$http.get('task/timeline', {'tid': this.$route.params._id}).then((response)=>{
                    let {timeline} = response.data.res;
                    if (timeline) {
                        this.$set('rows', timeline.map(item => [item.create_time, item.elapse]))
                    }
                })
            },
        }
    }
</script>
<style lang='less'>
</style>