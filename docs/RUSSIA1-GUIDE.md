# 📺 РОССИЯ 1 Stream - Ishlash Yo'riqnomasi

## ⚠️ CORS Muammosi

URL: `https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8`

Bu stream CORS xavfsizligi tufayli brauzerda to'g'ridan-to'g'ri ishlamaydi.

---

## ✅ 3 TA ISHLAYDIGAN YECHIM:

### 🎯 YECHIM 1: VLC Media Player (ENG OSON)

**100% ISHLAYDI - CORS YO'Q**

1. **VLC yuklab oling:** https://www.videolan.org/vlc/
2. VLC'ni oching
3. **Media** → **Open Network Stream** (Ctrl+N)
4. URL kiriting:
   ```
   https://vgtrkregion-reg.cdnvideo.ru/vgtrk/0/russia1-hd/1080p.m3u8
   ```
5. **Play** → ВЕСТИ ko'rinadi! ✅

---

### 🎯 YECHIM 2: russia1-player.html (Brauzer)

**Oddiy HTML file**

1. Loyihada `russia1-player.html` faylini oching
2. Brauzerda oching (double-click)
3. Video avtomatik boshlanadi

⚠️ Agar CORS xatosi bo'lsa:
- Chrome Extensionlar: "CORS Unblock", "Allow CORS"
- Yoki Firefox ishlatib ko'ring
- Yoki VPN yoqing

---

### 🎯 YECHIM 3: Backend Proxy (Production)

**Web platforma uchun professional yechim**

#### Kerakli paketlar:
```bash
npm install express cors node-fetch
```

#### Ishga tushirish:

**Terminal 1 - Backend (port 3001):**
```bash
npm run proxy
```

**Terminal 2 - Frontend (port 5173):**
```bash
npm run dev
```

#### Frontend URL o'zgartiring:
```javascript
// /src/data/movies.js va /src/pages/TVChannels.jsx
videoUrl: 'http://localhost:3001/stream/russia1.m3u8'
```

---

## 🎬 NIMA KO'RASIZ:

✅ РОССИЯ 1 jonli efir
✅ ВЕСТИ dasturi  
✅ 1080p HD sifat
✅ To'liq ekran
✅ Player controls

---

## 🔧 TEXNIK TAFSILOTLAR:

### Stream ma'lumotlari:
- Format: HLS (HTTP Live Streaming)
- Extension: .m3u8
- Sifat: 1080p Full HD
- Codec: H.264 video, AAC audio

### CORS nima?
CORS = Cross-Origin Resource Sharing

Brauzer xavfsizlik mexanizmi:
- localhost:5173 → vgtrkregion-reg.cdnvideo.ru
- ❌ Blocked (turli domenlar)

Yechim:
1. VLC (CORS yo'q)
2. Browser extension (CORS o'chirish)
3. Backend proxy (CORS qo'shish)

---

## 📝 TAVSIYALAR:

### Tezkor test:
✅ **VLC** - 2 daqiqada ishlaydi

### Development:
✅ **russia1-player.html** + CORS extension

### Production:
✅ **Backend proxy** - eng xavfsiz

---

## 🆘 YORDAM:

Agar video ishlamasa:

1. **VLC'da sinab ko'ring** - bu 100% ishlaydi
2. CORS extension o'rnating
3. VPN yoqing
4. Boshqa brauzer sinang (Firefox, Edge)
5. Backend proxy ishlatib ko'ring

---

## 📞 QULLAB-QUVVATLASH:

Qo'shimcha yordam kerak bo'lsa:
- proxy-server.js faylini o'qing
- CORS-ISSUE.md faylini ko'ring
- russia1-player.html dan foydalaning

**VLC Media Player bilan ishlatish eng oson va ishonchli!** 🎬
