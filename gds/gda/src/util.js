let Util = {
    getCookie(key) {
        let name = `${key}=`;
        let pair = document.cookie.split(';');
        
        for (let i = 0; i < pair.length; i++) {
            let item = pair[i];
            while(item.charAt(0) == ' ') item = item.substring(1);
            if (item.indexOf(name) === 0) return item.substring(name.length, item.length);
        }
        
        return '';
    },
    setCookie(key, val, expire){
        var exdate=new Date();
        exdate.setDate(exdate.getDate() + expire);
        document.cookie=key + "=" + escape(val) + ((expire == null||expire == undefined) ? "" : ";expires="+exdate.toGMTString());
　　},
   isLogined(val, expire){
        if(val == null||val == undefined)
            return Boolean(getCookie('logined'));
        else{
            setCookie('logined', val, expire);
            return Boolean(val);
        }
   }
};

export default Util;