<template>
<section id="sidebar">
    <ul id="dataset_listing">
        <router-link :to="`${dataset.DID}`" href="#" v-for="dataset in datasets" :key="dataset.id">
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
        }
    },
    computed: {
        datasets() {
            return this.$store.state.datasets
        }
    }
}
</script>