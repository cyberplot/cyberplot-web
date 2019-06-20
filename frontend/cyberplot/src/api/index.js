import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api'

/* when login token expires, redirect user to login */
axios.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        if (error.response.status === 401 && error.response.data.result === 'Authentication token expired.') {
            window.location = '/login/'
        }
        else {
            return Promise.reject(error)
        }
    }
)

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
    return axios.post(`${API_URL}/dataset_delete/${did}/`, null, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDeleteDatasetVersion(did, vid, jwt) {
    return axios.post(`${API_URL}/dataset_version_delete/${did}/${vid}/`, null, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDownloadDataset(did, jwt) {
    return axios.get(`${API_URL}/dataset_download/${did}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiDownloadDatasetVersion(did, vid, jwt) {
    return axios.get(`${API_URL}/dataset_version_download/${did}/${vid}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiUploadDataset(name, identifier, containsHeader, file, jwt) {
    let formData = new FormData()
    formData.append('json', JSON.stringify({json: {name: name, identifier: identifier, containsHeader: containsHeader}}))
    formData.append('file', file)
    return axios.post(`${API_URL}/dataset_upload/`, formData, {headers: {Authorization: `Bearer: ${jwt}`,
                                                            'Content-Type': 'multipart/form-data'}})
}

export function apiShareDataset(did, uidReceiver, jwt) {
    return axios.post(`${API_URL}/dataset_share/${did}/${uidReceiver}/`, null, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiShareRequests(jwt) {
    return axios.get(`${API_URL}/share_requests/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiUserAutocomplete(phrase, jwt) {
    return axios.get(`${API_URL}/user_autocomplete/${phrase}/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}

export function apiGetUserInfo(jwt) {
    return axios.get(`${API_URL}/user_info/`, {headers: {Authorization: `Bearer: ${jwt}`}})
}