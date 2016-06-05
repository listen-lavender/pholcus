var Paginator = {
    props: {
        index: {
            type: Number,
            default: 1
        },
        size: {
            type: Number,
            default: 10
        }
    },
    data() {
        return {
          result: {},
        }
    },
    ready(){
        this.$http.get(this.url).then((response)=>{
            this.$set('result', response.data.res);
        })
    },
    events: {
        goto:function(index) {
            this.$set('index', index);
            this.$http.get(this.url).then((response)=>{
                    this.$set('result', response.data.res);
                })
        }
    }
};

module.exports = Paginator;
