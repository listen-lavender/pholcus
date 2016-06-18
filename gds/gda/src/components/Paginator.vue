<template>
    <div v-show="last>1" class="ui pagination menu">
      <a class="item" style="cursor:pointer;" v-on:click="goto(1)">1</a>
      <a v-if="!isStart" class="item" style="cursor:pointer;" v-on:click="goto(index - 1)">&lt;&lt;</a>
      <a v-for="page in pages" :class="index===page.number ? 'item active': 'item'" v-on:click="goto(page.number)">{{page.number}}</a>
      <a v-if="!isEnd" class="item" style="cursor:pointer;" v-on:click="goto(index + 1)">&gt;&gt;</a>
      <a class="item" style="cursor:pointer;" v-on:click="goto(last)">{{last}}</a>
      <!-- <span>
        goto page <input type="text" v-model="index" v-on:keyup.enter="goto(index)">
      </span> -->
    </div>
</template>
<script>
    import {near} from '../util'
    export default{
        props: {
            index: {
                type: Number,
                validator: function (value) {
                    return value > 0
                },
                default: 1
            },
            size: {
                type: Number,
                validator: function (value) {
                    return value >= 5
                },
                default: 10
            },
            total: {
                type: Number,
                default: 0
            },
            horizon: {
                type: Number,
                default: 6
            },
        },
        replace: true,
        inherit: false,
        computed: {
            isStart: function () {
                return this.index === 1;
            },
            isEnd: function () {
                return this.index === this.last;
            },
            pages: function () {
                return near(this.index, this.last, this.horizon);
            },
            last: function () {
                return Math.ceil(this.total/this.size);
            },
        },
        methods: {
            goto: function(num) {
                if (this.index != num && num > 0 && num <= this.last) {
                    this.index = num;
                    this.$dispatch('goto', this.index);
                }
            }
        },
    }
</script>
<style lang='less'>
    
</style>