/*
   delete nullable value of dict
*/
function delnull(dict){
    for(key in dict)
        if(dict[key] == undefined || dict[key].toString() == ''||dict[key] == 'None')
            delete dict[key];
    return dict;
}

function parseurl(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r!=null)
        return (r[2]);
    return null;
}