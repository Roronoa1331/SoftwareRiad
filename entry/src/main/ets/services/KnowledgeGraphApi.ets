import { http } from '@kit.NetworkKit';
import {
  CulturalRelic,
  getOfflineRelics,
  getOfflineStats,
  KgStats,
  searchRelics
} from '../models/Artifact';

// Set to true to skip network calls and use bundled offline data only
const OFFLINE_ONLY: boolean = true;
const API_BASE_URL: string = 'http://10.0.2.2:8000';
const HTTP_TIMEOUT_MS: number = 3000;

export class KnowledgeGraphApi {
  static isLive: boolean = false;

  /** Synchronous offline data — always available on first frame. */
  static getOfflineArtifacts(search?: string): CulturalRelic[] {
    const relics = getOfflineRelics();
    if (search && search.trim().length > 0) {
      return searchRelics(search, relics);
    }
    return relics;
  }

  static getOfflineKgStats(): KgStats {
    return getOfflineStats(getOfflineRelics());
  }

  /** Optional background refresh from backend API. */
  static async tryFetchLive(search?: string): Promise<{ relics: CulturalRelic[]; stats: KgStats } | null> {
    if (OFFLINE_ONLY) {
      return null;
    }
    try {
      const stats = await KnowledgeGraphApi.fetchStatsFromNetwork();
      const relics = await KnowledgeGraphApi.fetchArtifactsFromNetwork(search);
      if (stats !== null && relics.length > 0) {
        KnowledgeGraphApi.isLive = true;
        return { relics, stats };
      }
    } catch (_e) {
      KnowledgeGraphApi.isLive = false;
    }
    return null;
  }

  private static async fetchStatsFromNetwork(): Promise<KgStats | null> {
    const client = http.createHttp();
    try {
      const response = await client.request(`${API_BASE_URL}/api/stats`, {
        method: http.RequestMethod.GET,
        connectTimeout: HTTP_TIMEOUT_MS,
        readTimeout: HTTP_TIMEOUT_MS,
        header: { 'Content-Type': 'application/json' }
      });
      if (response.responseCode === 200 && response.result) {
        return JSON.parse(response.result as string) as KgStats;
      }
    } catch (_e) {
      // Use offline fallback
    } finally {
      client.destroy();
    }
    return null;
  }

  private static async fetchArtifactsFromNetwork(search?: string): Promise<CulturalRelic[]> {
    const client = http.createHttp();
    try {
      let url = `${API_BASE_URL}/api/artifacts?limit=50`;
      if (search && search.trim().length > 0) {
        url += `&search=${encodeURIComponent(search.trim())}`;
      }
      const response = await client.request(url, {
        method: http.RequestMethod.GET,
        connectTimeout: HTTP_TIMEOUT_MS,
        readTimeout: HTTP_TIMEOUT_MS,
        header: { 'Content-Type': 'application/json' }
      });
      if (response.responseCode === 200 && response.result) {
        return JSON.parse(response.result as string) as CulturalRelic[];
      }
    } catch (_e) {
      // Use offline fallback
    } finally {
      client.destroy();
    }
    return [];
  }
}
