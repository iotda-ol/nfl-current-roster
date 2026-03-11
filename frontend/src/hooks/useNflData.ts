import { useQuery } from "@tanstack/react-query";
import {
  fetchDraftProspects,
  fetchFreeAgents,
  fetchPlayer,
  fetchPlayerSearch,
  fetchRoster,
  fetchTeam,
  fetchTeams,
  type DraftFilters,
  type FreeAgentFilters,
} from "@/lib/api";

// ── Teams ─────────────────────────────────────────────────────────────────────

export function useTeams() {
  return useQuery({
    queryKey: ["teams"],
    queryFn: fetchTeams,
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

export function useTeam(abbr: string) {
  return useQuery({
    queryKey: ["teams", abbr],
    queryFn: () => fetchTeam(abbr),
    enabled: Boolean(abbr),
    staleTime: 1000 * 60 * 60,
  });
}

// ── Rosters ───────────────────────────────────────────────────────────────────

export function useRoster(teamAbbr: string, season?: number) {
  return useQuery({
    queryKey: ["rosters", teamAbbr, season],
    queryFn: () => fetchRoster(teamAbbr, season),
    enabled: Boolean(teamAbbr),
    staleTime: 1000 * 60 * 30, // 30 minutes
  });
}

export function usePlayer(playerId: string) {
  return useQuery({
    queryKey: ["players", playerId],
    queryFn: () => fetchPlayer(playerId),
    enabled: Boolean(playerId),
  });
}

export function usePlayerSearch(query: string) {
  return useQuery({
    queryKey: ["player-search", query],
    queryFn: () => fetchPlayerSearch(query),
    enabled: query.length >= 2,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

// ── Free Agents ───────────────────────────────────────────────────────────────

export function useFreeAgents(filters?: FreeAgentFilters) {
  return useQuery({
    queryKey: ["free-agents", filters],
    queryFn: () => fetchFreeAgents(filters),
    staleTime: 1000 * 60 * 15, // 15 minutes
  });
}

// ── Draft ─────────────────────────────────────────────────────────────────────

export function useDraftProspects(filters?: DraftFilters) {
  return useQuery({
    queryKey: ["draft-prospects", filters],
    queryFn: () => fetchDraftProspects(filters),
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}
