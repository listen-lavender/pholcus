var Filter = {
    props: {
        keyword: {
            type: String,
            default: null
        }
    },
    created(){
        this.$dispatch('getModel', this.model);
    },
    attached(){
        this.$dispatch('updateFlag', true);
    },
    events: {
        setFilter:function(model, keyword) {
            if(this.model == model & this.keyword != keyword){
                this.$set('index', 1);
                this.$set('keyword', keyword);
                this.$http.get(this.url).then((response)=>{
                        this.$set('result', response.data.res);
                    })
            }
        }
    },
    detached(){
        this.$dispatch('updateFlag', false);
    }
};

module.exports = Filter;
