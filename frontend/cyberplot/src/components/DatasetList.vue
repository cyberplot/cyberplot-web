<template>
<section id="sidebar">
    <ul id="dataset_listing">
        <a href="#" v-for="dataset in datasets" :key="dataset.id">
        <li>{{ dataset.name }}</li></a>
        <a href="#"><li id="active_dataset_button">dataset2</li></a>
    </ul>

    <a href="#" id="dataset_add_button" class="button_primary">Add new dataset</a>
</section>
</template>

<script>
export default {
    name: "DatasetList",
    data() {
        return {
            datasets: [
                {
                    id: 1,
                    name: "Employee Satisfaction Q4"
                },
                {
                    id: 2,
                    name: "Quarterly Earnings"
                },
                {
                    id: 3,
                    name: "Iris Dataset"
                },
                {
                    id: 4,
                    name: "Lab Measurements"
                }
            ]
        }
    }
}
</script>