<template>
    <div class="field">
      <label>{{label}}</label>
      <!-- <select v-model="{{key}}"> -->
      <select v-model="val">
        <option v-for="option in options" :value="option.value">
          {{option.text}}
        </option>
      </select>
    </div>
</template>
<script>
    export default {
        props: {
            curr: {
                type: Number,
            },
            next: {
                type: Number,
            },
            url: {
                type: String,
            },
            label: {
                type: String,
            },
            key: {
                type: String,
            },
            val: {
                type: Number,
            },
            options: {
                type: Array
            }
        },
        watch:{
            val: function(newVal, oldVal) {
                if(newVal && newVal != oldVal){
                    this.$dispatch('select', this.curr, this.next, this.key, this.val);
                }
            },
        },
        events: {
            refresh:function(curr, next, key, val) {
                if(this.curr > curr){
                    this.$set('options', []);
                    this.$set('val', '');
                }
                if(this.curr == next){
                    console.log()
                    this.$http.get(this.url + '?' + key + '=' + val).then((response)=>{
                        this.$set('options', response.data.res['options']);
                        this.$set('val', this.options.length>0?this.options[0].value:'');
                    })
                }
            }
        }
    }
</script>
<style lang='less'>
    
</style>