import Vue from 'vue'
import Vuex from 'vuex'
import { apiDatasetList } from '../api';

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
    user_uid: 1
}

const actions = {
    getDatasets(context) {
        return apiDatasetList(this.state.user_uid)
            .then((response) => {
                context.commit('setDatasets', { response: response.data })
            })
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