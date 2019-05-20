import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Dataset from '@/components/Dataset'
import Store from '@/store'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/login',
            name: 'Login',
            component: Login
        },

        {
            path: '/',
            name: 'DatasetNone',
            component: Dataset,
            beforeEnter (to, from, next) {
                if (!Store.getters.isAuthenticated) {
                    next('/login')
                } else {
                    next()
                }
            }
        },

        {
            path: '/:id',
            name: 'Dataset',
            component: Dataset,
            beforeEnter (to, from, next) {
                if (!Store.getters.isAuthenticated) {
                    next('/login')
                } else {
                    next()
                }
            }
        }
    ]
})
