// Cultural relic artifact model for knowledge graph subsystem (6.3.1)

export interface CulturalRelic {
  artifact_id: string;
  external_id: string;
  name: string;
  image_url: string;
  local_image_path?: string;
  age?: string;
  dynasty?: string;
  artifact_type?: string;
  material?: string;
  introduction?: string;
  detail_url: string;
  museum_name: string;
  museum_location?: string;
  artist?: string;
  culture?: string;
  country_of_origin?: string;
}

export interface KgStats {
  mysql_artifacts: number;
  neo4j_nodes: number;
  neo4j_relationships: number;
  kg_namespace: string;
}

export interface KgTriplePreview {
  predicate: string;
  object: string;
}

// Offline sample: Chinese cultural relics held at overseas museums (The Met, New York)
export const SAMPLE_RELICS: CulturalRelic[] = [
  {
    artifact_id: 'the_metrop_39799',
    external_id: '39799',
    name: 'Bottle with dragon and phoenix',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP105977.jpg',
    age: 'Ming dynasty (1368–1644)',
    dynasty: 'Ming Dynasty',
    artifact_type: 'Bottle',
    material: 'Porcelain with underglaze blue decoration',
    introduction: 'Ming dynasty porcelain bottle with dragon and phoenix motif, symbols of imperial power.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/39799',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_42102',
    external_id: '42102',
    name: 'Seated Buddha',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151037.jpg',
    age: 'late 6th century',
    dynasty: 'Northern Wei Dynasty',
    artifact_type: 'Sculpture',
    material: 'Gilt bronze',
    introduction: 'Northern Wei gilt bronze seated Buddha reflecting the spread of Buddhist art in China.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/42102',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_49269',
    external_id: '49269',
    name: 'Landscape in the Style of Dong Yuan',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP153442.jpg',
    age: '17th century',
    dynasty: 'Qing Dynasty',
    artifact_type: 'Hanging scroll',
    material: 'Ink and color on silk',
    introduction: 'Qing dynasty landscape painting in the style of Song master Dong Yuan.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/49269',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    artist: 'Wang Hui',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_544483',
    external_id: '544483',
    name: 'Ritual wine vessel (guang)',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP-18676-001.jpg',
    age: '13th–11th century B.C.',
    dynasty: 'Shang Dynasty',
    artifact_type: 'Ritual vessel',
    material: 'Bronze',
    introduction: 'Shang dynasty bronze ritual wine vessel with taotie mask decoration.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/544483',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_7818',
    external_id: '7818',
    name: 'Covered jar with dragon design',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP-13039-001.jpg',
    age: 'Kangxi period (1662–1722)',
    dynasty: 'Qing Dynasty',
    artifact_type: 'Jar',
    material: 'Porcelain with celadon glaze',
    introduction: 'Kangxi period Longquan celadon jar with dragon design.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/7818',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_49331',
    external_id: '49331',
    name: 'Mirror with animals of the four directions',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151046.jpg',
    age: 'Tang dynasty (618–907)',
    dynasty: 'Tang Dynasty',
    artifact_type: 'Mirror',
    material: 'Bronze',
    introduction: 'Tang dynasty bronze mirror with animals of the four directions.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/49331',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_42133',
    external_id: '42133',
    name: 'Bodhisattva Avalokiteshvara (Guanyin)',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151039.jpg',
    age: '11th century',
    dynasty: 'Song Dynasty',
    artifact_type: 'Sculpture',
    material: 'Wood with pigment',
    introduction: 'Song dynasty wooden sculpture of Bodhisattva Avalokiteshvara (Guanyin).',
    detail_url: 'https://www.metmuseum.org/art/collection/search/42133',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_42100',
    external_id: '42100',
    name: 'Standing Buddha',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151036.jpg',
    age: 'late 5th century',
    dynasty: 'Northern Wei Dynasty',
    artifact_type: 'Sculpture',
    material: 'Gilt bronze',
    introduction: 'Northern Wei standing Buddha in gilt bronze, Northern China.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/42100',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_72805',
    external_id: '72805',
    name: 'Bi disk with grain pattern',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP119035.jpg',
    age: 'Eastern Zhou dynasty (770–256 B.C.)',
    dynasty: 'Zhou Dynasty',
    artifact_type: 'Ritual object',
    material: 'Jade (nephrite)',
    introduction: 'Eastern Zhou jade bi disk with grain pattern, used in ancient rituals.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/72805',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_39645',
    external_id: '39645',
    name: 'Vase with peach and bat design',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP105974.jpg',
    age: 'Qing dynasty (1644–1911), Qianlong period',
    dynasty: 'Qing Dynasty',
    artifact_type: 'Vase',
    material: 'Porcelain with famille rose enamel decoration',
    introduction: 'Qianlong period famille rose vase with peach and bat motifs symbolizing longevity.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/39645',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_45308',
    external_id: '45308',
    name: 'Brush washer in the shape of a lotus leaf',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151049.jpg',
    age: 'Southern Song dynasty (1127–1279)',
    dynasty: 'Song Dynasty',
    artifact_type: 'Brush washer',
    material: 'Stoneware with glaze (Guan ware)',
    introduction: 'Southern Song Guan ware brush washer shaped as a lotus leaf for scholar\'s studio.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/45308',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_44739',
    external_id: '44739',
    name: 'Dish with fish and aquatic plants',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP105978.jpg',
    age: 'Ming dynasty (1368–1644), Xuande period',
    dynasty: 'Ming Dynasty',
    artifact_type: 'Dish',
    material: 'Porcelain with underglaze blue decoration',
    introduction: 'Xuande period blue-and-white dish with fish and aquatic plants.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/44739',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_49164',
    external_id: '49164',
    name: 'Altarpiece with Buddha and bodhisattvas',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP153441.jpg',
    age: '14th century',
    dynasty: 'Yuan Dynasty',
    artifact_type: 'Altarpiece',
    material: 'Ink and color on silk',
    introduction: 'Yuan dynasty Buddhist altarpiece painting with Buddha and bodhisattvas.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/49164',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_5029',
    external_id: '5029',
    name: 'Relief with dancing figure',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP119034.jpg',
    age: '2nd century B.C.',
    dynasty: 'Han Dynasty',
    artifact_type: 'Relief',
    material: 'Limestone',
    introduction: 'Han dynasty limestone relief with dancing figure from ancient China.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/5029',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_44638',
    external_id: '44638',
    name: 'Snuff bottle with landscape',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP105976.jpg',
    age: 'Qing dynasty (1644–1911)',
    dynasty: 'Qing Dynasty',
    artifact_type: 'Snuff bottle',
    material: 'Glass with painted decoration',
    introduction: 'Qing dynasty inside-painted glass snuff bottle with landscape scene.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/44638',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_49332',
    external_id: '49332',
    name: 'Mirror with inscription',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151047.jpg',
    age: 'Tang dynasty (618–907)',
    dynasty: 'Tang Dynasty',
    artifact_type: 'Mirror',
    material: 'Bronze',
    introduction: 'Tang dynasty bronze mirror with dedicatory inscription.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/49332',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_400854',
    external_id: '400854',
    name: 'Old Trees, Level Distance',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP-18707-001.jpg',
    age: '1080',
    dynasty: 'Song Dynasty',
    artifact_type: 'Hanging scroll',
    material: 'Ink and color on silk',
    introduction: 'Landscape painting attributed to Guo Xi, Northern Song master of monumental landscape.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/400854',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    artist: 'Guo Xi',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_42137',
    external_id: '42137',
    name: 'Head of a bodhisattva',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP151040.jpg',
    age: '6th century',
    dynasty: 'Northern Qi Dynasty',
    artifact_type: 'Sculpture',
    material: 'Sandstone with pigment',
    introduction: 'Northern Qi sandstone head of a bodhisattva with traces of original pigment.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/42137',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_44738',
    external_id: '44738',
    name: 'Plate with lotus scroll',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP105975.jpg',
    age: 'Ming dynasty (1368–1644), Yongle period',
    dynasty: 'Ming Dynasty',
    artifact_type: 'Plate',
    material: 'Porcelain with underglaze blue decoration',
    introduction: 'Yongle period blue-and-white plate with lotus scroll design from imperial kilns.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/44738',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  },
  {
    artifact_id: 'the_metrop_72806',
    external_id: '72806',
    name: 'Cong tube with mask design',
    image_url: 'https://images.metmuseum.org/CRDImages/as/original/DP119036.jpg',
    age: 'Neolithic period, Liangzhu culture (ca. 3300–2250 B.C.)',
    dynasty: 'Neolithic',
    artifact_type: 'Ritual object',
    material: 'Jade (nephrite)',
    introduction: 'Liangzhu culture jade cong tube with mask design, prehistoric China.',
    detail_url: 'https://www.metmuseum.org/art/collection/search/72806',
    museum_name: 'The Metropolitan Museum of Art',
    museum_location: 'New York, USA',
    culture: 'China',
    country_of_origin: 'China'
  }
];

