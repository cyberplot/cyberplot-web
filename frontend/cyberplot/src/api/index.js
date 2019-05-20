import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

export function apiLogin(userData) {
    return axios.post(`${API_URL}/login/`, userData)
}

export function apiSignup(userData) {
    return axios.post(`${API_URL}/signup/`, userData)
}

export function apiDatasetList(jwt) {
    return axios.get(`${API_URL}/dataset_list/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDataset(did, jwt) {
    return axios.get(`${API_URL}/dataset/${did}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiChangeDataset(did, datasetData, jwt) {
    return axios.put(`${API_URL}/dataset/${did}/`, datasetData, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDeleteDataset(did, jwt) {
    return axios.post(`${API_URL}/dataset_delete/${did}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDownloadDataset(did, jwt) {
    return axios.get(`${API_URL}/dataset_download/${did}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiUserAutocomplete(phrase, jwt) {
    return axios.get(`${API_URL}/user_autocomplete/${phrase}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiGetUserInfo(jwt) {
    return axios.get(`${API_URL}/user_info/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}