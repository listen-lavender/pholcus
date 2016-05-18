import Util from '../util';
import API from './setting';


export const orderDetail = (id, callback) => {
    let url = `${API.ORDER_DETAIL}/${id}`;
    Util.ajax({
        url,
    }, callback);
};
