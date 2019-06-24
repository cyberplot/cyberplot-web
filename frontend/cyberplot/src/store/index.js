import Vue from 'vue'
import Vuex from 'vuex'
import { apiDatasetList, apiDataset, apiDeleteDataset, apiDeleteDatasetVersion, apiDownloadDataset, apiDownloadDatasetVersion, apiChangeDataset, apiLogin, apiSignup, apiGetUserInfo, apiUploadDataset, apiUserAutocomplete, apiShareDataset, apiShareRequests, apiAnswerShareRequest } from '../api'
import { isValidJwt, EventBus, downloadFile } from '../utils'
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
        attributeRename: false,
        attributeMissingValue: false
    },
    notificationsOpened: false,
    shareRequests: [],
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
        context.commit('unsetCurrentDataset')
        return apiLogin(userData)
            .then(response => context.commit('setJwtToken', { jwt: response.data }))
            .catch(error => {
                EventBus.$emit('failedAuthentication', error)
            })
    },

    signup(context, userData) {
        context.commit('setUserData', { userData })
        return apiSignup(userData)
            .then(response => EventBus.$emit('completeRegistering'))
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
                context.commit('unsetCurrentDataset')
                context.dispatch('getDatasets')
                router.push({ path: `/` })
            })
        context.commit('closeModals')
    },

    deleteDatasetVersion(context, vid) {
        apiDeleteDatasetVersion(this.state.currentDataset.dataset.DID, vid, context.state.jwt.token)
            .then((response) => {
                let index = this.state.currentDataset.datasetVersions.findIndex(element => element.VID === vid)
                this.state.currentDataset.datasetVersions.splice(index, 1)
            })
    },

    downloadCurrentDataset(context) {
        apiDownloadDataset(this.state.currentDataset.dataset.DID, context.state.jwt.token)
            .then((response) => {
                downloadFile(response)
            })
    },

    downloadDatasetVersion(context, vid) {
        apiDownloadDatasetVersion(this.state.currentDataset.dataset.DID, vid, context.state.jwt.token)
            .then((response) => {
                downloadFile(response)
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
        apiUploadDataset(dataset.name, dataset.identifier, dataset.containsHeader, dataset.updating, dataset.file, context.state.jwt.token)
            .then((response) => {
                context.dispatch('getDatasets')
                context.commit('closeModals')
                EventBus.$emit('successfulUpload')
            })
            .catch(error => {
                EventBus.$emit('failedUpload', error)
            })
    },

    shareCurrentDataset(context, uidReceiver) {
        apiShareDataset(this.state.currentDataset.dataset.DID, uidReceiver, context.state.jwt.token)
            .then((response) => {
                context.commit('closeModals')
            })
            .catch(error => {
                EventBus.$emit('failedShare')
            })
    },

    getShareRequests(context) {
        return apiShareRequests(context.state.jwt.token)
            .then((response) => {
                context.commit('setShareRequests', { response: response.data })
            })
    },

    answerShareRequest(context, request) {
        return apiAnswerShareRequest(request, context.state.jwt.token)
            .then((response) => {
                context.dispatch('getShareRequests')
                context.dispatch('getDatasets')
            })
    },

    userAutocomplete(context, phrase) {
        apiUserAutocomplete(phrase, context.state.jwt.token)
            .then((response) => {
                EventBus.$emit('autocomplete', response.data.users)
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

    unsetCurrentDataset(state) {
        state.currentDataset = []
    },

    setCurrentUser(state, payload) {
        state.currentUser = payload.response.user
        state.userKey = payload.response.key
    },

    setShareRequests(state, payload) {
        state.shareRequests = payload.response.requests

        if(state.shareRequests.length === 0) {
            state.notificationsOpened = false
        }
        else {
            state.notificationsOpened = true
        }
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
    },

    selectedAttributeData() {
        var attributeAID = state.selectedAttribute
        for(let [index, attribute] of state.currentDataset.attributes.entries()) {
            if(attribute.AID == attributeAID) {
                return attribute
            }
        }
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
})

export default store