/**
 * AeroIndex / FareOS — Vercel Serverless Function Entrypoint
 * Powers real institutional REST API v1 queries on live deployed links
 * Accessible by Reserve Bank of India (RBI), National Statistical Office (NSO), and SIH 2026 Auditors
 */

const url = require('url');
const govApi = require('../services/web/api_v1_gov');

module.exports = (req, res) => {
  // Enable full CORS for external institutional consumers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-API-Key');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    return res.end();
  }

  const parsedUrl = url.parse(req.url, true);
  let pathname = parsedUrl.pathname || '/';

  // Normalize pathname if stripped by Vercel rewrite
  if (!pathname.startsWith('/api')) {
    pathname = '/api' + (pathname.startsWith('/') ? pathname : '/' + pathname);
  }

  if (pathname === '/api/docs') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    return res.end(govApi.getHtmlDocs());
  }

  if (govApi.isGovEndpoint(pathname)) {
    return govApi.handleGovApiRequest(req, res, pathname, parsedUrl.query);
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  return res.end(JSON.stringify({
    success: false,
    data: null,
    meta: {
      api_version: 'v1.0.0',
      as_of: new Date().toISOString(),
      data_status: 'NO_DATA',
      methodology_version: 'JEVONS-2026.1'
    },
    error: {
      code: 'ENDPOINT_NOT_FOUND',
      message: `The endpoint '${pathname}' does not exist in AeroIndex API v1.`
    }
  }, null, 2));
};
