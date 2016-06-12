import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import HomeView from './views/Home.vue'

import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import LogoutForm from './components/LogoutForm.vue'

import TaskView from './views/Task.vue'
import TaskActiveView from './views/TaskActive.vue'
import TaskMonitorView from './views/TaskMonitor.vue'
import TaskMonitorDataView from './views/TaskMonitorData.vue'
import TaskMonitorTimeView from './views/TaskMonitorTime.vue'
import TaskMonitorTotalView from './views/TaskMonitorTotal.vue'
import TaskMonitorLogView from './views/TaskMonitorLog.vue'
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

import {isLogined, setLocal} from './util'

// Vue.component('home', HomeView)
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
        name: 'home',
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
            '/task': {
                name: 'task',
                component: TaskView,
                subRoutes: {
                    '/active': {
                        name: 'active',
                        component: TaskActiveView
                    },
                    '/monitor': {
                        name: 'monitor',
                        component: TaskMonitorView,
                    },
                    '/monitor/data/:_id': {
                        name: 'data',
                        component: TaskMonitorDataView,
                    },
                    '/monitor/time/:_id': {
                        name: 'time',
                        component: TaskMonitorTimeView,
                    },
                    '/monitor/total/:_id': {
                        name: 'total',
                        component: TaskMonitorTotalView,
                    },
                    '/monitor/log/:_id': {
                        name: 'log',
                        component: TaskMonitorLogView,
                    },
                    '/:_id':{
                        name: 'task_detail',
                        component: TaskForm,
                    }
                }
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
                return response
            }
            else{
                isLogined(true)
                return response
            }
        }
        else{
            isLogined(false)
            setLocal('code', response.data.code)
            setLocal('msg', response.data.msg)
            router.go({name:'unknow'})
            return response
        }
    }

});

router.alias({
    '/': '/manage/task/active',
    '/manage': '/manage/task/active',
    '/manage/task': '/manage/task/active',
})

router.beforeEach(function(transition) {
    if((transition.to.path == '/login' || transition.to.path == '/register') && isLogined()){
        router.go({name:'active'})
    }
    else if(transition.to.path == '/unknow' || transition.to.path == '/login' || transition.to.path == '/register' || isLogined()){
        transition.next()
    }
    else{
        router.go({name:'login'})
    }
})

router.start(HomeView, '#app')
window.Vue = Vue

