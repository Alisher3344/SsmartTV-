import React from 'react';
import { useTranslation } from 'react-i18next';
import { Construction } from 'lucide-react';
import { useStore } from '../store/useStore';

const MASTERS_URL = 'https://pro.ssmart.uz';

// Suzuvchi "Ustalar" tugmasi — ekranning pastki-o'ng burchagida, har sahifada ko'rinadi.
// Headerni siqmaslik uchun navbar'dan shu yerga ko'chirilgan.
const MastersFab = () => {
  const { t } = useTranslation();
  const playerOpen = useStore((s) => s.playerOpen);

  // Video ko'rilayotganda (player ochiq) tugma xalaqit bermasligi uchun yashiriladi.
  if (playerOpen) return null;

  return (
    <a
      href={MASTERS_URL}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={t('nav.masters')}
      className="group fixed bottom-6 right-6 z-50 flex items-center gap-2 px-5 py-3 rounded-full bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 text-white font-bold text-sm shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 ring-2 ring-orange-300/50"
    >
      {/* Diqqatni tortuvchi yengil pulse halqasi */}
      <span className="absolute inset-0 rounded-full bg-orange-400/40 animate-ping -z-10" aria-hidden="true" />
      <Construction size={20} className="text-white" />
      <span>{t('nav.masters')}</span>
      <span className="absolute -top-1.5 -right-1.5 bg-yellow-300 text-orange-700 text-[10px] font-extrabold w-5 h-5 rounded-full leading-none shadow-sm flex items-center justify-center">
        ★
      </span>
    </a>
  );
};

export default MastersFab;
