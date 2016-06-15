import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import HomeView from './views/Home.vue'

import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import LogoutForm from './components/LogoutForm.vue'

import RunningSnapshotView from './views/RunningSnapshot.vue'
import TaskView from './views/Task.vue'
import TaskDataView from './views/TaskData.vue'
import TaskTimeView from './views/TaskTime.vue'
import TaskTotalView from './views/TaskTotal.vue'
import TaskLogView from './views/TaskLog.vue'
import TaskForm from './components/TaskForm.vue'

import ScriptView from './views/Script.vue'
import ScriptForm from './components/ScriptForm.vue'

import StepView from './views/Step.vue'
import StepForm from './components/StepForm.vue'

import CreatorView from './views/Creator.vue'
import CreatorForm from './components/CreatorForm.vue'
import UserForm from './components/UserForm.vue'

import NavMenuView from './components/NavMenu.vue'
import TopView from './components/Top.vue'

import ChooseView from './components/Choose.vue'
import CascadeView from './components/Cascade.vue'
import PaginatorView from './components/Paginator.vue'

import UnknowView from './views/Unknow.vue'

import {isLogined, setLocal, getLocal} from './util'

// Vue.component('index', HomeView)
Vue.component('top', TopView)
Vue.component('choose', ChooseView)
Vue.component('cascade', CascadeView)
Vue.component('paginator', PaginatorView)

// var App = Vue.extend({'template':'<home></home>'})

Vue.use(VueRouter)
Vue.use(VueResource)

var router = new VueRouter({
    // history: true,
    linkActiveClass: 'active'
})

router.map({
    '/': {
        name: 'index',
        component: HomeView
    },
    '/login': {
        name: 'login',
        component: LoginForm,
    },
    '/register': {
        name: 'register',
        component: RegisterForm,
    },
    '/logout': {
        name: 'logout',
        component: LogoutForm,
    },
    '/manage':{
        name: 'manage',
        component: NavMenuView,
        subRoutes: {
            '/running/snapshot': {
                name: 'runningsnapshot',
                component: RunningSnapshotView
            },
            '/task': {
                name: 'task',
                component: TaskView,
            },
            '/task/data/:_id': {
                name: 'data',
                component: TaskDataView,
            },
            '/task/time/:_id': {
                name: 'time',
                component: TaskTimeView,
            },
            '/task/total/:_id': {
                name: 'total',
                component: TaskTotalView,
            },
            '/task/log/:_id': {
                name: 'log',
                component: TaskLogView,
            },
            '/task/:_id':{
                name: 'task_detail',
                component: TaskForm,
            },
            '/script': {
                name: 'script',
                component: ScriptView
            },
            '/script/:_id': {
                name: 'script_detail',
                component: ScriptForm,
            },
            '/step': {
                name: 'step',
                component: StepView,
            },
            '/step/:_id': {
                name: 'step_detail',
                component: StepForm,
            },
            '/creator': {
                name: 'creator',
                component: CreatorView,
            },
            '/creator/:_id': {
                name: 'creator_detail',
                component: CreatorForm,
            },
            '/setting/:_id': {
                name: 'setting',
                component: UserForm,
            },
        }
    },
    '/unknow': {
        name: 'unknow',
        component: UnknowView
    }
})

Vue.http.options.emulateJSON = true;
Vue.http.options.root = '/gds/api'
Vue.http.options.error = function(response) {
}

Vue.http.options.beforeSend = function(request){
    // request.headers['Authorization'] = 'abc';
    // Vue.http.headers.common['Authorization'] = 'abc';
    // request.headers['Cookie'] = document.cookie;
}

Vue.http.interceptors.push({

    request: function (request) {
        return request;
    },

    response: function (response) {
        if(response.data.code == 1){
            if(response.data.res.user == null){
                isLogined(false)
                setLocal('group', '')
                return response
            }
            else{
                isLogined(true)
                setLocal('group', response.data.res.user.group)
                return response
            }
        }
        else{
            isLogined(false)
            setLocal('code', response.data.code)
            setLocal('msg', response.data.msg)
            setLocal('group', '')
            router.go({name:'unknow'})
            return response
        }
    }

});

router.alias({
    // '/': '/manage/running/snapshot',
})

router.beforeEach(function(transition) {
    if((transition.to.path == '/login' || transition.to.path == '/register') && isLogined()){
        if(getLocal('group') == 'operator')
            router.go({name:'task'});
        else
            router.go({name:'runningsnapshot'});
    }
    else if(transition.to.path == '/unknow' || transition.to.path == '/login' || transition.to.path == '/register' || isLogined()){
        if(transition.to.path == '/')
            if(getLocal('group') == 'operator')
                router.go({name:'task'});
            else
                router.go({name:'runningsnapshot'});
        else
            transition.next();
    }
    else{
        router.go({name:'login'})
    }
})

router.start(HomeView, '#app')

