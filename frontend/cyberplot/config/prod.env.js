'use strict'
module.exports = {
    NODE_ENV: '"production"',
    API_URL: JSON.stringify(`http://${process.env.CYBERPLOT_URL}/api`)
}
