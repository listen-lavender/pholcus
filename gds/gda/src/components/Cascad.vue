<template>
    <div class="multi-select">
        <div class="item" v-for="item in items">
            <select class="select-first" v-model="item.firstSelected" v-on:change="firstChange($index, $event)">
                <option v-for="option in item.first" v-bind:value="option.value">{{option.text}}</option>
            </select>
            <select class="select-second" v-model="item.secondSelected" v-on:change="secondChange($index, $event)">
                <option v-for="option in item.second" v-bind:value="option.value">{{option.text}}</option>
            </select>
            <select class="select-third" v-model="item.thirdSelected">
                <option v-for="option in item.third" v-bind:value="option.value">{{option.text}}</option>
            </select>
            <a v-if="$index!=0" href="javascript:;" class="del" v-on:click = "delItem($index)">delete</a>
        </div>
        <a href="javascript:;" v-on:click="addItem()" class="addItem">add</a>
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
            var defaultData = {
        firstSelected: 0,
        secondSelected: 0,
        thirdSelected: 0,
        first: [{
            text: 'a',
            value: 0
        },{
            text: 'b',
            value: 1
        }],
        second: [{
            text: 'aa',
            value: 0
        },{
            text: 'bb',
            value: 1
        }],
        third: [{
            text: 'aaa',
            value: 0
        },{
            text: 'bbb',
            value: 1
        }]
    };
    var demo = new Vue({
        el: '.multi-select',
        data: {
            items: [],
            testData: [{a:0}]
        },
        created: function (i) {
            // 获取默认数据，如果是单一数据，直接赋值items[0]，如果是多个数据，循环赋值
            var d = extend({},defaultData);

            // 赋值给itmes
            this.items[0] = d;
        },
        methods:{
            // testAdd: function(){
            //  var self = this;
            //  self.testData.push({a:self.testData.length});
            // },
            firstChange: function(index,e){
                // 根据分类一的值，显示分类二、分类三的内容，默认是0
                var self = this,
                    obj = {
                        param: {
                            app_id: e.target.value
                        },//请求接口参数
                        index: index,//当前索引，获取数据后赋值给demo.items使用
                        val: e.target.value,//当前选中的值
                        type: 0 //分类级别，0一级分类，1二级分类
                    };
                getData(obj);
            },
            secondChange: function(index,e){
                var obj = {
                    param: {
                        app_id: e.target.value
                    },
                    index: index,
                    val: e.target.value,
                    type: 1
                }
                getData(obj);
            },
            addItem: function(){
                var self = this,
                    d = extend({},defaultData);
                self.items.push(d);
            },
            delItem: function(index){
                this.items.splice(index,1);
            }
        }
    });
    function extend(o,n){
        for(var key in n){
            if(n.hasOwnProperty(key) && !o.hasOwnProperty(key)){
                o[key] = n[key];
            }
        }
        return o;
    }
    //index分类的索引，type第几分类 
    function getData(obj){
        var index = obj.index;
        var b = {
            0: {
                selected: '0',
                items: [{
                    text: 'aa1',
                    value: 0
                },{
                    text: 'aa2',
                    value: 1
                }]
            },
            1: {
                selected: '0',
                items: [{
                    text: 'bb1',
                    value: 0
                },{
                    text: 'bb2',
                    value: 1
                }]
            }
        },
        c = {
            0: {
                selected: '0',
                items: [{
                    text: 'aaa1',
                    value: 0
                },{
                    text: 'aaa2',
                    value: 1
                }]
            },
            1: {
                selected: '0',
                items: [{
                    text: 'bbb1',
                    value: 0
                },{
                    text: 'bbb2',
                    value: 1
                }]
            }
        };
        var curItem = demo.items[index],
            val = obj.val || 0;

        // 如果是一级分类change，那么二级分类赋值后，三级也相应的赋值
        // 如果仅是二级分类，只要给三级分类赋值即可
        if(obj.type === 0){
            curItem.secondSelected = b[val]['selected'];
            curItem.second = b[val]['items'];

            curItem.thirdSelected = c[0]['selected'];
            curItem.third = c[0]['items'];
        }else{
            curItem.thirdSelected = c[val]['selected'];
            curItem.third = c[val]['items'];
        }
    }
        }
    }
</script>
<style lang='less'>
    
</style>