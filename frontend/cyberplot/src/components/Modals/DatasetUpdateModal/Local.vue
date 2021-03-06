<template>
<form id="form_update_local">
    <span v-if="updating">
        <header><img src="@/assets/images/icon_update_blue.svg"> Update dataset from local file</header>
    </span>
    <span v-else>
        <header><img src="@/assets/images/icon_dataset_new_blue.svg"> Add new dataset from local file</header>
    </span>
    
    <div v-if="step === 0">
        <img ref="fileDrop" src="@/assets/images/icon_source_file_blue.svg" alt="Drag file here" id="dataset_upload">
        <span class="errorText" v-show="invalidFile">Please select a valid CSV file.</span>
        <span class="errorText" v-show="uploadFailed">{{ uploadFailedMessage }}</span>
        <p id="file_prompt">
            Drag and drop a file or 
            <input @change="getFileFromPrompt()" type="file" ref="file" accept=".csv,.jpg,.jpeg,.png" style="display: none">
            <a @click="$refs.file.click()" id="button_copy" class="button_primary">Select file</a>
            <span id="supported_file_types">(supported types: csv, jpg, png)</span>
        </p>

        <nav>
            <a @click="backToInitial" id="button_back" class="interactive"><img src="@/assets/images/button_back.svg" alt="Back"></a>
        </nav>
    </div>

    <div v-else-if="step === 1" id="dataset_type_setup">
        <p>
            Please select dataset type.
        </p>

        <label>
            <input type="radio" name="type" value="multivariate" v-model="datasetType">
            <div class="button_secondary">
                <img src="@/assets/images/icon_dataset_multivariate_white.svg" v-if="datasetType == 'multivariate'">
                <img src="@/assets/images/icon_dataset_multivariate_blue.svg" v-else>
                Multivariate
            </div>
        </label>

        <label>
            <input type="radio" name="type" value="matrix" v-model="datasetType">
            <div class="button_secondary">
                <img src="@/assets/images/icon_dataset_matrix_white.svg" v-if="datasetType == 'matrix'">
                <img src="@/assets/images/icon_dataset_matrix_blue.svg" v-else>
                Matrix
            </div>
        </label>

        <nav>
            <a @click="goToPreviousStep" id="button_back" class="interactive"><img src="@/assets/images/button_back.svg" alt="Back"></a>
            <a @click="goToNextStep" id="button_next"><img src="@/assets/images/button_next.svg" alt="Next"></a>
        </nav>
    </div>
    
    <div v-else-if="step === 2" id="attribute_setup">
        <p>
            Are the following attribute labels?
        </p>

        <ul id="attribute_labels">
            <li v-for="(attribute, index) in attributeLabels" :key="index">
                {{ attribute }}
            </li>
        </ul>

        <label>
            <input type="radio" name="labels" value="yes" v-model="labelsCorrect">
            <div href="#" id="data_type_nominal_button" class="button_secondary">Yes</div>
        </label>

        <label>
            <input type="radio" name="labels" value="no" v-model="labelsCorrect">
            <div href="#" id="data_type_nominal_button" class="button_secondary">No</div>
        </label>

        <nav>
            <a @click="goToPreviousStep" id="button_back" class="interactive"><img src="@/assets/images/button_back.svg" alt="Back"></a>
            <a @click="uploadFile" id="button_next"><img src="@/assets/images/button_next.svg" alt="Next"></a>
        </nav>
    </div>

    <div v-else-if="step === 3" id="upload_in_progress">
        <p>
            Uploading dataset...
        </p>
    </div>
</form>
</template>

<script>
import {EventBus} from '../../../utils';

