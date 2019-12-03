<template>
<section id="sidebar">
    <ul id="dataset_listing">
        <router-link v-on:click.native="changeDataset(dataset.DID)" :to="`${dataset.DID}`" v-for="dataset in datasets" :key="dataset.id">
            <li>
                <img src="@/assets/images/icon_dataset_multivariate.svg" alt="Multivariate dataset" v-if="dataset.type == 'multivariate'">
                <img src="@/assets/images/icon_dataset_matrix.svg" alt="Multivariate dataset" v-if="dataset.type == 'matrix'">
                {{ dataset.name }}
            </li>
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

<style scoped>
#dataset_listing {
    overflow-y: scroll;
    scrollbar-width: none;
    list-style: none;
    padding: 1em;
    margin: 1em;
    margin-right: 0;
    margin: 0;
    padding-right: 0;
    flex-grow: 1;
}

#dataset_listing .router-link-active li {
    background-color: #ececec;
    border-bottom: 5px solid #1fbbfb;
}

#dataset_listing li {
    border-radius: 0.3em 0 0 0.3em;
    padding: 0.6em;
    font-family: 'Libre Franklin Bold';
    color: #888;
}

#dataset_listing li img {
    margin-right: 0.5em;
}

#dataset_listing li:hover {
    background-color: #eee;
    border-radius: 0.3em 0 0 0.3em;
}

#dataset_listing a {
    text-decoration: none;
}

#dataset_add_button {
    height: 3em;
    display: block;
    margin: 1em;
    text-align: center;
    line-height: 3em;
    position: relative;
}

#sidebar {
    width: 40em;
    display: flex;
    flex-direction: column;
    align-content: stretch;
    background-color: #f9f9f9;
}
</style>