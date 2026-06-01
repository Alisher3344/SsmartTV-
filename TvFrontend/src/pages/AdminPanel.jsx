import React, { useEffect, useState } from 'react';
import { useStore } from '../store/useStore';
import apiClient from '../api/client';
import imageToDataUrl from '../utils/imageToDataUrl';
import { LogOut, Pencil, Trash2, Plus, Loader2 } from 'lucide-react';

// Asosiy kategoriya = davlat
const COUNTRIES = ['ozbekiston', 'rossiya', 'belarus'];

// Sub kategoriya = janr (ixtiyoriy)
const GENRES = [
  '',
  'yangiliklar',
  'sport',
  'kino',
  'seriallar',
  'musiqiy',
  'bolalar',
  'hujjatli',
  'kongilochar',
  'talimiy',
  'madaniyat',
  'sayohat',
  'anime',
  'multfilm',
  'jonli',
  'oilaviy',
];

// Mirror of the backend slugify (app/import_m3u.py): lowercase, non-alphanumeric
// runs become "-", trimmed.
const slugify = (s) =>
  s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

const EMPTY_FORM = {
  name: '',
  slug: '',
  category: 'ozbekiston',
  subcategory: '',
  video_url: '',
  is_live: false,
  logo: '',
  current_show: '',
  time: '',
  description_uz: '',
  description_ru: '',
  sort_order: 0,
};

