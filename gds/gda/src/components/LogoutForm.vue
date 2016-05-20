<template>
</template>
<script>
    import {isLogined, setCookie} from '../util'
    export default {
        ready(){
            this.$http.get('creator/logout').then((response)=>{
                isLogined(false);
                setCookie('sid', '');
                setCookie('session', '');
                this.$route.router.go({name: 'login'});
            })
        },
    }
</script>
<style lang='less'>
</style>