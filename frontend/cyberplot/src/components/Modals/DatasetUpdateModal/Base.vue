<template>
<form id="form_update">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset</header>
        <p>Please select data source to update <strong>{{ currentDataset.dataset.name }}</strong>.</p>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset</header>
        <p>Please select data source to continue.</p>
    </span>

    <label>
        <input type="radio" name="source" value="local" v-model="dataSource">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_file_white.svg" v-if="dataSource == 'local'">
            <img src="@/assets/images/icon_source_file_blue.svg" v-else>
            Local file
        </div>
    </label>

    <label>
        <input type="radio" name="source" value="database" v-model="dataSource">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_database_white.svg" v-if="dataSource == 'database'">
            <img src="@/assets/images/icon_source_database_blue.svg" v-else>
            Remote database
        </div>
    </label>

    <label>
        <input type="radio" name="source" value="python" v-model="dataSource">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_python_white.svg" v-if="dataSource == 'python'">
            <img src="@/assets/images/icon_source_python_blue.svg" v-else>
            Python
        </div>
    </label>
    
    <label>
        <input type="radio" name="source" value="r" v-model="dataSource">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_r_white.svg" v-if="dataSource == 'r'">
            <img src="@/assets/images/icon_source_r_blue.svg" v-else>
            R data frame
        </div>
    </label>

    <nav>
        <a href="#" id="button_next" @click="submitForm"><img src="@/assets/images/button_next.svg" alt="Next"></a>
        <a href="#" id="button_back"><img src="@/assets/images/button_back.svg" alt="Back"></a>
    </nav>
</form>
</template>

<script>
export default {
    name: 'DatasetUpdateModalBase',
    props: {
        updating: Boolean,
    },
    data() {
        return {
            dataSource: ''
        }
    },
    methods: {
        submitForm: function() {
            if(this.dataSource != '') {
                this.$emit('formSubmit', this.dataSource)
            }
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        }
    }
}
</script>
