<template>
    <div class="uidropdown">
        <div class="multi">
            <span v-for="item in selectitems" class="tag">
                <span class="text">{{item.text}}</span>
                <a class="delete" v-on:click="rid(item)"></a>
            </span>
        </div>
        <ul class="optionlist">
            <li v-for="item in unselectitems" class="optionitem" v-on:click="choose(item)"><div>{{item.text}}</div></li>
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
            selectitems: {
                type: Array,
            },
            unselectitems: {
                type: Array,
            },
        },
        computed: {
            selectIds: function() {
                let selectIds = [];
                for(let k=0;k<this.selectitems.length;k++)
                    selectIds.push(this.selectitems[k].value);
                return selectIds.join(',');
            },
            unselectIds: function() {
                let unselectIds = [];
                for(let k=0;k<this.unselectitems.length;k++)
                    unselectIds.push(this.unselectitems[k].value);
                return unselectIds.join(',');
            },
        },
        methods: {
            choose:function(item){
                this.unselectitems.$remove(item);
                this.selectitems.push(item);
                this.$dispatch('selectmulti', this.mark, this.selectIds, this.unselectIds);
            },
            rid:function(item){
                this.selectitems.$remove(item);
                this.unselectitems.push(item);
                this.$dispatch('selectmulti', this.mark, this.selectIds, this.unselectIds);
            },
        }
    }
</script>
<style lang='less'>
    .uidropdown{
        position: relative;
        z-index: 0;
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
    .delete::before {
        content: "x";
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
        position: absolute;
        z-index: 1;
        top: 13px;
        max-height: 500px;
        opacity: 1;
        background: white;
        visibility: visible;
        border:1px solid black;
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