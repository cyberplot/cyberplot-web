import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt(jwt) {  
    if (!jwt || jwt.split('.').length < 3) {
        return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    return now < exp
}

export function downloadFile(response) {
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'dataset.csv')
    document.body.appendChild(link)
    link.click()
    link.remove()
}