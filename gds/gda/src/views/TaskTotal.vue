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
                    'label': 'total'
                }, {
                    'type': 'number',
                    'label': 'fail'
                }, {
                    'type': 'number',
                    'label': 'timeout'
                }, {
                    'type': 'number',
                    'label': 'succ'
                }],
                rows: [],
                options: {
                    vAxis: {
                        title: '',
                        minValue: 0,
                    },
                    width: '100%',
                    height: 800,
                    curveType: 'function'
                }
            }
        },
        created(){
            this.loadData()
        },
        methods: {
            loadData(){
                this.$http.get('task/quantityline', {'tid': this.$route.params._id}).then((response)=>{
                    let {quantityline, peak} = response.data.res;
                    if (quantityline) {
                        this.$set('rows', quantityline.map(item => [item.create_time, item.total, item.fail, item.timeout, item.succ]))
                        if (peak) this.$set('options.vAxis.maxValue', peak)
                    }
                })
            },
        },
    }
</script>
<style lang='less'>
</style>