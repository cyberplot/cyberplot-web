<template>
<content>
    <VueTitle :title="datasetSelected() ? currentDataset.dataset.name : 'cyberplot'" />

    <nav id="navigation_main">
        <h1>Cyberplot</h1>
        <img src="@/assets/images/logo_white.svg" alt="Cyberplot logo" id="cyberplot_logo">
        <a @click="logout" id="logout_button" class="button_secondary">Log out</a>
        <a @click="toggleNotifications" id="user_label" class="interactive">
            <img src="@/assets/images/icon_user_white_notification.svg" alt="User profile" id="icon_user">
            {{ this.currentUser.username }}
        </a>
    </nav>
    <NotificationCenter />

    <main>
        <DatasetList />
        <DatasetView v-if="datasetSelected()" />
        <section v-else id="content">
            <img src="@/assets/images/icon_dataset_gray.svg" alt="No dataset selected" id="dataset_placeholder_icon" />
        </section>
    </main>

    <DatasetOverlay />
</content>
</template>

<script>
import NotificationCenter from './NotificationCenter.vue'
import DatasetOverlay from './DatasetOverlay.vue'
import DatasetList from './DatasetList.vue'
import DatasetView from './DatasetView.vue'
import VueTitle from './Helpers/Title.vue'

export default {
    name: 'Dataset',
    components: {
        DatasetList,
        DatasetView,
        NotificationCenter,
        DatasetOverlay,
        VueTitle
    },
    beforeMount() {
        this.$store.dispatch('getUserInformation')
    },
    methods: {
        datasetSelected: function() {
            return this.$route.name === "Dataset"
        },

        toggleNotifications: function() {
            this.$store.commit('toggleNotifications')
        },

        logout: function() {
            this.$store.state.jwt = ''
            this.$router.push('/login/')
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        currentUser() {
            return this.$store.state.currentUser
        }
    }
}
</script>

<style>
content {
    display: contents;
}

#dataset_placeholder_icon {
    top: 50%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    display: block;
    margin: 0;
    position: relative;
    width: 16em;
}

dt {
    font-family: 'Libre Franklin Bold';
}

a img {
    vertical-align: middle;
}

.selector a {
    margin-right: 0.5em;
}
</style>