import { create } from 'zustand';
import apiClient from '../api/client';

export const useStore = create((set) => ({
  // Til sozlamalari
  language: localStorage.getItem('language') || 'uz',
  setLanguage: (lang) => {
    localStorage.setItem('language', lang);
    set({ language: lang });
  },

  // Foydalanuvchi ma'lumotlari
  user: null,
  authLoading: true,
  setUser: (user) => set({ user }),

  // Video player ochiqmi — ochiq paytda suzuvchi tugmalar (MastersFab) yashiriladi
  playerOpen: false,
  setPlayerOpen: (open) => set({ playerOpen: open }),

  // Joriy sessiyani backend'dan tekshirish (cookie orqali)
  fetchMe: async () => {
    try {
      const { data } = await apiClient.get('/api/auth/me');
      set({ user: data, authLoading: false });
    } catch {
      set({ user: null, authLoading: false });
    }
  },

  // Ro'yxatdan o'tish
  register: async (email, password, username) => {
    const { data } = await apiClient.post('/api/auth/register', {
      email,
      password,
      username,
    });
    set({ user: data });
    return data;
  },

  // Kirish (staff/admin/superuser — username + parol)
  login: async (username, password) => {
    const { data } = await apiClient.post('/api/auth/staff/login', { username, password });
    set({ user: data });
    return data;
  },

  // Chiqish
  logout: async () => {
    try {
      await apiClient.post('/api/auth/logout');
    } finally {
      set({ user: null });
    }
  },

  // Qidiruv
  searchQuery: '',
  setSearchQuery: (query) => set({ searchQuery: query }),

  // Mobil menyu
  isMobileMenuOpen: false,
  setMobileMenuOpen: (isOpen) => set({ isMobileMenuOpen: isOpen }),
}));