export function searchRelics(query: string, relics: CulturalRelic[]): CulturalRelic[] {
  if (!query.trim()) {
    return relics;
  }
  const lower = query.toLowerCase();
  return relics.filter(item =>
    item.name.toLowerCase().includes(lower) ||
    (item.dynasty !== undefined && item.dynasty.toLowerCase().includes(lower)) ||
    (item.material !== undefined && item.material.toLowerCase().includes(lower)) ||
    (item.artifact_type !== undefined && item.artifact_type.toLowerCase().includes(lower)) ||
    (item.artist !== undefined && item.artist.toLowerCase().includes(lower))
  );
}

/** Build knowledge-graph triple previews shown in the detail view. */
export function buildTriplePreview(relic: CulturalRelic): KgTriplePreview[] {
  const triples: KgTriplePreview[] = [
    { predicate: 'collected_in', object: relic.museum_name },
    { predicate: 'has_name', object: relic.name }
  ];
  if (relic.dynasty) {
    triples.push({ predicate: 'belongs_to_dynasty', object: relic.dynasty });
  }
  if (relic.country_of_origin) {
    triples.push({ predicate: 'created_in', object: relic.country_of_origin });
  }
  if (relic.artist) {
    triples.push({ predicate: 'created_by', object: relic.artist });
  }
  if (relic.material) {
    triples.push({ predicate: 'material_is', object: relic.material });
  }
  if (relic.artifact_type) {
    triples.push({ predicate: 'type_is', object: relic.artifact_type });
  }
  if (relic.culture) {
    triples.push({ predicate: 'belongs_to_culture', object: relic.culture });
  }
  if (relic.age) {
    triples.push({ predicate: 'has_age', object: relic.age });
  }
  return triples;
}

