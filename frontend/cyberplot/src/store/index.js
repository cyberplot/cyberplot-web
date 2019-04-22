import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    openedModals: {
        userSettings: false
    },
    notificationsOpened: false
}

const actions = {

}

const mutations = {
    openModal(modal) {
        openedModals[modal] = true
    },

    closeModals() {
        for(var modal in state.openedModals) {
            state.openedModals[modal] = false
        }
    },
    
    toggleNotifications() {
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