// DataCoin Service Worker
// Enables offline functionality and background operations

const CACHE_NAME = 'datacoin-v1.0.0';
const API_CACHE_NAME = 'datacoin-api-v1.0.0';

// Files to cache for offline use
const STATIC_CACHE_URLS = [
  '/',
  '/frontend/index.html',
  '/pwa/manifest.json',
  '/icons/datacoin-192x192.png',
  '/icons/datacoin-512x512.png'
];

// API endpoints to cache
const API_CACHE_URLS = [
  '/system/health',
  '/blockchain/stats',
  '/wallets',
  '/data/stats',
  '/corporate/shares'
];

// Install event - cache static resources
self.addEventListener('install', event => {
  console.log('🪙 DataCoin Service Worker installing...');
  
  event.waitUntil(
    Promise.all([
      // Cache static files
      caches.open(CACHE_NAME).then(cache => {
        console.log('📦 Caching static files...');
        return cache.addAll(STATIC_CACHE_URLS);
      }),
      
      // Cache API responses
      caches.open(API_CACHE_NAME).then(cache => {
        console.log('🔄 Pre-caching API responses...');
        return Promise.all(
          API_CACHE_URLS.map(url => 
            fetch(url).then(response => {
              if (response.ok) {
                return cache.put(url, response.clone());
              }
            }).catch(() => {
              // Ignore errors during pre-caching
              console.log(`⚠️ Could not pre-cache ${url}`);
            })
          )
        );
      })
    ]).then(() => {
      console.log('✅ DataCoin Service Worker installed successfully');
      // Take control immediately
      return self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('🔄 DataCoin Service Worker activating...');
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
            console.log('🗑️ Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ DataCoin Service Worker activated');
      // Take control of all clients
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle API requests
  if (url.pathname.startsWith('/api') || 
      url.pathname.startsWith('/wallets') || 
      url.pathname.startsWith('/blockchain') ||
      url.pathname.startsWith('/data') ||
      url.pathname.startsWith('/mining') ||
      url.pathname.startsWith('/corporate') ||
      url.pathname.startsWith('/system')) {
    
    event.respondWith(handleApiRequest(request));
  }
  // Handle static file requests
  else {
    event.respondWith(handleStaticRequest(request));
  }
});

// Handle API requests with cache-first strategy for reads, network-first for writes
async function handleApiRequest(request) {
  const isReadRequest = request.method === 'GET';
  
  if (isReadRequest) {
    // Cache-first for GET requests
    try {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        // Update cache in background
        updateCacheInBackground(request);
        return cachedResponse;
      }
      
      // Not in cache, try network
      const networkResponse = await fetch(request);
      if (networkResponse.ok) {
        const cache = await caches.open(API_CACHE_NAME);
        cache.put(request, networkResponse.clone());
      }
      return networkResponse;
      
    } catch (error) {
      console.log('🔴 API request failed, using cache:', request.url);
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        return cachedResponse;
      }
      
      // Return offline response
      return new Response(JSON.stringify({
        error: 'Offline',
        message: 'This request requires an internet connection'
      }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } else {
    // Network-first for POST/PUT/DELETE requests
    try {
      const networkResponse = await fetch(request);
      
      // If successful, invalidate related cache entries
      if (networkResponse.ok) {
        await invalidateRelatedCache(request.url);
      }
      
      return networkResponse;
    } catch (error) {
      // Queue the request for later when online
      await queueRequest(request);
      
      return new Response(JSON.stringify({
        success: false,
        message: 'Request queued for when connection is restored'
      }), {
        status: 202,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }
}

// Handle static file requests with cache-first strategy
async function handleStaticRequest(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
    
  } catch (error) {
    console.log('🔴 Static request failed:', request.url);
    
    // Return offline page for HTML requests
    if (request.destination === 'document') {
      const cache = await caches.open(CACHE_NAME);
      return cache.match('/frontend/index.html');
    }
    
    throw error;
  }
}

// Update cache in background
async function updateCacheInBackground(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(API_CACHE_NAME);
      await cache.put(request, networkResponse.clone());
    }
  } catch (error) {
    // Silent fail for background updates
  }
}

// Invalidate related cache entries
async function invalidateRelatedCache(url) {
  const cache = await caches.open(API_CACHE_NAME);
  const keys = await cache.keys();
  
  // Remove related cache entries
  const relatedKeys = keys.filter(request => {
    const requestUrl = new URL(request.url);
    return requestUrl.pathname.includes(new URL(url).pathname.split('/')[1]);
  });
  
  await Promise.all(relatedKeys.map(key => cache.delete(key)));
}

// Queue requests for background sync
async function queueRequest(request) {
  // Store request in IndexedDB for background sync
  // This would be implemented with IndexedDB in a full implementation
  console.log('📝 Queuing request for background sync:', request.url);
}

// Background sync event
self.addEventListener('sync', event => {
  console.log('🔄 Background sync triggered:', event.tag);
  
  if (event.tag === 'datacoin-sync') {
    event.waitUntil(syncQueuedRequests());
  }
});

// Sync queued requests when back online
async function syncQueuedRequests() {
  console.log('📡 Syncing queued requests...');
  // Implementation would retrieve queued requests from IndexedDB
  // and replay them when back online
}

// Push notification event
self.addEventListener('push', event => {
  console.log('📱 Push notification received');
  
  const options = {
    body: 'DataCoin notification',
    icon: '/icons/datacoin-192x192.png',
    badge: '/icons/datacoin-96x96.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'open',
        title: 'Open DataCoin',
        icon: '/icons/datacoin-96x96.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/icons/close-icon.png'
      }
    ]
  };
  
  if (event.data) {
    const data = event.data.json();
    options.body = data.message || options.body;
    options.title = data.title || 'DataCoin';
  }
  
  event.waitUntil(
    self.registration.showNotification('DataCoin', options)
  );
});

// Notification click event
self.addEventListener('notificationclick', event => {
  console.log('📱 Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message event - communication with main thread
self.addEventListener('message', event => {
  console.log('💬 Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_UPDATE') {
    event.waitUntil(updateCacheInBackground(new Request(event.data.url)));
  }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', event => {
  console.log('⏰ Periodic sync triggered:', event.tag);
  
  if (event.tag === 'datacoin-mining-check') {
    event.waitUntil(checkMiningStatus());
  }
});

// Check mining status in background
async function checkMiningStatus() {
  try {
    const response = await fetch('/mining/status');
    if (response.ok) {
      const status = await response.json();
      
      // Send notification if mining completed
      if (status.lastBlockMined) {
        self.registration.showNotification('DataCoin Mining Complete!', {
          body: `Block ${status.lastBlockMined} has been mined successfully!`,
          icon: '/icons/datacoin-192x192.png',
          tag: 'mining-complete'
        });
      }
    }
  } catch (error) {
    console.log('⚠️ Failed to check mining status:', error);
  }
}

console.log('🪙 DataCoin Service Worker loaded successfully');