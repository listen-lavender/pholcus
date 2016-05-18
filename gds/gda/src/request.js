import {getCookie, setCookie, isLogined} from './util';

let Util = {
    xhr({ url = '', type = 'GET', dataType = 'json', data = {}, success, error = function(err){} }){
        type = type.toUpperCase();
        let xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4) {
                if (xhr.status >= 200 && xhr.status < 300) {
                    typeof success === 'function' && success(xhr.responseText);
                } else {
                    typeof error === 'function' && error(xhr.status);
                }
            }
        };
        
        if (type === "GET") {
            xhr.open(type, this.setParameter(url, data), true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            xhr.send(null);
        } else if (type === "POST" || type === 'PUT') {
            xhr.open(type, url, true);
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            data._xsrf = getCookie('_xsrf');
            xhr.send(this.setParameter('', data).slice(1));
        }

    },

    capitalize(val = ''){ return `${val.slice(0, 1).toUpperCase()}${val.slice(1)}`; },

    timeAgo(secs = 0){
        let t = Date.now() / 1000 - parseInt(secs);

        if (t / 86400 > 1) return this.formatDateTime(secs * 1000, { showYear: t / 31536000 > 1 });
        if (t / 3600 > 1) return `${Math.floor(t / 3600)} 小时前`;
        if (t / 60 > 1) return `${Math.floor(t / 60)} 分钟前`;
        if (t > 10) return `${Math.floor(t)} 秒前`;
        return '刚刚收到';
    },

    socialTimeAgo(secs = 0){
        let t = Date.now() / 1000 - parseInt(secs);

        if (t / 172800 > 1) return this.formatDateTime(secs * 1000, { showYear: t / 31536000 > 1 });
        if (new Date().getDate() - new Date(parseInt(secs) * 1000).getDate() == 1) {
            return '昨天 ' + this.formatDateTime(secs * 1000, { showMoment: true });
        }
        if (t / 3600 > 1) return this.formatDateTime(secs * 1000, { showMoment: true });
        if (t / 60 > 1) return Math.floor(t / 60) + ' 分钟前';
        if (t > 10) return Math.floor(t) + ' 秒前';
        return '刚刚';
    },

    formatDateTime(mSecs = 0, options) {
        options = options || {};
        let hour, min, sec, month, day, year,
            date = new Date(parseInt(mSecs)),
            fill = options.simple ? '' : '0';
        
        hour = date.getHours() > 9 ? date.getHours() : `${fill}${date.getHours()}`;
        min = date.getMinutes() > 9 ? date.getMinutes() : `${fill}${date.getMinutes()}`;
        
        if (!!options.showMoment) return hour + ':' + min;

        sec = date.getSeconds() > 9 ? date.getSeconds() : `${fill}${date.getSeconds()}`;
        month = parseInt(date.getMonth() + 1)  > 9 ? parseInt(date.getMonth() + 1)  : `${fill}${parseInt(date.getMonth() + 1)}`;
        day =  date.getDate() > 9 ?  date.getDate() : `${fill}${date.getDate()}`;
        year = !!options.showYear ? `${date.getFullYear()}-` : '';

        return `${year}${month}-${day} ${hour}:${min}`;
    },

    ajax({ url = '', type = 'GET', data, dataType = 'JSON' }, sucCallback, errCallback){
        this.xhr({
            url: url,
            type: type,
            data: data,
            dataType: dataType,
            success(data){
                data = JSON.parse(data);
                if (String(data.code) === '0' && typeof sucCallback === 'function') {
                    sucCallback(data.res);
                } else if(String(data.code) === '4') {
                    ClientSdk.login();
                } else {
                    ClientSdk.toastClient(data.msg);
                    
                    if (typeof sucCallback === 'function') {
                        return sucCallback(data);
                    }
                }
            },

            error(err){
                return typeof errCallback === 'function' ? errCallback(err) : err;
                console.error(err);
            }
        });
    },
    
    getParameter(url = '', name = ''){
        let reg = new RegExp("[\\?&]" + name + "=([^&#]*)", "gi"), results = reg.exec(url);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    },

    setParameter(url = '', querys = {}){
        for (let name in querys){
            let spliter = url.indexOf('?') !== -1 ? '&' : '?', reg;
            reg = new RegExp(`([?&])${name}=.*?(&|$)`, "gi");
            url = this.getParameter(url, name) ? url.replace(reg, `$1${name}=${querys[name]}$2`) : `${url}${spliter}${name}=${querys[name]}`;
        }
        return url;
    },
};

export default Util;