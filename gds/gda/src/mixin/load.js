import {shallowCopy} from '../util';

var Paginator = {
    props: {
        index: {
            type: Number,
            default: 1
        },
        size: {
            type: Number,
            default: 10
        },
        deleted: {
            type: Boolean,
            default: false
        },
        datakey: {
            type: String,
            default: null
        },
        total: {
            type: Number,
            default: 0
        }
    },
    computed: {
        deleteUrl: function() {
            let link = this.datakey + '/detail';
            return link;
        },
    },
    watch: {
        'deleted': function(newVal, oldVal) {
            for(let k=0; k<this.result.length; k++){
                let obj = this.result[k];
                if(obj.own){
                    obj.deleted = newVal;
                    this.result.$set(k, obj);
                }
            }
        }
    },
    data() {
        return {
          result:{}
        }
    },
    ready(){
        this.$http.get(this.getUrl).then((response)=>{
            this.$set('total', response.data.res.total);
            if(this.datakey){
                for(let k=0; k<response.data.res[this.datakey].length; k++)
                    response.data.res[this.datakey][k].deleted = this.deleted
                this.$set('result', response.data.res[this.datakey]);
            }
            else
                this.$set('result', response.data.res);
        })
    },
    methods: {
        remove:function(obj) {
            this.$http.delete(this.deleteUrl + '/' + obj._id).then((response)=>{
                this.result.$remove(obj);
            })
        },
        removeAll:function() {
            let ids = [];
            for(let k=0; k<this.result.length; k++)
                if(this.result[k].own)
                    ids.push(this.result[k]._id);
            if(ids.length > 0){
                ids = ids.join(',');
                this.$http.delete(this.deleteUrl, {'ids':ids}).then((response)=>{
                    this.$dispatch('goto', 1);
                })
            }
        }
    },
    events: {
        goto:function(index) {
            this.$set('index', index);
            this.$http.get(this.getUrl).then((response)=>{
                this.$set('total', response.data.res.total);
                if(this.datakey)
                    this.$set('result', response.data.res[this.datakey]);
                else
                    this.$set('result', response.data.res);
            })
        }
    }
};

module.exports = Paginator;
