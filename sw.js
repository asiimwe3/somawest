const CACHE='somawest-v3';
const ASSETS=['./','./index.html','./manifest.json','./favicon.png',
'./icons/icon-192.png','./icons/icon-512.png','./icons/apple-touch-icon.png',
'./images/hero_band.jpg?v=1','./images/class1.jpg?v=1','./images/class2.jpg?v=1','./images/class3.jpg?v=1','./images/class4.jpg?v=1',
'./images/field1.jpg?v=1','./images/group1.jpg?v=1','./images/group2.jpg?v=1','./images/group3.jpg?v=1',
'./images/lab1.jpg?v=1','./images/lab2.jpg?v=1','./images/lab3.jpg?v=1','./images/lab4.jpg?v=1'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.indexOf('somawest')!==0).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request).then(h=>h||caches.match('./'))))});
