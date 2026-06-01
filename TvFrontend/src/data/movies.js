export const moviesData = {
  hero: {
    id: 1,
    title: {
      uz: "SHERIKLAR III",
      ru: "ШЕРИКLAR III"
    },
    description: {
      uz: "Komediya, 2026, 12+, Qyrgyzstan",
      ru: "Комедия, 2026, 12+, Кыргызстан"
    },
    rating: {
      imdb: 8.8,
      kinopoisk: 8.8,
      ntv: 8.8
    },
    image: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1200&h=600&fit=crop",
  },
  
  featured: {
    id: 2,
    title: {
      uz: "Turnir",
      ru: "Турнир"
    },
    description: {
      uz: "Fasl 1, Seriya 1",
      ru: "Сезон 1, Серия 1"
    },
    image: "https://images.unsplash.com/photo-1574267432644-f610a4e1dd6e?w=300&h=400&fit=crop",
  },
  
  channels: [
    { id: 1, name: "7 HD", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23333'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='20' fill='white' text-anchor='middle'%3E7 HD%3C/text%3E%3C/svg%3E" },
    { id: 2, name: "КИНО ЯНГИ", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23555'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='16' fill='white' text-anchor='middle'%3EКИНО%3C/text%3E%3C/svg%3E" },
    { id: 3, name: "КИНОХИТ", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23666'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='16' fill='white' text-anchor='middle'%3EХИТ%3C/text%3E%3C/svg%3E" },
    { id: 4, name: "ИНДИЙСКОЕ КИНО", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23777'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='14' fill='white' text-anchor='middle'%3EИНДИЯ%3C/text%3E%3C/svg%3E" },
    {
      id: 5,
      name: "РОССИЯ 1",
      logo: "/russia1-logo.svg"
    },
    { id: 6, name: "НОВОЕ КИНО", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23888'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='14' fill='white' text-anchor='middle'%3EНОВОЕ%3C/text%3E%3C/svg%3E" },
    { id: 7, name: "КИНОСЕРИЯ", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23999'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='14' fill='white' text-anchor='middle'%3EСЕРИЯ%3C/text%3E%3C/svg%3E" },
    { id: 8, name: "КИНОУЖАС", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23aaa'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='16' fill='white' text-anchor='middle'%3EУЖАС%3C/text%3E%3C/svg%3E" },
    { id: 9, name: "КИНОХИТ", logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='80'%3E%3Crect width='120' height='80' fill='%23bbb'/%3E%3Ctext x='60' y='45' font-family='Arial' font-size='16' fill='white' text-anchor='middle'%3EХИТ%3C/text%3E%3C/svg%3E" },
  ],
  
  cinemas: [
    { 
      id: 1, 
      name: "viju",
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%2300d9c0'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='28' font-weight='bold' fill='white' text-anchor='middle'%3Eviju%3C/text%3E%3C/svg%3E",
      color: "#00d9c0"
    },
    { 
      id: 2, 
      name: "PREMIER", 
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%23ffd700'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='24' font-weight='bold' fill='black' text-anchor='middle'%3EPREMIER%3C/text%3E%3C/svg%3E",
      color: "#ffd700"
    },
    { 
      id: 3, 
      name: "Disney+", 
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%230063e5'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='28' font-weight='bold' fill='white' text-anchor='middle'%3EDisney+%3C/text%3E%3C/svg%3E",
      color: "#0063e5"
    },
    { 
      id: 4, 
      name: "SSMART TV", 
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%23710087'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='22' font-weight='bold' fill='white' text-anchor='middle'%3ESSMART TV%3C/text%3E%3C/svg%3E",
      color: "#710087"
    },
    { 
      id: 5, 
      name: "salom.tv", 
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%230080ff'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='24' font-weight='bold' fill='white' text-anchor='middle'%3Esalom.tv%3C/text%3E%3C/svg%3E",
      color: "#0080ff"
    },
    { 
      id: 6, 
      name: "Paramount+", 
      logo: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='120'%3E%3Crect width='200' height='120' fill='%230063e5'/%3E%3Ctext x='100' y='70' font-family='Arial' font-size='22' font-weight='bold' fill='white' text-anchor='middle'%3EParamount+%3C/text%3E%3C/svg%3E",
      color: "#0063e5"
    },
  ],
  
  premieres: [
    {
      id: 1,
      title: {
        uz: "34 yillik o'rzu",
        ru: "34-летняя мечта"
      },
      genre: {
        uz: "Badiiy",
        ru: "Художественный"
      },
      image: "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=300&h=450&fit=crop",
    },
    {
      id: 2,
      title: {
        uz: "Jannat 2: Onamga maktub",
        ru: "Джаннат 2: Письмо маме"
      },
      genre: {
        uz: "Oilaga",
        ru: "Для семьи"
      },
      age: "12+",
      image: "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=300&h=450&fit=crop",
    },
    {
      id: 3,
      title: {
        uz: "KRIK 7",
        ru: "КРИК 7"
      },
      genre: {
        uz: "Qo'rqinchli",
        ru: "Ужасы"
      },
      age: "18+",
      image: "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=300&h=450&fit=crop",
    },
    {
      id: 4,
      title: {
        uz: "Salom Yevropa!",
        ru: "Привет Европа!"
      },
      genre: {
        uz: "Oilaga",
        ru: "Для семьи"
      },
      image: "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&h=450&fit=crop",
    },
    {
      id: 5,
      title: {
        uz: "Priguny",
        ru: "Прыгуны"
      },
      genre: {
        uz: "Subtitrlash",
        ru: "Субтитры"
      },
      image: "https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=300&h=450&fit=crop",
    },
    {
      id: 6,
      title: {
        uz: "Sheriklar 3",
        ru: "Шерикlar 3"
      },
      genre: {
        uz: "Oilaga",
        ru: "Для семьи"
      },
      image: "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300&h=450&fit=crop",
    },
  ],
  
  uzbekSeries: [
    {
      id: 1,
      title: "Ko'proq ko'rsatish",
      isButton: true,
    }
  ]
};
