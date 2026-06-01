# 🚀 PRODUCTION DEPLOYMENT GUIDE

SSMART TV platformasini production serverga deploy qilish uchun to'liq qo'llanma.

---

## 📋 TALABLAR

### Backend Server:
- Node.js 16+ (18+ tavsiya etiladi)
- 1GB+ RAM
- Ubuntu/CentOS/Debian Linux
- Domen nomi (masalan: api.ssmarttv.uz)
- SSL sertifikat (Let's Encrypt bepul)

### Frontend Hosting:
- Static hosting (Vercel, Netlify, Cloudflare Pages)
- Yoki Nginx/Apache server
- HTTPS (majburiy)

---

## 🔧 BACKEND DEPLOYMENT (Node.js Server)

### 1. VPS/Cloud Server olish

**Tavsiya etiladigan provayderlar:**
- DigitalOcean (Droplet - $6/month)
- AWS EC2 (t2.micro - Free tier)
- Linode ($5/month)
- Hetzner (€4/month)
- Uzb: UZINFOCOM, Xost.uz

### 2. Serverga ulanish

```bash
ssh root@your-server-ip
```

### 3. Node.js o'rnatish

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Tekshirish
node --version  # v18.x.x
npm --version   # 9.x.x
```

### 4. Proxy server'ni deploy qilish

```bash
# Loyihani serverga yuklash
git clone https://github.com/your-username/ssmart-tv.git
cd ssmart-tv

# Dependencies o'rnatish
npm install --production

# PM2 process manager o'rnatish
npm install -g pm2

# Server'ni ishga tushirish
pm2 start proxy-server.cjs --name ssmart-proxy

# Auto-restart (server qayta yuklanganda)
pm2 startup
pm2 save

# Logs ko'rish
pm2 logs ssmart-proxy
```

### 5. Nginx reverse proxy sozlash

```bash
# Nginx o'rnatish
sudo apt install nginx

# Config yaratish
sudo nano /etc/nginx/sites-available/ssmart-api
```

```nginx
server {
    listen 80;
    server_name api.ssmarttv.uz;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Config'ni yoqish
sudo ln -s /etc/nginx/sites-available/ssmart-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL (HTTPS) sozlash

```bash
# Certbot o'rnatish
sudo apt install certbot python3-certbot-nginx

# SSL sertifikat olish
sudo certbot --nginx -d api.ssmarttv.uz

# Auto-renew
sudo certbot renew --dry-run
```

Endi backend tayyor: `https://api.ssmarttv.uz`

---

## 🌐 FRONTEND DEPLOYMENT

### VARIANT 1: Vercel (Tavsiya, bepul)

```bash
# Vercel CLI o'rnatish
npm install -g vercel

# Loyihani build qilish
npm run build

# Deploy
cd dist
vercel --prod
```

Vercel sizga domen beradi: `https://ssmart-tv.vercel.app`

### VARIANT 2: Netlify

```bash
# Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy --prod --dir=dist
```

### VARIANT 3: O'z serveringizda (Nginx)

```bash
# Frontend'ni build qilish (local kompyuterda)
npm run build

# dist/ papkani serverga yuklash
scp -r dist/* root@your-server:/var/www/ssmarttv

# Nginx config
sudo nano /etc/nginx/sites-available/ssmarttv
```

```nginx
server {
    listen 80;
    server_name ssmarttv.uz www.ssmarttv.uz;
    root /var/www/ssmarttv;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/ssmarttv /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL
sudo certbot --nginx -d ssmarttv.uz -d www.ssmarttv.uz
```

---

## 🔗 URL'LARNI YANGILASH

### Frontend kodida (production URL'lar):

**1. movies.js:**
```javascript
// /src/data/movies.js
{
  id: 5,
  name: "РОССИЯ 1",
  logo: "/russia1-logo.svg",
  videoUrl: "https://api.ssmarttv.uz/api/stream/russia1"
}
```

**2. TVChannels.jsx:**
```javascript
// /src/pages/TVChannels.jsx
{
  id: 1,
  name: 'Россия 1',
  videoUrl: 'https://api.ssmarttv.uz/api/stream/russia1'
},
{
  id: 2,
  name: 'Россия 24',
  videoUrl: 'https://api.ssmarttv.uz/api/stream/russia24'
}
```

**3. Environment variables (tavsiya):**

`.env.production` yarating:
```
VITE_API_URL=https://api.ssmarttv.uz
```

Kodda:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';
videoUrl: `${API_URL}/api/stream/russia1`
```

---

## 🔒 XAVFSIZLIK

### 1. Firewall sozlash

```bash
# UFW yoqish
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. Rate limiting (DDoS himoya)

Nginx config'ga qo'shing:
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    ...
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://localhost:3001;
    }
}
```

### 3. Environment variables

```bash
# .env fayl yarating
nano .env
```

```
NODE_ENV=production
PORT=3001
ALLOWED_ORIGINS=https://ssmarttv.uz,https://www.ssmarttv.uz
```

proxy-server.cjs'da:
```javascript
require('dotenv').config();

