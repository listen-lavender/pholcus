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
    watch: {
        'deleted': function(newVal, oldVal) {
            for(let k=0; k<this.result.length; k++){
                let obj = this.result[k];
                obj.deleted = newVal;
                this.result.$set(k, obj);
            }
        }
    },
    data() {
        return {
          result:{}
        }
    },
    ready(){
        this.$http.get(this.url).then((response)=>{
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
            console.log(obj);
            this.result.$remove(obj);
        },
        removeAll:function() {
            for(let k=0; k<this.result.length; k++){
                console.log(this.result[k]);
                console.log(this.result[k]._id);
                console.log(this.result[k].deleted);
            }
        }
    },
    events: {
        goto:function(index) {
            this.$set('index', index);
            this.$http.get(this.url).then((response)=>{
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
