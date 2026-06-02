/** Asosiy shimmer skeleton bloki. */
export const Skeleton = ({ className = '' }) => (
  <div className={`skeleton rounded-lg ${className}`} />
);

/** Poster (2:3) skeleton — kino/serial kartalari uchun. */
export const PosterSkeleton = ({ className = '' }) => (
  <Skeleton className={`aspect-[2/3] w-full ${className}`} />
);

/** Gorizontal qator skeleton — karusellar yuklanayotganda. */
export const RowSkeleton = ({ count = 8, itemClassName = 'w-32 h-20 flex-shrink-0' }) => (
  <div className="flex gap-4 overflow-hidden">
    {Array.from({ length: count }).map((_, i) => (
      <Skeleton key={i} className={itemClassName} />
    ))}
  </div>
);

export default Skeleton;
