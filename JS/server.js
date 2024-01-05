const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 3000;

// Serve static files (HTML, JS, CSS) from a specific directory
app.use(express.static('.')); // Set this to your files' directory

// Proxy configuration for Blazegraph
app.use('/blazegraph', createProxyMiddleware({
  target: 'http://192.168.1.56:9999',
  changeOrigin: true,
  pathRewrite: {
    '^/blazegraph': '/blazegraph/namespace/formula1/sparql', // Adjust as needed
  },
  onProxyRes: function (proxyRes) {
    proxyRes.headers['Access-Control-Allow-Origin'] = '*';
  }
}));

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
