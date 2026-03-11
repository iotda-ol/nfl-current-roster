import type { DraftProspect, FreeAgent, Player, Team } from "@/types";

// All API calls go through Next.js rewrites which proxy to the backend.
// Set NEXT_PUBLIC_API_URL to override (e.g. for direct access in testing).
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "";

export interface FreeAgentFilters {
  position?: string;
  search?: string;
}

export interface DraftFilters {
  year?: number;
  round_number?: number;
  position?: string;
}

async function apiFetch<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${res.statusText} (${url})`);
  }
  return res.json() as Promise<T>;
}

// ── Teams ─────────────────────────────────────────────────────────────────────

export function fetchTeams(): Promise<Team[]> {
  return apiFetch<Team[]>("/api/teams/");
}

export function fetchTeam(abbr: string): Promise<Team> {
  return apiFetch<Team>(`/api/teams/${encodeURIComponent(abbr)}`);
}

// ── Rosters ───────────────────────────────────────────────────────────────────

export function fetchRoster(teamAbbr: string, season?: number): Promise<Player[]> {
  const params = season ? `?season=${season}` : "";
  return apiFetch<Player[]>(`/api/rosters/${encodeURIComponent(teamAbbr)}${params}`);
}

export function fetchPlayer(playerId: string): Promise<Player> {
  return apiFetch<Player>(`/api/rosters/player/${encodeURIComponent(playerId)}`);
}

export function fetchPlayerSearch(query: string): Promise<Player[]> {
  return apiFetch<Player[]>(`/api/rosters/search?q=${encodeURIComponent(query)}`);
}

// ── Free Agents ───────────────────────────────────────────────────────────────

export function fetchFreeAgents(filters?: FreeAgentFilters): Promise<FreeAgent[]> {
  const params = new URLSearchParams();
  if (filters?.position) params.set("position", filters.position);
  if (filters?.search) params.set("search", filters.search);
  const qs = params.toString() ? `?${params.toString()}` : "";
  return apiFetch<FreeAgent[]>(`/api/free-agents/${qs}`);
}

// ── Draft ─────────────────────────────────────────────────────────────────────

export function fetchDraftProspects(filters?: DraftFilters): Promise<DraftProspect[]> {
  const params = new URLSearchParams();
  if (filters?.year) params.set("year", String(filters.year));
  if (filters?.round_number) params.set("round_number", String(filters.round_number));
  if (filters?.position) params.set("position", filters.position);
  const qs = params.toString() ? `?${params.toString()}` : "";
  return apiFetch<DraftProspect[]>(`/api/draft/prospects${qs}`);
}
