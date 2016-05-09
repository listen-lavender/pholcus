import Util from '../util';
var LoginState = {

    props: {
        uid: {
            type: String,
            default: function(){
                
            },
            required: true
        },
    },

    data(){
        return {
            fetching: false,
            finished: false,
            page: 0,
            pageLimit: 10,
        };
    },

    methods: {
        formatApi: function(url, options){
            var skip = options && options.skip || 0;
            var limit = options && options.limit || this.$get('pageLimit');
            return Util.setQueryVal(url, {skip: skip, limit: limit});
        },
        getList: function(callback){
            this.$set('fetching', true);

            this.fetchingData({limit: this.$get('pageLimit'), skip: this.$get('page') * this.$get('pageLimit')}, data => {
                this.$set('page', this.$get('page') + 1);
                this.$set('fetching', false);
                callback(data);
            });
        },

        getInitList(callback){
            this.$set('page', 0);
            this.$set('finished', false);
            this.$set('fetching', false);
            this.getList(callback);
        },

        fetchingData: function(options, callback){
            if (typeof options === 'function') {
                callback = options;
                options = {};
            }

            Util.ajax({
                url: this.formatApi(this.$get('url'), options)
            }, function(data){
                if (!(data && data.length > 0 && typeof callback === 'function')) {
                    this.$set('finished', true);
                }
                callback(data);
            }.bind(this));
        },
    }

};

module.exports = LoginState;