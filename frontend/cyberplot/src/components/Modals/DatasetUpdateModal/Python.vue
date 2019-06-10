<template>
<form id="form_update_python">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset using Python</header>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset using Python</header>
    </span>

    <p>To use Python with Cyberplot, first install the cyberplot package from PyPI repository by running the following command in the terminal.</p>
    <div class="cli_box">
        pip install cyberplot
    </div>

    <span v-if="updating">
        <p>After installing the package, use the following command in your Python environment to update <strong>{{ currentDataset.dataset.name }}</strong>.</p>

        <div class="cli_box">
            import cyberplot<br />
            cyberplot.update(your_array,<br />
            id = "<strong>{{ currentDataset.key }}</strong>")
        </div>
        <a id="button_copy" class="button_secondary" v-clipboard="currentDataset.key">Copy dataset identifier</a>
    </span>
    <span v-else>
        <p>After installing the package, use the following command in your Python environment to upload a new dataset.</p>

        <div class="cli_box">
            import cyberplot<br />
            cyberplot.new(your_array,<br />
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
    name: 'DatasetUpdateModalPython',
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
#form_update_python .button_secondary {
    margin-left: 4.1em;
}
</style>