// ---- Login gate ----------------------------------------------------------
function LoginForm({ notAdmin }) {
  const { login, logout } = useStore();
  const [loginValue, setLoginValue] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setBusy(true);
    try {
      const user = await login(loginValue, password);
      if (!user?.is_admin) {
        setError("Bu hisobda admin huquqi yo'q.");
      }
    } catch {
      setError("Login yoki parol noto'g'ri.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4">
      <form
        onSubmit={submit}
        className="w-full max-w-sm bg-dark-card border border-gray-800 rounded-2xl p-8 space-y-5"
      >
        <h1 className="text-2xl font-bold text-center">Admin panel</h1>
        <p className="text-sm text-gray-400 text-center">
          Davom etish uchun tizimga kiring
        </p>

        {notAdmin && (
          <div className="text-sm bg-red-500/10 text-red-400 rounded-lg px-3 py-2">
            Siz tizimga kirdingiz, lekin admin huquqingiz yo'q.{' '}
            <button type="button" onClick={logout} className="underline">
              Chiqish
            </button>
          </div>
        )}

        <div>
          <label className="block text-sm text-gray-400 mb-1">Login</label>
          <input
            type="text"
            value={loginValue}
            onChange={(e) => setLoginValue(e.target.value)}
            autoFocus
            placeholder="admin123"
            className="w-full bg-dark border border-gray-700 rounded-lg px-3 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-primary"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Parol</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••"
            className="w-full bg-dark border border-gray-700 rounded-lg px-3 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-primary"
          />
        </div>

        {error && <div className="text-sm text-red-400">{error}</div>}

        <button
          type="submit"
          disabled={busy}
          className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-60"
        >
          {busy && <Loader2 size={18} className="animate-spin" />}
          Kirish
        </button>
      </form>
    </div>
  );
}

// ---- Channel add/edit form ----------------------------------------------
// Remounted via `key` whenever the edited channel changes, so initial state is
// derived from props with a lazy initializer (no syncing effect needed).
function ChannelForm({ editing, onDone, onCancel }) {
  const [form, setForm] = useState(() =>
    editing ? { ...EMPTY_FORM, ...editing } : EMPTY_FORM
  );
  const [slugTouched, setSlugTouched] = useState(() => !!editing);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  const onName = (value) => {
    setForm((f) => ({
      ...f,
      name: value,
      slug: slugTouched ? f.slug : slugify(value),
    }));
  };

  const onPickImage = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      const dataUrl = await imageToDataUrl(file);
      set('logo', dataUrl);
    } catch {
      setError("Rasmni o'qib bo'lmadi.");
    }
  };

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.name.trim() || !form.slug.trim()) {
      setError('Nom va slug majburiy.');
      return;
    }
    setBusy(true);
    // Store the same image in both `logo` (tiles) and `image` (detail views).
    const payload = {
      name: form.name,
      slug: form.slug,
      category: form.category,
      subcategory: form.subcategory || null,
      video_url: form.video_url || null,
      is_live: form.is_live,
      logo: form.logo || null,
      image: form.logo || null,
      current_show: form.current_show || null,
      time: form.time || null,
      description_uz: form.description_uz || null,
      description_ru: form.description_ru || null,
      sort_order: Number(form.sort_order) || 0,
    };
    try {
      if (editing) {
        await apiClient.put(`/api/channels/${editing.slug}`, payload);
      } else {
        await apiClient.post('/api/channels', payload);
      }
      onDone();
    } catch (err) {
      const status = err?.response?.status;
      if (status === 409) setError('Bu slug allaqachon mavjud.');
      else if (status === 401 || status === 403)
        setError('Ruxsat yo\'q (admin sessiyasi kerak).');
      else setError('Saqlashda xatolik yuz berdi.');
    } finally {
      setBusy(false);
    }
  };

  const field =
    'w-full bg-dark border border-gray-700 rounded-lg px-3 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-primary';

  return (
    <form
      onSubmit={submit}
      className="bg-dark-card border border-gray-800 rounded-2xl p-6 space-y-4"
    >
      <h2 className="text-lg font-semibold flex items-center gap-2">
        {editing ? <Pencil size={18} /> : <Plus size={18} />}
        {editing ? `Tahrirlash: ${editing.name}` : 'Yangi kanal qo\'shish'}
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-gray-400 mb-1">Nom *</label>
          <input
            className={field}
            value={form.name}
            onChange={(e) => onName(e.target.value)}
            placeholder="Bolajon"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Slug *</label>
          <input
            className={field}
            value={form.slug}
            disabled={!!editing}
            onChange={(e) => {
              setSlugTouched(true);
              set('slug', slugify(e.target.value));
            }}
            placeholder="bolajon"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Davlat (kategoriya)
          </label>
          <select
            className={field}
            value={form.category}
            onChange={(e) => set('category', e.target.value)}
          >
            {COUNTRIES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Janr (sub-kategoriya)
          </label>
          <select
            className={field}
            value={form.subcategory}
            onChange={(e) => set('subcategory', e.target.value)}
          >
            {GENRES.map((g) => (
              <option key={g} value={g}>
                {g === '' ? '— yo\'q —' : g}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Stream URL (m3u8)
          </label>
          <input
            className={field}
            value={form.video_url}
            onChange={(e) => set('video_url', e.target.value)}
            placeholder="https://.../playlist.m3u8"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Hozir efirda
          </label>
          <input
            className={field}
            value={form.current_show}
            onChange={(e) => set('current_show', e.target.value)}
            placeholder="Multfilm"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Vaqt</label>
          <input
            className={field}
            value={form.time}
            onChange={(e) => set('time', e.target.value)}
            placeholder="18:00 - 19:00"
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Tavsif (UZ)
          </label>
          <input
            className={field}
            value={form.description_uz}
            onChange={(e) => set('description_uz', e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Tavsif (RU)
          </label>
          <input
            className={field}
            value={form.description_ru}
            onChange={(e) => set('description_ru', e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm text-gray-400 mb-1">Tartib raqami</label>
          <input
            type="number"
            className={field}
            value={form.sort_order}
            onChange={(e) => set('sort_order', e.target.value)}
          />
        </div>
        <label className="flex items-center gap-2 mt-7 text-sm text-gray-300">
          <input
            type="checkbox"
            checked={form.is_live}
            onChange={(e) => set('is_live', e.target.checked)}
            className="w-4 h-4 accent-primary"
          />
          Jonli efir (is_live)
        </label>
      </div>

      <div>
        <label className="block text-sm text-gray-400 mb-1">Kanal rasmi</label>
        <div className="flex items-center gap-4">
          <input
            type="file"
            accept="image/*"
            onChange={onPickImage}
            className="text-sm text-gray-400 file:mr-3 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-primary file:text-black file:cursor-pointer"
          />
          {form.logo && (
            <img
              src={form.logo}
              alt="preview"
              className="h-14 w-14 object-contain rounded-lg bg-dark border border-gray-700"
            />
          )}
        </div>
      </div>

      {error && <div className="text-sm text-red-400">{error}</div>}

      <div className="flex items-center gap-3">
        <button
          type="submit"
          disabled={busy}
          className="btn-primary flex items-center gap-2 disabled:opacity-60"
        >
          {busy && <Loader2 size={18} className="animate-spin" />}
          {editing ? 'Saqlash' : "Qo'shish"}
        </button>
        {editing && (
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 rounded-lg bg-dark border border-gray-700 text-gray-300 hover:bg-gray-800"
          >
            Bekor qilish
          </button>
        )}
      </div>
    </form>
  );
}

// ---- Dashboard -----------------------------------------------------------
function Dashboard() {
  const { user, logout } = useStore();
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(null);

  // Reload helper used by event handlers (after create/edit/delete).
  const load = async () => {
    try {
      const { data } = await apiClient.get('/api/channels');
      setChannels(data);
    } catch {
      setChannels([]);
    }
  };

  // Initial fetch on mount — state is only set in the async callbacks.
  useEffect(() => {
    let active = true;
    apiClient
      .get('/api/channels')
      .then(({ data }) => active && setChannels(data))
      .catch(() => active && setChannels([]))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  const onDone = () => {
    setEditing(null);
    load();
  };

  const onDelete = async (channel) => {
    if (!window.confirm(`"${channel.name}" kanalini o'chirilsinmi?`)) return;
    try {
      await apiClient.delete(`/api/channels/${channel.slug}`);
      load();
    } catch {
      window.alert("O'chirishda xatolik yuz berdi.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Admin panel</h1>
          <p className="text-sm text-gray-400">
            {user?.username || user?.email} · kanallarni boshqarish
          </p>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-2 bg-dark-card px-3 py-2 rounded-lg hover:bg-gray-800 transition-colors text-sm"
        >
          <LogOut size={16} />
          Chiqish
        </button>
      </div>

      <ChannelForm
        key={editing?.slug || 'new'}
        editing={editing}
        onDone={onDone}
        onCancel={() => setEditing(null)}
      />

      <div className="bg-dark-card border border-gray-800 rounded-2xl overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between">
          <h2 className="font-semibold">Kanallar ({channels.length})</h2>
        </div>
        {loading ? (
          <div className="p-10 flex justify-center">
            <Loader2 className="animate-spin text-gray-500" />
          </div>
        ) : (
          <div className="divide-y divide-gray-800">
            {channels.map((c) => (
              <div
                key={c.id}
                className="flex items-center gap-4 px-6 py-3 hover:bg-dark/40"
              >
                <img
                  src={c.logo || '/logo.png'}
                  alt={c.name}
                  className="h-10 w-10 object-contain rounded bg-dark border border-gray-700 flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <div className="font-medium truncate">{c.name}</div>
                  <div className="text-xs text-gray-500 truncate">
                    {c.slug} · {c.category}
                    {c.subcategory ? ` / ${c.subcategory}` : ''}
                  </div>
                </div>
                {c.is_live && (
                  <span className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full">
                    LIVE
                  </span>
                )}
                <button
                  onClick={() => {
                    setEditing(c);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                  className="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800"
                  title="Tahrirlash"
                >
                  <Pencil size={16} />
                </button>
                <button
                  onClick={() => onDelete(c)}
                  className="p-2 rounded-lg text-gray-400 hover:text-red-400 hover:bg-gray-800"
                  title="O'chirish"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
            {channels.length === 0 && (
              <div className="p-10 text-center text-gray-500">
                Kanallar yo'q
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ---- Entry ---------------------------------------------------------------
export default function AdminPanel() {
  const { user, authLoading } = useStore();

  if (authLoading) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center">
        <Loader2 className="animate-spin text-gray-500" size={28} />
      </div>
    );
  }

  if (!user) return <LoginForm />;
  if (!user.is_admin) return <LoginForm notAdmin />;
  return <Dashboard />;
}
