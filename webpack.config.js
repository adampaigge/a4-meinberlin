var ExtractTextPlugin = require('extract-text-webpack-plugin')
var path = require('path')
var webpack = require('webpack');
var autoprefixer = require('autoprefixer');

module.exports = {
  entry: {
    meinberlin: [
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      'jquery',
      'js-cookie',
      'moment',
      'react',
      'react-addons-update',
      'react-dom'
    ]
  },
  devtool: 'eval',
  output: {
    libraryTarget: 'var',
    library: '[name]',
    path: './meinberlin/static/',
    publicPath: '/static/',
    filename: '[name].js'
  },
  externals: {
    'django': 'django'
  },
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!adhocracy4)/,  // exclude all dependencies but adhocracy4
        loader: 'babel-loader',
        query: {
          presets: ['babel-preset-es2015', 'babel-preset-react'].map(require.resolve)
        }
      },
      {
        test: /\.s?css$/,
        loader: ExtractTextPlugin.extract('style?sourceMap', '!css?sourceMap!postcss?sourceMap!sass?sourceMap')
      }
    ]
  },
  postcss: [
    autoprefixer({browsers: ['last 3 versions', 'ie >= 10']})
  ],
  resolve: {
    fallback: path.join(__dirname, 'node_modules'),
    extensions: ['', '.js', '.jsx', '.scss', '.css']
  },
  resolveLoader: {
    fallback: path.join(__dirname, 'node_modules')
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.js'),
    new ExtractTextPlugin('[name].css')
  ]
}
