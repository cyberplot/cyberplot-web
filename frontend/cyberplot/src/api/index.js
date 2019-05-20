import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function apiDatasetList(uid) {
    return axios.get(`${API_URL}/dataset_list/${uid}/`)
}

export function apiDataset(uid, did) {
    return axios.get(`${API_URL}/dataset/${uid}/${did}/`)
}

export function apiChangeDataset(uid, did, datasetData) {
    return axios.put(`${API_URL}/dataset/${uid}/${did}/`, datasetData)
}

export function apiDeleteDataset(uid, did) {
    return axios.post(`${API_URL}/dataset_delete/${uid}/${did}/`)
}

export function apiUserAutocomplete(phrase) {
    return axios.get(`${API_URL}/user_autocomplete/${phrase}/`)
}