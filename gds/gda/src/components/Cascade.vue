<template>
    <div>
        <choose v-for="(index, item) in items" :curr="index" :next="index+1" :url="item.url" :label="item.label" :key="item.key" :val="item.val" :options="item.options"></choose>
    </div>
</template>
<script>
    export default {
        props: {
            items: {
                type: Array,
            },
        },
        events: {
            select:function(curr, next, key, val) {
                this.$dispatch('modify', key, val);
                this.$broadcast('refresh', curr, next, key, val);
            }
        }
    }
</script>
<style lang='less'>
    
</style>