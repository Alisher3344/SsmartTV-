import { Film } from 'lucide-react';
import ComingSoon from '../components/ComingSoon';

const Movies = () => (
  <div className="min-h-screen bg-dark text-white">
    <ComingSoon icon={Film} className="min-h-[70vh] pt-12 pb-16" />
  </div>
);

export default Movies;
