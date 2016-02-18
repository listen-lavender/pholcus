/*
   delete nullable value of dict
*/
function delnull(dict){
    for(key in dict)
        if(dict[key].toString() == ''||dict[key] == 'None')
            delete dict[key];
    return dict;
}