import Vue from 'vue'
import Vuex from 'vuex'
import { apiDatasetList, apiDataset, apiDeleteDataset, apiDownloadDataset, apiChangeDataset, apiLogin, apiSignup, apiGetUserInfo, apiUploadDataset } from '../api'
import { isValidJwt, EventBus } from '../utils'
import router from '../router'

Vue.use(Vuex)

const state = {
    openedModals: {
        userSettings: false,
        datasetRename: false,
        datasetUpdate: false,
        datasetDelete: false,
        datasetShare: false,
        datasetVersion: false,
        attributeRename: false
    },
    notificationsOpened: false,
    datasetUpdateUpdating: false, /* are we updating an existing dataset? */
    datasets: [],
    currentDataset: [],
    selectedAttribute: 0,
    currentUser: '',
    userKey: '',
    jwt: ''
}

const actions = {
    login(context, userData) {
        context.commit('setUserData', { userData })
        return apiLogin(userData)
            .then(response => context.commit('setJwtToken', { jwt: response.data }))
            .catch(error => {
                EventBus.$emit('failedAuthentication', error)
            })
    },

    signup(context, userData) {
        context.commit('setUserData', { userData })
        return apiSignup(userData)
            .catch(error => {
                EventBus.$emit('failedRegistering', error)
            })
    },

    getDatasets(context) {
        return apiDatasetList(context.state.jwt.token)
            .then((response) => {
                context.commit('setDatasets', { response: response.data })
            })
    },

    getCurrentDataset(context, { dataset_did }) {
        return apiDataset(dataset_did, context.state.jwt.token)
            .then((response) => {
                context.commit('setCurrentDataset', { response: response.data })
            })
    },
    
    getUserInformation(context) {
        return apiGetUserInfo(context.state.jwt.token)
            .then((response) => {
                context.commit('setCurrentUser', { response: response.data })
            })
    },

    deleteCurrentDataset(context) {
        apiDeleteDataset(this.state.currentDataset.dataset.DID, context.state.jwt.token)
            .then((response) => {
                context.dispatch('getDatasets')
            })
        router.push({ path: `/` })
        context.commit('closeModals')
    },

    downloadCurrentDataset(context) {
        apiDownloadDataset(this.state.currentDataset.dataset.DID, context.state.jwt.token)
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'dataset.csv')
                document.body.appendChild(link)
                link.click()
                link.remove()
            })
    },

    changeCurrentDataset(context, leaveDialogOpen) {
        apiChangeDataset(this.state.currentDataset.dataset.DID, this.state.currentDataset, context.state.jwt.token)
            .then((response) => {
                context.dispatch('getDatasets')
            })

        if(leaveDialogOpen != true) {
            context.commit('closeModals')
        }
    },

    uploadDataset(context, dataset) {
        apiUploadDataset(dataset.name, dataset.identifier, dataset.containsHeader, dataset.file, context.state.jwt.token)
            .then((response) => {
                context.dispatch('getDatasets')
                context.commit('closeModals')
                EventBus.$emit('successfulUpload')
            })
            .catch(error => {
                EventBus.$emit('failedUpload', error)
            })
    }
}

const mutations = {
    setUserData(state, payload) {
        state.userData = payload.userData
    },

    setJwtToken(state, payload) {
        localStorage.token = payload.jwt.token
        state.jwt = payload.jwt
    },

    openModal(state, modal) {
        mutations.closeModals(state)

        if(modal === 'datasetAdd' || modal === 'datasetUpdate') {
            state.datasetUpdateUpdating = (modal == 'datasetUpdate')
        }

        if(modal === 'datasetAdd') {
            modal = 'datasetUpdate'
        }

        state.openedModals[modal] = true
    },

    closeModals(state) {
        for(var modal in state.openedModals) {
            state.openedModals[modal] = false
        }
    },
    
    toggleNotifications(state) {
        state.notificationsOpened = !state.notificationsOpened
    },

    setDatasets(state, payload) {
        state.datasets = payload.response.datasets
    },

    setCurrentDataset(state, payload) {
        state.currentDataset = payload.response
        state.selectedAttribute = 0 /* deselect attribute when changing datasets */
    },

    setCurrentUser(state, payload) {
        state.currentUser = payload.response.user
        state.userKey = payload.response.key
    },

    selectAttribute(state, attribute) {
        state.selectedAttribute = attribute
    }  
}

const getters = {
    isAuthenticated(state) {
        return isValidJwt(state.jwt.token)
    },

    /* overlay is opened whenever at least one modal is opened */
    overlayOpened() {
        for(var modal in state.openedModals) {
            if(state.openedModals[modal]) {
                return true
            }
        }
        return false
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store