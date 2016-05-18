'use strict'

export const getCookie = function(key, val, expire){
    let name = `${key}=`;
    let pair = document.cookie.split(';');
    
    for (let i = 0; i < pair.length; i++) {
        let item = pair[i];
        while(item.charAt(0) == ' ') item = item.substring(1);
        if (item.indexOf(name) === 0) return item.substring(name.length, item.length);
    }
    
    return '';
}

export const setCookie = function(key, val, expire){
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + expire);
    document.cookie=key + "=" + escape(val) + ((expire == null||expire == undefined) ? "" : ";expires="+exdate.toGMTString());
}

export const isLogined = function(val, expire){
    if(val == null||val == undefined){
        return getCookie('logined').toLowerCase() === 'true'
    }
    else{
        val = val + ''
        console.log('---q')
        setCookie('logined', val, expire)
        console.log('---p')
        return val.toLowerCase() === 'true'
    }
}
