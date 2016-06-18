<template>
</template>
<script>
    import {isLogined, setCookie, setLocal} from '../util'
    export default {
        ready(){
            this.$http.get('creator/logout').then((response)=>{
                isLogined(false);
                setCookie('sid', '');
                setCookie('session', '');
                setLocal('group', '')
                setLocal('uid', '')
                this.$route.router.go({name: 'login'});
            })
        },
    }
</script>
<style lang='less'>
</style>