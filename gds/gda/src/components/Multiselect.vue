<template>
    <div class="uidropdown">
        <div class="multi">
            <span v-for="item in selectItems" class="tag">
                <san class="text">banana</san>
                <a class="delete" v-on:click="rid(item)"></a>
            </span>
        </div>
        <ul class="optionlist">
            <li v-for="item in unselectItems" class="optionitem" v-on:click="choose(item)"><div>{{item.name}}</div></li>
        </ul>
    </div>
</template>
<script>
    export default {
        props: {
            mark:{
                type: String,
                default:'',
            },
            selectItems: {
                type: Array,
            },
            unselectItems: {
                type: Array,
            },
        },
        computed: {
            selectIds: function() {
                let selectIds = [];
                for(let k=0;k<this.selectItems.length;k++)
                    selectIds.push(this.selectItems[k]._id);
                return selectIds.join(',');
            },
            unselectIds: function() {
                let unselectIds = [];
                for(let k=0;k<this.unselectItems.length;k++)
                    unselectIds.push(this.unselectItems[k]._id);
                return unselectIds.join(',');
            },
        },
        methods: {
            choose(item){
                this.unselectItems.$remove(item);
                this.selectItems.push(item);
                this.$dispatch('selectmulti', this.mark, this.selectIds, this.unselectIds);
            },
            rid(item){
                this.selectItems.$remove(item);
                this.unselectItems.push(item);
                this.$dispatch('selectmulti', this.mark, this.selectIds, this.unselectIds);
            },
        }
    }
</script>
<style lang='less'>
    .uidropdown{
        position: relative;
        border: 0;
        font: inherit;
        font-size: 100%;
        padding: 0;
        margin: 0;
        word-break: break-all;
        vertical-align: baseline;
        -webkit-overflow-scrolling: touch;
        outline: 0;
        box-sizing: border-box;
        display: block;
    }
    .multi{
        border: 1px solid #ddd;
        line-height: 25px;
        height: 30px;
        width: 100%;
        padding: 1px 5px;
    }
    .tag{
        cursor: pointer;
        margin-right: 3px;
        background: #eee;
        color: #000;
        font-size: 14px;
        padding: 0 3px;
    }
    .text{
        padding-right: 3px;
    }
    .delete{
        color: #000;
    }
    .content{
        border: none;
        display: inline;
        white-space: pre;
        max-width: 100%;
    }
    .placeholder{
        color: #ddd;
        margin-left: -6px;
    }
    .optionlist{
        max-height: 500px;
        opacity: 1;
        visibility: visible;
    }
    .optionlist li{
        cursor: pointer;
        list-style-type: none;
    }
    .optionitem{
        padding: 3px 1pc;
        border-bottom: 1px solid transparent;
    }
</style>