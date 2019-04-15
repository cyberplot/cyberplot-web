<template>
<section id="sidebar">
    <ul id="dataset_listing">
        <router-link :to="`${dataset.id}`" href="#" v-for="dataset in datasets" :key="dataset.id">
            <li>{{ dataset.name }}</li>
        </router-link>
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