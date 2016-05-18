export const BASE_URL = '';

export const API = (() => {
    const makeApi = (path) => {
        return `${BASE_URL}${path}`;
    };

    return {
        ORDER: makeApi('order'),
        ORDER_DETAIL: makeApi('order'),
        CHECKOUT_PRODUCT: makeApi('checkout'),
        PAY_PRODUCT: makeApi('order'),
        USER_ORDER_LIST: makeApi('user/order'),
        USER: makeApi('user'),
        MY_ORDER: makeApi('my'),
        AWARD: makeApi('award'),
        ADDRESS: makeApi('addr'),
        SELECT_ADDRESS: makeApi('submit/info'),
        CONFIRM_AWARD: makeApi('confirm'),
    };
})();
