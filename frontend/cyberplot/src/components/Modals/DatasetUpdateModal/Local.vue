<template>
<form id="form_update_local">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset from local file</header>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset from local file</header>
    </span>

    <img src="@/assets/images/icon_source_file_blue.svg" alt="Drag file here" id="dataset_upload">

    <p>
        Drag and drop a csv file or 
        <input type="file" ref="file" style="display: none">
        <a @click="$refs.file.click()" id="button_copy" class="button_primary">Select file</a>
    </p>

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
        }
    }
}
</script>

<style>
#form_update_local p {
    text-align: center;
    margin: 0;
}

#form_update_local .button_primary {
    margin-left: 0.5em;
    display: inline;
}

#dataset_upload {
    width: 8em;
    margin-left: auto;
    margin-right: auto;
    display: block;
    padding: 1.5em;
}
</style>