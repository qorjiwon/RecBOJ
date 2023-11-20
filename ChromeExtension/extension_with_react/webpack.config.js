const path = require('path')
const CopyPlugin = require("copy-webpack-plugin")
const HtmlPlugin = require('html-webpack-plugin')
const autoprefixer = require('autoprefixer')
const tailwindcss = require('tailwindcss')

/*
new tab  >> manifest
"chrome_url_overrides" : {
    "newtab": "newTab.html"
  },
*/

module.exports = {
    mode: "development",
    devtool: "cheap-module-source-map",
    entry: {
        contentScript: path.resolve('./src/contentScript/contentScript.tsx'),
    },
    module: {
        rules: [
            {
                use: "ts-loader",
                test: /\.tsx$/,
                exclude: /node_modules/
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader", {
                    loader: 'postcss-loader',
                    options: {
                        postcssOptions: {
                            ident: 'postcss',
                            plugins: [tailwindcss, autoprefixer],
                        },
                    }
                }],
            }, 
            {
                test: /\.(jpe?g|png|gif|svg)$/i,
                type: "assets/resource",
                use: "assets/resource",
            },
        ]
    },
    plugins: 
    [
        new CopyPlugin({
            patterns: [
                {from: path.resolve('src/static'),
                to: path.resolve('dist')},
            ]
        }),
        ...getHtmlPlugins([
            'popup',
            'options',
        ]),
        
    ],
    resolve: {
        extensions: ['.tsx', '.ts', '.js']
    },
    output: {
        filename: '[name].js'
    },
    optimization: {
        splitChunks: {
            chunks(chunk) {
                return chunk.name !== 'contentScript';
            }
        },
    },
}

function getHtmlPlugins(chunks) {
    return chunks.map(chunk => new HtmlPlugin(
        {
            title: 'React Extension',
            filename: `${chunk}.html`,
            chunks: [chunk]
        }
    ))
}