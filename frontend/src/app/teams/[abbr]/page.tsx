"use client";

import { useParams } from "next/navigation";
import { useRoster, useTeam } from "@/hooks/useNflData";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { ErrorMessage } from "@/components/ui/error-message";
import type { Player } from "@/types";

const POSITION_ORDER = ["QB", "RB", "FB", "WR", "TE", "OT", "OG", "C", "DE", "DT", "LB", "CB", "S", "K", "P", "LS"];

function groupByPosition(players: Player[]): Record<string, Player[]> {
  const grouped: Record<string, Player[]> = {};
  for (const player of players) {
    const pos = player.position ?? "UNK";
    if (!grouped[pos]) grouped[pos] = [];
    grouped[pos].push(player);
  }
  return grouped;
}

function sortPositions(positions: string[]): string[] {
  return positions.sort((a, b) => {
    const ai = POSITION_ORDER.indexOf(a);
    const bi = POSITION_ORDER.indexOf(b);
    if (ai === -1 && bi === -1) return a.localeCompare(b);
    if (ai === -1) return 1;
    if (bi === -1) return -1;
    return ai - bi;
  });
}

export default function TeamRosterPage() {
  const params = useParams();
  const abbr = (params?.abbr as string)?.toUpperCase();

  const { data: team, isLoading: teamLoading } = useTeam(abbr);
  const { data: players, isLoading: rosterLoading, error } = useRoster(abbr);

  if (teamLoading || rosterLoading) {
    return <LoadingSpinner message={`Loading ${abbr} roster…`} />;
  }

  if (error) {
    return (
      <div className="p-8">
        <ErrorMessage message={(error as Error).message} />
      </div>
    );
  }

  const grouped = groupByPosition(players ?? []);
  const positions = sortPositions(Object.keys(grouped));

  return (
    <div className="p-6 max-w-5xl mx-auto">
      {/* Team header */}
      <div
        className="rounded-xl p-6 mb-8 text-white"
        style={{
          backgroundColor: team?.team_color
            ? `#${team.team_color.replace("#", "")}`
            : "#1e3a5f",
        }}
      >
        <div className="flex items-center gap-4">
          {team?.team_logo_espn && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={team.team_logo_espn}
              alt={abbr}
              className="w-16 h-16 object-contain"
            />
          )}
          <div>
            <h1 className="text-3xl font-bold">{team?.team_name ?? abbr}</h1>
            <p className="text-white/80">
              {team?.team_division} · {players?.length ?? 0} players
            </p>
          </div>
        </div>
      </div>

      {/* Roster by position */}
      {positions.length === 0 ? (
        <p className="text-gray-500 text-sm">No roster data available. Run the sync script to populate data.</p>
      ) : (
        <div className="space-y-8">
          {positions.map((pos) => (
            <section key={pos}>
              <h2 className="text-lg font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="inline-block w-10 text-center text-xs font-bold bg-gray-200 text-gray-700 rounded px-1 py-0.5">
                  {pos}
                </span>
                {pos}
              </h2>
              <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
                <table className="min-w-full divide-y divide-gray-100">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">#</th>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Name</th>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Ht</th>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Wt</th>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">Exp</th>
                      <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">College</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {grouped[pos].map((player) => (
                      <tr key={player.player_id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm text-gray-500 w-10">
                          {player.jersey_number ?? "—"}
                        </td>
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">
                          <div className="flex items-center gap-3">
                            {player.headshot_url ? (
                              // eslint-disable-next-line @next/next/no-img-element
                              <img
                                src={player.headshot_url}
                                alt=""
                                className="w-8 h-8 rounded-full object-cover bg-gray-200"
                                onError={(e) => {
                                  (e.target as HTMLImageElement).style.display = "none";
                                }}
                              />
                            ) : (
                              <div className="w-8 h-8 rounded-full bg-gray-200" aria-hidden="true" />
                            )}
                            {player.full_name ?? "Unknown"}
                          </div>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">{player.height ?? "—"}</td>
                        <td className="px-4 py-3 text-sm text-gray-500">
                          {player.weight ? `${player.weight} lbs` : "—"}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">
                          {player.years_exp !== null && player.years_exp !== undefined
                            ? player.years_exp === 0
                              ? "Rookie"
                              : `${player.years_exp} yr${player.years_exp !== 1 ? "s" : ""}`
                            : "—"}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500">{player.college ?? "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  );
}
