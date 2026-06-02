import { Clapperboard } from 'lucide-react';
import ComingSoon from '../components/ComingSoon';

const MovieDetail = () => (
  <div className="min-h-screen bg-dark text-white">
    <ComingSoon icon={Clapperboard} className="min-h-[70vh] pt-12 pb-16" />
  </div>
);

export default MovieDetail;
