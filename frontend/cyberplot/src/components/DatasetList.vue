<template>
<section id="sidebar">
    <ul id="dataset_listing">
        <router-link v-on:click.native="changeDataset(dataset.DID)" :to="`${dataset.DID}`" v-for="dataset in datasets" :key="dataset.id">
            <li>{{ dataset.name }}</li>
        </router-link>
    </ul>

    <a @click="showNewDatasetModal" id="dataset_add_button" class="button_primary">Add new dataset</a>
</section>
</template>

<script>
export default {
    name: "DatasetList",
    beforeMount() {
        this.$store.dispatch('getDatasets')
    },
    methods: {
        showNewDatasetModal: function() {
            this.$store.commit('openModal', 'datasetAdd')
        },

        changeDataset: function(DID) {
            this.$store.dispatch('getCurrentDataset', { dataset_did: DID })
        }
    },
    computed: {
        datasets() {
            return this.$store.state.datasets
        }
    }
}
</script>

<style>
#dataset_listing {
    overflow-y: scroll;
    scrollbar-width: none;
}

#dataset_listing::-webkit-scrollbar {
    width: 0;
    height: 0;
}
</style>