/** Compute offline graph statistics from bundled sample data. */
export function getOfflineStats(relics: CulturalRelic[] = SAMPLE_RELICS): KgStats {
  const dynastySet: Set<string> = new Set();
  const materialSet: Set<string> = new Set();
  const typeSet: Set<string> = new Set();
  const artistSet: Set<string> = new Set();
  let relationshipCount: number = 0;

  relics.forEach((relic: CulturalRelic) => {
    relationshipCount += buildTriplePreview(relic).length;
    if (relic.dynasty) {
      dynastySet.add(relic.dynasty);
    }
    if (relic.material) {
      materialSet.add(relic.material);
    }
    if (relic.artifact_type) {
      typeSet.add(relic.artifact_type);
    }
    if (relic.artist) {
      artistSet.add(relic.artist);
    }
  });

  // Artifacts + 1 museum + 1 location + unique dynasties/materials/types/artists/culture
  const nodeCount: number = relics.length + 1 + 1 + dynastySet.size +
    materialSet.size + typeSet.size + artistSet.size + 1;

  return {
    mysql_artifacts: relics.length,
    neo4j_nodes: nodeCount,
    neo4j_relationships: relationshipCount,
    kg_namespace: 'http://softwareenriad.org/kg/'
  };
}

export function getOfflineRelics(): CulturalRelic[] {
  return SAMPLE_RELICS.slice();
}
