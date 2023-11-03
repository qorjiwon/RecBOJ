const {merge} = require('webpack-merge')
const common = require('./webpack.config.js')

module.exports = merge(
    common,
    {
        mode: "production",
        devtool: "cheap-module-source-map",
    }
)
