<template>
<form id="form_update">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset</header>
        <p>Please select data source to update <strong>Iris Dataset</strong>.</p>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset</header>
        <p>Please select data source to continue.</p>
    </span>

    <label>
        <input type="radio" name="source" value="local">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_file_blue.svg">
            Local file
        </div>
    </label>

    <label>
        <input type="radio" name="source" value="local">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_database_blue.svg">
            Remote database
        </div>
    </label>

    <label>
        <input type="radio" name="source" value="local">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_python_blue.svg">
            Python
        </div>
    </label>
    
    <label>
        <input type="radio" name="source" value="local">
        <div class="button_secondary">
            <img src="@/assets/images/icon_source_r_blue.svg">
            R data frame
        </div>
    </label>

    <nav>
        <a href="#" id="button_next"><img src="@/assets/images/button_next.svg" alt="Next"></a>
        <a href="#" id="button_back"><img src="@/assets/images/button_back.svg" alt="Back"></a>
    </nav>
</form>
</template>

<script>
export default {
    name: 'DatasetUpdateModalBase',
    props: {
        updating: Boolean
    }
}
</script>
