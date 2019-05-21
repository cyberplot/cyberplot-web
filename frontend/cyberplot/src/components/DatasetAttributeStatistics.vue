<template>
<div id="attribute_statistics" v-if="selectedAttribute != -1">
    <dl>
        <dt><img src="@/assets/images/icon_statistics_gray.svg"> Statistics</dt>
        <dd>
            <table>
                <tr>
                    <td>{{ beautify(currentDataset.statistics[selectedAttribute].minimum) }}</td>
                    <td>{{ beautify(currentDataset.statistics[selectedAttribute].Q1) }}</td>
                    <td>{{ beautify(currentDataset.statistics[selectedAttribute].median) }}</td>
                    <td>{{ beautify(currentDataset.statistics[selectedAttribute].Q3) }}</td>
                    <td>{{ beautify(currentDataset.statistics[selectedAttribute].maximum) }}</td>
                </tr>
                <tr><td>min</td><td>1Q</td><td>med</td><td>3Q</td><td>max</td></tr>
            </table>

            <ul>
                <li>
                    <img src="@/assets/images/icon_mean_gray.svg" alt="Arithmetic mean">
                    {{ currentDataset.statistics[selectedAttribute].mean.toFixed(2) }}
                </li>
                <li>
                    <img src="@/assets/images/icon_standard_deviation_gray.svg" alt="Standard deviation">
                    {{ currentDataset.statistics[selectedAttribute].sdev.toFixed(2) }}
                </li>
            </ul>
        </dd>
    </dl>
</div>
</template>

<script>
export default {
    name: 'DatasetAttributeStatistics',
    methods: {
        beautify: function(number) {
            if(number > 1000000) {
                return '~' + (number / 1000000).toFixed(0) + 'M'
            }
            else if(number > 1000) {
                return '~' + (number / 1000).toFixed(0) + 'k'
            }
            else if(number * 10 % 10 == 0) {
                return number.toFixed(0)
            }
            else {
                return number.toFixed(1)
            }
        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        selectedAttribute() {
            var attributeAID = this.$store.state.selectedAttribute

            if(!attributeAID) {
                return -1
            }

            for(let [index, attribute] of this.currentDataset.statistics.entries()) {
                if(attribute.AID == attributeAID) {
                    return index
                }
            }

            return -1 /* if there is no statistics record associated with attribute, display nothing */
        }
    }
}
</script>

<style>
#attribute_statistics {
    flex: 1;
}

#attribute_statistics table {
    background-color: #eee;
    border-radius: 0.3em;
    padding: 0.5em;
    border-spacing: 0;
}

#attribute_statistics td {
    padding: 0.2em;
    width: 3em;
    text-align: center;
}

#attribute_statistics tr:nth-of-type(1) {
    font-family: 'Libre Franklin Bold';
}

#attribute_statistics tr:nth-of-type(2) {
    font-size: 0.8em;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(2) {
    border: 1px solid #4b4b4b;
    border-right: none;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(3) {
    border-top: 1px solid #4b4b4b;
    border-bottom: 1px solid #4b4b4b;
}

#attribute_statistics tr:nth-of-type(1) td:nth-of-type(4) {
    border: 1px solid #4b4b4b;
    border-left: none;
}

#attribute_statistics ul {
    list-style: none;
    padding: 0;
}

#attribute_statistics li {
    display: inline-block;
    width: 8.6em;
    border-radius: 0.3em;
    border: 1px solid #4b4b4b;
    padding: 0.1em;
    margin-top: 0.5em;
    font-family: 'Libre Franklin Bold';
}

#attribute_statistics li:nth-of-type(1) {
    margin-right: 0.1em;
}

#attribute_statistics li:nth-of-type(2) {
    margin-left: 0.1em;
}
</style>