export default {
    name: 'DatasetUpdateModalLocal',
    props: {
        updating: Boolean,
        modalOpened: Boolean
    },
    data() {
        return {
            file: '',
            attributeLabels : [],
            invalidFile: false,
            uploadFailed: false,
            uploadFailedMessage: '',
            labelsCorrect: 'yes',
            datasetType: '',
            datasetCanBeMatrix: true,
            step: 0
        }
    },
    methods: {
        backToInitial: function() {
            this.$emit('backToInitial')
        },

        getFileFromPrompt: function() {
            this.file = this.$refs.file.files[0]
            this.validateFile()
        },

        validateFile: function() {
            this.invalidFile = false

            let reader = new FileReader()
            reader.onloadend = (e) => {
                if (e.target.readyState == FileReader.DONE) {
                    let extension = this.file.name.split('.').pop().toLowerCase()
                    let isImage = ['jpg', 'jpeg', 'png'].indexOf(extension) > -1

                    if(isImage) {
                        this.datasetType = 'matrix'
                        this.uploadFile()
                        return
                    }

                    let data = e.target.result.split('\n')
                    this.attributeLabels = data[0].split(',')

                    this.datasetCanBeMatrix = true
                    for(var rowIndex in data) {
                        let row = data[rowIndex].split(',')
                        for(var valueIndex in row) {
                            let value = row[valueIndex]
                            if(isNaN(value)) {
                                this.datasetCanBeMatrix = false
                                break
                            }
                        }
                        if(!this.datasetCanBeMatrix) {
                            break
                        }
                    }

                    this.datasetType = 'multivariate'
                    if(this.updating) {
                        this.datasetType = this.currentDataset.dataset.type
                        if(this.datasetType == 'matrix') {
                            this.uploadFile()
                        }
                        else {
                            this.step = 2
                        }
                    }
                    else {
                        if(this.datasetCanBeMatrix) {
                            this.step = 1
                        }
                        else {
                            this.step = 2
                        }
                    }
                }
            }
            
            let blob = this.file.slice(0, 1000)
            reader.readAsBinaryString(blob)
        },

        uploadFile: function() {
            let datasetName = this.file.name.split(".")[0]
            let containsHeader = 0
            if(this.datasetType === 'multivariate' && this.labelsCorrect === 'yes') {
                containsHeader = 1
            }
            let updating = this.updating ? 1 : 0
            this.$store.dispatch('uploadDataset', { name: datasetName,
                                                    type: this.datasetType,
                                                    identifier: this.apiKey,
                                                    containsHeader: containsHeader,
                                                    updating: updating,
                                                    file: this.file })
            this.step = 3
        },

        goToPreviousStep: function() {
            if(this.step === 2 && !this.datasetCanBeMatrix) {
                this.step = 0
            }
            else {
                this.step -= 1
            }
        },

        goToNextStep: function() {
            if(this.step === 1 && this.datasetType === 'matrix') {
                this.uploadFile()
            }
            else {
                this.step += 1
            }

        }
    },
    computed: {
        currentDataset() {
            return this.$store.state.currentDataset
        },

        apiKey() {
            if(this.updating) {
                return this.currentDataset.key
            }
            else {
                return this.$store.state.userKey
            }
        }
    },
    mounted() {
        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach((evt) => {
            this.$refs.fileDrop.addEventListener(evt, (e) => {
                e.preventDefault()
                e.stopPropagation()
            }, false)
        })

        this.$refs.fileDrop.addEventListener('drop', (e) => {
            this.file = e.dataTransfer.files[0]
            this.validateFile()
        })

        EventBus.$on('failedUpload', (msg) => {
            this.uploadFailed = true
            this.uploadFailedMessage = msg.response.data.result
            this.step = 0
        })

        EventBus.$on('successfulUpload', (msg) => {
            if(this.updating) {
                this.$store.dispatch('getCurrentDataset', { dataset_did: this.currentDataset.dataset.DID })
            }
        })
    },
    watch: {
        modalOpened: function(value, oldValue) {
            if(oldValue === false && value === true) {
                this.step = 0
                this.invalidFile = false
                this.uploadFailed = false
                this.labelsCorrect = 'yes'
                this.datasetType = 'multivariate'
            }
        }
    }
}
</script>

<style scoped>
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

.errorText {
    display: block;
    padding-bottom: 2em;
    padding-left: 0 !important;
    text-align: center;
}

#attribute_labels {
    overflow-x: scroll;
    background-color: white;
    border-radius: 0.3em;
    white-space: nowrap;
    padding: 1.5em;
}

#attribute_labels li {
    display: inline;
    padding: 1em;
    font-weight: bold;
    color: #3765ff;
    background: linear-gradient(to bottom, #64dafa, #1fbbfb 15%, #3765ff 100%);
    background-clip: border-box;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#file_prompt {
    text-align: center;
    margin: 0 !important;
}

#attribute_setup div {
    margin-top: 1em;
    margin-bottom: 1em;
}

#dataset_type_setup div {
    margin-top: 1em;
    margin-bottom: 1em;
}

#dataset_type_setup label img {
    vertical-align: middle;
    display: inline;
    width: 2em;
}

#supported_file_types {
    display: block;
    margin-top: 1em;
    color: #888;
    font-size: 0.9em;
}
</style>