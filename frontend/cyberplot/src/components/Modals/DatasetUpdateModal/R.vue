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
        <p>After importing the package, use the following command to update <strong>Iris Dataset</strong>.</p>

        <div class="cli_box">
            cyberplot.update(your_datatable,<br />
            id = "<strong>346f9f436c0d99fbb937658af47a09f9</strong>")
        </div>
        <a href="#" id="button_copy" class="button_secondary">Copy dataset identifier</a>
    </span>
    <span v-else>
        <p>After importing the package, use the following command to upload a new dataset.</p>

        <div class="cli_box">
            cyberplot.update(your_datatable,<br />
            id = "<strong>346f9f436c0d99fbb937658af47a09f9</strong>",<br />
            name = "DATASET_NAME")
        </div>
        <a href="#" id="button_copy" class="button_secondary">Copy user identifier</a>
    </span>

    <nav>
        <a href="#" id="button_back"><img src="@/assets/images/button_back.svg" alt="Back"></a>
    </nav>
</form>
</template>

<script>
export default {
    name: 'DatasetUpdateModalR',
    props: {
        updating: Boolean
    }
}
</script>