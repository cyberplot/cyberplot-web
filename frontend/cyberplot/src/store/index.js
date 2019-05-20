import Vue from 'vue'
import Vuex from 'vuex'
import { apiDatasetList, apiDataset, apiDeleteDataset, apiChangeDataset } from '../api'
import router from '../router'

Vue.use(Vuex)

const state = {
    openedModals: {
        userSettings: false,
        datasetRename: false,
        datasetUpdate: false,
        datasetDelete: false,
        datasetShare: false,
        attributeRename: false
    },
    notificationsOpened: false,
    datasetUpdateUpdating: false, /* are we updating an existing dataset? */
    datasets: [],
    currentDataset: [],
    selectedAttribute: 0,
    user_uid: 1
}

const actions = {
    getDatasets(context) {
        return apiDatasetList(this.state.user_uid)
            .then((response) => {
                context.commit('setDatasets', { response: response.data })
            })
    },

    getCurrentDataset(context, { dataset_did }) {
        return apiDataset(this.state.user_uid, dataset_did)
            .then((response) => {
                context.commit('setCurrentDataset', { response: response.data })
            })
    },

    deleteCurrentDataset(context) {
        apiDeleteDataset(this.state.user_uid, this.state.currentDataset.dataset.DID)
        .then((response) => {
            context.dispatch('getDatasets')
        })
        router.push({ path: `/dataset/` })
        context.commit('closeModals')
    },

    changeCurrentDataset(context) {
        apiChangeDataset(this.state.user_uid, this.state.currentDataset.dataset.DID, this.state.currentDataset)
        .then((response) => {
            context.dispatch('getDatasets')
        })
        context.commit('closeModals')
    }
}

const mutations = {
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

    selectAttribute(state, attribute) {
        state.selectedAttribute = attribute
    }  
}

const getters = {
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