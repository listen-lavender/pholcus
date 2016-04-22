import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import App from './App.vue'
import NavView from './views/Nav.vue'
import CodeView from './views/Code.vue'
import TaskView from './views/Task.vue'
import UserView from './views/User.vue'
import TaskActiveView from './views/TaskActive.vue'
import TaskMonitorView from './views/TaskMonitor.vue'
import TaskManageView from './views/TaskManage.vue'
import TaskForm from './components/TaskForm.vue'
import CodeNewView from './views/CodeNew.vue'



var app = Vue.extend({})


Vue.use(VueRouter)
Vue.use(VueResource)

Vue.http.options.root = 'http://192.168.0.33:7001/gds'

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
            '/manage': {
                name: 'manage',
                component: TaskManageView
            },
            '/:_id': {
                name: 'detail',
                component: TaskForm
            }
        }
    },
    '/code': {
        name: 'code',
        component: CodeView,
        subRoutes: {
            '/new': {
                name: 'new',
                component: CodeNewView
            }
        }
    },
    '/user': {
        name: 'user',
        component: UserView
    }
})


router.start(app, 'body')