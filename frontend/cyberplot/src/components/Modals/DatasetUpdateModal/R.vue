<template>
<form id="form_update_r">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset using R</header>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset using R</header>
    </span>

    <p>To upload R dataframe, first download the cyberplot package by running the following command.</p>
    <div class="cli_box">
        install.packages("cyberplot")<br />
        library("cyberplot")
    </div>

    <span v-if="updating">
        <p>After importing the package, use the following command to update <strong>{{ currentDataset.dataset.name }}</strong>.</p>

        <div class="cli_box">
            cyberplot.update(your_datatable,<br />
            id = "<strong>{{ currentDataset.key }}</strong>")
        </div>
        <a id="button_copy" class="button_secondary" v-clipboard="currentDataset.key">Copy dataset identifier</a>
    </span>
    <span v-else>
        <p>After importing the package, use the following command to upload a new dataset.</p>

        <div class="cli_box">
            cyberplot.new(your_datatable,<br />
            id = "<strong>{{ userKey }}</strong>",<br />
            name = "DATASET_NAME")
        </div>
        <a id="button_copy" class="button_secondary" v-clipboard="userKey">Copy user identifier</a>
    </span>

    <nav>
        <a @click="backToInitial" id="button_back" class="interactive"><img src="@/assets/images/button_back.svg" alt="Back"></a>
    </nav>
</form>
</template>

<script>
export default {
    name: 'DatasetUpdateModalR',
    props: {
        updating: Boolean
    },
    methods: {
        backToInitial: function() {
            this.$emit('backToInitial')
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        userKey() {
            return this.$store.state.userKey
        }
    }
}
</script>

<style scoped>
#form_update_r .button_secondary {
    margin-left: 4.1em;
}
</style>