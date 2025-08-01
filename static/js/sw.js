// Empty Service Worker file to prevent 404 errors
// This file exists only to resolve browser cache issues

console.log('Service Worker loaded (empty implementation)');

// Basic service worker that does nothing
self.addEventListener('install', function(event) {
    console.log('Service Worker installing');
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activating');
    event.waitUntil(self.clients.claim());
});