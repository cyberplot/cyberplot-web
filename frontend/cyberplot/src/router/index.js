import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Dataset from '@/components/Dataset'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: Login
        },

        {
            path: '/dataset/',
            name: 'DatasetNone',
            component: Dataset
        },

        {
            path: '/dataset/:id',
            name: 'Dataset',
            component: Dataset
        }
    ]
})