const allowedOrigins = process.env.ALLOWED_ORIGINS.split(',');

app.use(cors({
  origin: function(origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));
```

---

## 📊 MONITORING

### 1. PM2 monitoring

```bash
pm2 monit
pm2 status
pm2 logs ssmart-proxy --lines 100
```

### 2. Nginx logs

```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 3. Disk space

```bash
df -h
du -sh /var/www/ssmarttv
```

---

## 🔄 UPDATE QILISH

### Backend yangilash:

```bash
cd ssmart-tv
git pull
npm install --production
pm2 restart ssmart-proxy
```

### Frontend yangilash:

```bash
# Local kompyuterda
npm run build

# Serverga yuklash
scp -r dist/* root@your-server:/var/www/ssmarttv
```

---

## 🆘 TROUBLESHOOTING

### Problem: Proxy server ishlamayapti
```bash
pm2 logs ssmart-proxy
pm2 restart ssmart-proxy
```

### Problem: CORS xatosi
- Nginx config'ni tekshiring
- ALLOWED_ORIGINS to'g'riligini tasdiqlang
- Browser cache'ni tozalang

### Problem: SSL muammosi
```bash
sudo certbot renew
sudo systemctl restart nginx
```

### Problem: Video yuklanmayapti
- PM2 logs tekshiring: `pm2 logs`
- Stream URL ishlayotganini tasdiqlang
- Network connectivity tekshiring

---

## 💰 NARXLAR (Taxminiy)

**Minimal setup:**
- DigitalOcean Droplet: $6/month
- Domen (.uz): $10/year
- SSL: $0 (Let's Encrypt)
- Frontend: $0 (Vercel/Netlify)
**JAMI: ~$7/month**

**Professional setup:**
- AWS EC2 t3.medium: $30/month
- CloudFront CDN: $20/month
- Route53: $1/month
- S3 Storage: $2/month
**JAMI: ~$53/month**

---

## ✅ CHECKLIST

Backend:
- [ ] VPS/Cloud server
- [ ] Node.js o'rnatilgan
- [ ] proxy-server.cjs deploy qilindi
- [ ] PM2 sozlandi
- [ ] Nginx reverse proxy
- [ ] SSL sertifikat
- [ ] Firewall sozlandi
- [ ] Monitoring setup

Frontend:
- [ ] Build muvaffaqiyatli
- [ ] Hosting tanlandi
- [ ] Deploy qilindi
- [ ] SSL (HTTPS)
- [ ] URL'lar yangilandi
- [ ] CORS to'g'ri ishlayapti

Test:
- [ ] https://api.ssmarttv.uz/health → OK
- [ ] https://ssmarttv.uz ochiladi
- [ ] РОССИЯ 1 stream ishlaydi
- [ ] РОССИЯ 24 stream ishlaydi
- [ ] Mobile'da ishlaydi

---

**Production tayyor! 🚀**

Qo'shimcha yordam: support@ssmarttv.uz
