# CORS Muammosi va Yechimlar

## ⚠️ Muammo

Russia 1 HD stream URL'i CORS (Cross-Origin Resource Sharing) xatosini beradi:

```
Access to fetch at 'https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8'
from origin 'http://localhost:5173' has been blocked by CORS policy
```

## 🔧 Yechimlar

### 1. Backend Proxy (Tavsiya etiladi)

Backend server orqali stream'ni proxy qilish:

```javascript
// Node.js Express misol
app.get('/proxy/russia1', (req, res) => {
  const streamUrl = 'https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8';
  
  // CORS headerlarini qo'shish
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET');
  
  // Stream'ni proxy qilish
  fetch(streamUrl)
    .then(response => response.body.pipe(res))
    .catch(err => res.status(500).send(err));
});
```

Keyin frontend'da:

```javascript
videoUrl: '/proxy/russia1'
```

### 2. CORS Proxy Service

Vaqtinchalik test uchun CORS proxy ishlatish:

```javascript
videoUrl: 'https://cors-anywhere.herokuapp.com/https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8'
```

⚠️ **Eslatma:** Production uchun ishlatmang!

### 3. Server tomonda CORS sozlash

Agar stream serveriga kirishingiz bo'lsa, quyidagi headerlarni qo'shing:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### 4. Chrome Extension (Faqat development uchun)

Development paytida CORS'ni o'chirish uchun:

1. "CORS Unblock" extension o'rnating
2. Extension'ni yoqing
3. Sahifani yangilang

⚠️ **Eslatma:** Faqat development uchun!

## 📺 Test Stream

Hozirda test uchun Mux.dev ochiq stream ishlatilmoqda:

```
https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8
```

Bu stream CORS muammosiz ishlaydi va video player'ni test qilish uchun juda yaxshi.

## 🚀 Production uchun

Production'da:

1. **Backend proxy** (eng yaxshi yechim)
2. **CDN proxy** (Cloudflare, AWS CloudFront)
3. **Stream provider bilan CORS sozlash**

## 💡 Qo'shimcha Ma'lumot

CORS - bu brauzer xavfsizlik mexanizmi. U bir domaindan (localhost:5173) boshqa domainga (vgtrkregion-reg.cdnvideo.ru) so'rov yuborishni cheklaydi.

Yechim: Server tomonida ruxsat berish yoki proxy server ishlatish.
