import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Clapperboard } from 'lucide-react';

/**
 * Qayta ishlatiluvchi "Tez kunda" / "Скоро" holati.
 * - To'liq sahifa uchun: <ComingSoon icon={Film} /> (default markazlashgan, min-h-[60vh])
 * - Bo'lim ichida: <ComingSoon className="py-12" showBackButton={false} />
 */
const ComingSoon = ({
  title,
  subtitle,
  icon: Icon = Clapperboard,
  showBackButton = true,
  className = 'min-h-[60vh]',
}) => {
  const { t } = useTranslation();

  return (
    <div className={`flex items-center justify-center px-4 ${className}`}>
      <div className="w-full max-w-xl text-center">
        {/* Nozik ikonka — fonsiz, float yo'q */}
        <Icon
          size={30}
          strokeWidth={1.25}
          className="mx-auto mb-5 text-gold/60 reveal reveal-1"
          aria-hidden="true"
        />

        {/* Eyebrow */}
        <p className="eyebrow justify-center reveal reveal-1">{t('comingSoon.badge')}</p>

        {/* Title — yirik serif */}
        <h1 className="font-display text-fluid-display font-semibold gradient-text reveal reveal-2">
          {title || t('comingSoon.title')}
        </h1>

        {/* Oltin chiziq divider */}
        <div className="mx-auto my-6 h-px w-16 bg-gold/50 reveal reveal-2" />

        {/* Subtitle */}
        <p className="mx-auto max-w-md text-sm leading-relaxed text-white/55 sm:text-base reveal reveal-3">
          {subtitle || t('comingSoon.subtitle')}
        </p>

        {showBackButton && (
          <Link to="/" className="btn-outline mt-8 reveal reveal-4">
            {t('comingSoon.back')}
          </Link>
        )}
      </div>
    </div>
  );
};

export default ComingSoon;
