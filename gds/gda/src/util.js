'use strict'

export const parseCookie = function(){
    let pair = document.cookie.split(';');
    let jsonCookie = {};
    
    for (let index = 0; index < pair.length; index++) {
        let item = pair[index].split('=');
        item[0] = item[0].replace(/ /g, '');
        item[1] = item[1].replace(/"/g, '');
        jsonCookie[item[0]] = item[1]
    }
    return jsonCookie;
}

export const getCookie = function(key){
    let jsonCookie = parseCookie()
    if (key in jsonCookie)
        return jsonCookie[key]
    return '';
}

export const setCookie = function(key, val, expire){
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + expire);

    let jsonCookie = {};
    jsonCookie[key] = val
    if (expire == null||expire == undefined)
        ;
    else
        jsonCookie['expires'] = exdate.toGMTString()
    
    let txtCookie = []
    for(key in jsonCookie)
        txtCookie.push(' ' + key + '=' + jsonCookie[key])
    document.cookie = txtCookie.join(';').replace(' ', '');
}

export const getLocal = function(key){
    if(window.localStorage)
        return (window.localStorage.getItem(key)||'')
    return getCookie(key)
}

export const setLocal = function(key, val, expire){
    if(window.localStorage)
        window.localStorage.setItem(key, val)
    else
        setCookie(key, val, expire)
}

export const getSession = function(key){
    if(window.sessionStorage)
        return (window.sessionStorage.getItem(key)||'')
    return getCookie(key)
}

export const setSession = function(key, val, expire){
    if(window.sessionStorage)
        window.sessionStorage.setItem(key, val)
    else
        setCookie(key, val, expire)
}

export const isLogined = function(val, expire){
    if(val == null||val == undefined){
        return getLocal('logined').toLowerCase() === 'true'
    }
    else{
        val = val + ''
        setLocal('logined', val, expire)
        return val.toLowerCase() === 'true'
    }
}
