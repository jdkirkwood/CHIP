const autoprefixer = require('autoprefixer')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
var path = require('path')
const extractSass = new ExtractTextPlugin({
  filename: 'main.css',
})

module.exports = {
  mode: 'development',
  devtool: 'source-map',
  entry: './main.js',
  output: {
    filename: 'output.js',
    path: path.resolve(__dirname)
  },
//   entry: './webpack_entry.py',
//   output: {
//     filename: 'todos.js',
//     path: path.resolve(__dirname, 'todos/static')
//   },  
  module: {
    rules: [
      { test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'url-loader?limit=10000&mimetype=application/font-woff' },
      { test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/, loader: 'file-loader' },
      {
        test: /\.py$/,
        loader: 'py-loader',
        options: {
          compiler: 'transcrypt'
        }
      },
      {
        test: /\.s(a|c)ss$/,
        use: extractSass.extract({
          use: [
            {
              loader: 'css-loader',
              options: {
                sourceMap: true
              }
            },
            {
              loader: 'postcss-loader',
              options: {
                sourceMap: true,
                plugins: () => [autoprefixer()]
              }
            },
            {
              loader: 'sass-loader',
              options: {
                sourceMap: true,
                includePaths: ['./node_modules']
              }
            }
          ]
        })
      }
    ]
  },
  plugins: [
    extractSass
  ]
}
