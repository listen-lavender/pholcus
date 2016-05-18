import {isLogined} from '../util';

var LoginState = {
    data(){
        return {
            loggined: isLogined(),
        };
    },
};

module.exports = LoginState;