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
      {/* Orqa fon nuri */}
      <div className="relative w-full max-w-lg">
        <div className="pointer-events-none absolute -inset-10 bg-radial-glow" aria-hidden="true" />

        <div className="glass-card relative rounded-2xl px-6 py-12 sm:px-12 sm:py-16 text-center">
          {/* Icon badge */}
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-br from-primary/30 to-primary/5 ring-1 ring-primary/30 animate-float">
            <Icon size={38} className="text-primary-light" strokeWidth={1.6} />
          </div>

          {/* Badge pill */}
          <span className="mb-4 inline-block rounded-full bg-primary/15 px-3 py-1 text-xs font-medium uppercase tracking-widest text-primary-light">
            {t('comingSoon.badge')}
          </span>

          {/* Title */}
          <h1 className="gradient-text text-2xl font-bold sm:text-3xl">
            {title || t('comingSoon.title')}
          </h1>

          {/* Subtitle */}
          <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-gray-400 sm:text-base">
            {subtitle || t('comingSoon.subtitle')}
          </p>

          {showBackButton && (
            <Link to="/" className="btn-primary mt-8 w-full sm:w-auto">
              {t('comingSoon.back')}
            </Link>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComingSoon;
