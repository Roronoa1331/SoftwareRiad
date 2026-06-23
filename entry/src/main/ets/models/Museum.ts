// Museum data model for Chinese Museums app

export interface Museum {
  id: string;
  name: string;
  location: string;
  city: string;
  description: string;
  establishedYear: number;
  visitorCount: number; // Annual visitors in millions
  highlights: string[];
  openingHours: string;
  admissionFee: string;
  imageUrl: string;
  rating: number; // 1-5 stars
  category: MuseumCategory;
  website?: string;
  latitude?: number;
  longitude?: number;
}

export enum MuseumCategory {
  HISTORY = 'History',
  ART = 'Art',
  SCIENCE = 'Science',
  ARCHAEOLOGY = 'Archaeology',
  ETHNOGRAPHY = 'Ethnography',
  NATURAL_HISTORY = 'Natural History',
  SPECIALIZED = 'Specialized'
}

// Sample museum data for Chinese museums
export const museums: Museum[] = [
  {
    id: '1',
    name: 'National Museum of China',
    location: 'Tiananmen Square East',
    city: 'Beijing',
    description: 'The National Museum of China is one of the largest museums in the world, with a collection of over 1.4 million items. It showcases Chinese history from prehistoric times to modern era.',
    establishedYear: 2003,
    visitorCount: 8.6,
    highlights: ['Ancient Chinese bronzes', 'Porcelain collection', 'Historical documents', 'Revolutionary artifacts'],
    openingHours: '9:00 AM - 5:00 PM (Closed Mondays)',
    admissionFee: 'Free (reservation required)',
    imageUrl: 'common/images/national_museum.jpg',
    rating: 4.8,
    category: MuseumCategory.HISTORY,
    website: 'https://en.chnmuseum.cn',
    latitude: 39.9042,
    longitude: 116.4074
  },
  {
    id: '2',
    name: 'Palace Museum (Forbidden City)',
    location: '4 Jingshan Front St',
    city: 'Beijing',
    description: 'The Palace Museum, also known as the Forbidden City, was the Chinese imperial palace from the Ming to Qing dynasties. It houses over 1.8 million cultural relics.',
    establishedYear: 1925,
    visitorCount: 19.0,
    highlights: ['Imperial architecture', 'Ancient ceramics', 'Paintings and calligraphy', 'Jade collection'],
    openingHours: '8:30 AM - 5:00 PM (Apr-Oct), 8:30 AM - 4:30 PM (Nov-Mar)',
    admissionFee: 'CNY 60 (Apr-Oct), CNY 40 (Nov-Mar)',
    imageUrl: 'common/images/palace_museum.jpg',
    rating: 4.9,
    category: MuseumCategory.HISTORY,
    website: 'https://en.dpm.org.cn',
    latitude: 39.9163,
    longitude: 116.3972
  },
  {
    id: '3',
    name: 'Shanghai Museum',
    location: '201 Renmin Avenue',
    city: 'Shanghai',
    description: 'Shanghai Museum is a museum of ancient Chinese art, renowned for its collection of bronzes, ceramics, paintings, and calligraphy.',
    establishedYear: 1952,
    visitorCount: 2.3,
    highlights: ['Ancient Chinese bronzes', 'Ming and Qing furniture', 'Chinese paintings', 'Calligraphy'],
    openingHours: '9:00 AM - 5:00 PM (Last entry 4:00 PM)',
    admissionFee: 'Free',
    imageUrl: 'common/images/shanghai_museum.jpg',
    rating: 4.7,
    category: MuseumCategory.ART,
    website: 'https://www.shanghaimuseum.net',
    latitude: 31.2304,
    longitude: 121.4737
  },
  {
    id: '4',
    name: 'Terracotta Army Museum',
    location: 'Lintong District',
    city: "Xi'an",
    description: 'The museum houses the Terracotta Army, a collection of terracotta sculptures depicting the armies of Qin Shi Huang, the first Emperor of China.',
    establishedYear: 1979,
    visitorCount: 6.5,
    highlights: ['Terracotta warriors', 'Bronze chariots and horses', 'Excavation pits', 'Historical artifacts'],
    openingHours: '8:30 AM - 5:30 PM (Mar-Nov), 8:30 AM - 5:00 PM (Dec-Feb)',
    admissionFee: 'CNY 120 (Mar-Nov), CNY 100 (Dec-Feb)',
    imageUrl: 'common/images/terracotta_museum.jpg',
    rating: 4.8,
    category: MuseumCategory.ARCHAEOLOGY,
    website: 'https://www.bmy.com.cn',
    latitude: 34.3849,
    longitude: 109.2784
  },
  {
    id: '5',
    name: 'National Art Museum of China',
    location: '1 Wusi Street',
    city: 'Beijing',
    description: 'The National Art Museum of China is the largest art museum in China, focusing on modern and contemporary Chinese art.',
    establishedYear: 1963,
    visitorCount: 1.8,
    highlights: ['Modern Chinese paintings', 'Contemporary art exhibitions', 'Oil paintings', 'Sculptures'],
    openingHours: '9:00 AM - 5:00 PM (Closed Mondays)',
    admissionFee: 'Free',
    imageUrl: 'common/images/national_art_museum.jpg',
    rating: 4.6,
    category: MuseumCategory.ART,
    website: 'https://www.namoc.org',
    latitude: 39.9225,
    longitude: 116.4064
  },
  {
    id: '6',
    name: 'Museum of the War of Chinese People\'s Resistance Against Japanese Aggression',
    location: 'Wanping City',
    city: 'Beijing',
    description: 'A museum dedicated to the Second Sino-Japanese War, located near the Marco Polo Bridge where the war began.',
    establishedYear: 1987,
    visitorCount: 1.2,
    highlights: ['Historical photographs', 'War artifacts', 'Documentary films', 'Memorial hall'],
    openingHours: '9:00 AM - 4:30 PM (Closed Mondays)',
    admissionFee: 'Free',
    imageUrl: 'common/images/war_museum.jpg',
    rating: 4.5,
    category: MuseumCategory.HISTORY,
    latitude: 39.8500,
    longitude: 116.2167
  },
  {
    id: '7',
    name: 'China Science and Technology Museum',
    location: '5 Beichen East Road',
    city: 'Beijing',
    description: 'One of the largest science museums in the world, featuring interactive exhibits on science and technology.',
    establishedYear: 1988,
    visitorCount: 3.5,
    highlights: ['Interactive science exhibits', 'Space exploration section', 'Robotics demonstrations', 'Children\'s science playground'],
    openingHours: '9:00 AM - 5:00 PM (Closed Mondays)',
    admissionFee: 'CNY 30',
    imageUrl: 'common/images/science_museum.jpg',
    rating: 4.7,
    category: MuseumCategory.SCIENCE,
    website: 'https://www.cstm.org.cn',
    latitude: 39.9956,
    longitude: 116.4079
  },
  {
    id: '8',
    name: 'Suzhou Museum',
    location: '204 Dongbei Street',
    city: 'Suzhou',
    description: 'Designed by I.M. Pei, this museum combines traditional Suzhou architecture with modern design, housing artifacts from the Wu region.',
    establishedYear: 1960,
    visitorCount: 2.1,
    highlights: ['Ming and Qing furniture', 'Suzhou embroidery', 'Ancient paintings', 'Traditional architecture'],
    openingHours: '9:00 AM - 5:00 PM (Closed Mondays)',
    admissionFee: 'Free',
    imageUrl: 'common/images/suzhou_museum.jpg',
    rating: 4.7,
    category: MuseumCategory.ART,
    website: 'https://www.szmuseum.com',
    latitude: 31.2989,
    longitude: 120.5853
  }
];

// Helper functions
export function getMuseumsByCity(city: string): Museum[] {
  return museums.filter(museum => museum.city === city);
}

export function getMuseumsByCategory(category: MuseumCategory): Museum[] {
  return museums.filter(museum => museum.category === category);
}

export function getTopRatedMuseums(limit: number = 5): Museum[] {
  return [...museums]
    .sort((a, b) => b.rating - a.rating)
    .slice(0, limit);
}

export function searchMuseums(query: string): Museum[] {
  const lowerQuery = query.toLowerCase();
  return museums.filter(museum =>
    museum.name.toLowerCase().includes(lowerQuery) ||
    museum.city.toLowerCase().includes(lowerQuery) ||
    museum.description.toLowerCase().includes(lowerQuery) ||
    museum.highlights.some(highlight => highlight.toLowerCase().includes(lowerQuery))
  );
}