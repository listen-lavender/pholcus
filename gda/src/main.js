import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

import LoginView from './views/Login.vue'

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

import CreatorView from './views/Creator.vue'
import CreatorForm from './components/CreatorForm.vue'
import UserForm from './components/UserForm.vue'

var app = Vue.extend({})


Vue.use(VueRouter)
Vue.use(VueResource)

Vue.http.options.root = 'http://localhost:7001/gds/api'

// Vue.http.interceptors.push({
//     response(response){
//         if(response.data.stat===1){
//             return response.data.result;
//         }else {
//             throw {'name': 'Response Error', 'msg': `stat error ${response.data.stat}`}
//         }
//     }
// })

var router = new VueRouter({
    linkActiveClass: 'active'
})

router.map({
    '/': {
        name: 'home',
        component: app
    },
    '/login': {
        name: 'login',
        component: LoginView
    },
    '/task': {
        name: 'task',
        component: TaskView,
        subRoutes: {
            '/': {
                component: TaskActiveView
            },
            '/active': {
                name: 'active',
                component: TaskActiveView
            },
            '/monitor': {
                name: 'monitor',
                component: TaskMonitorView,
                subRoutes: {
                    '/data/:_id':{
                        name: 'data',
                        component: TaskMonitorDataView,
                    },
                    '/time/:_id':{
                        name: 'time',
                        component: TaskMonitorTimeView,
                    },
                    '/total/:_id':{
                        name: 'total',
                        component: TaskMonitorTotalView,
                    },
                    '/log/:_id':{
                        name: 'log',
                        component: TaskMonitorLogView,
                    }
                }
            },
            '/:_id':{
                name: 'task_detail',
                component: TaskForm,
            }
        }
    },
    '/script': {
        name: 'script',
        component: ScriptView,
        subRoutes: {
            '/:_id':{
                name: 'script_detail',
                component: ScriptForm,
            }
        }
    },
    '/creator': {
        name: 'creator',
        component: CreatorView,
        subRoutes: {
            '/:_id':{
                name: 'creator_detail',
                component: CreatorForm,
            }
        }
    },
    '/setting/:_id': {
        name: 'setting',
        component: UserForm
    }
})


router.start(app, 'body')