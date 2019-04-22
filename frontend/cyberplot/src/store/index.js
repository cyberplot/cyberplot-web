import Vue from 'vue'
import Vuex from 'vuex'

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
    notificationsOpened: false
}

const actions = {

}

const mutations = {
    openModal(state, modal) {
        state.openedModals[modal] = true
    },

    closeModals(state) {
        for(var modal in state.openedModals) {
            state.openedModals[modal] = false
        }
    },
    
    toggleNotifications(state) {
        state.notificationsOpened = !state.notificationsOpened
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