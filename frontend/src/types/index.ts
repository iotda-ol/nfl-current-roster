// Types that mirror the Pydantic schemas in the backend

export interface Team {
  id: number;
  team_abbr: string;
  team_name: string;
  team_nick?: string | null;
  team_conf?: string | null;
  team_division?: string | null;
  team_color?: string | null;
  team_color2?: string | null;
  team_logo_wikipedia?: string | null;
  team_wordmark?: string | null;
  team_conference_logo?: string | null;
  team_league_logo?: string | null;
  team_logo_espn?: string | null;
  updated_at?: string | null;
}

export interface Player {
  id: number;
  player_id: string;
  full_name?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  position?: string | null;
  position_group?: string | null;
  team?: string | null;
  jersey_number?: number | null;
  status?: string | null;
  years_exp?: number | null;
  college?: string | null;
  height?: string | null;
  weight?: number | null;
  birth_date?: string | null;
  headshot_url?: string | null;
  depth_chart_position?: string | null;
  depth_chart_order?: number | null;
  season?: number | null;
  updated_at?: string | null;
}

export interface FreeAgent {
  id: number;
  player_id: string;
  full_name?: string | null;
  position?: string | null;
  position_group?: string | null;
  age?: number | null;
  years_exp?: number | null;
  college?: string | null;
  height?: string | null;
  weight?: number | null;
  last_team?: string | null;
  contract_value?: string | null;
  headshot_url?: string | null;
  updated_at?: string | null;
}

export interface DraftProspect {
  id: number;
  pick_number: number;
  round_number: number;
  pick_in_round?: number | null;
  team_abbr?: string | null;
  player_name?: string | null;
  position?: string | null;
  college?: string | null;
  height?: string | null;
  weight?: number | null;
  age?: number | null;
  games?: number | null;
  stats_json?: string | null;
  grade?: number | null;
  notes?: string | null;
  year: number;
  updated_at?: string | null;
}
