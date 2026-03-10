"use client";

import { useState } from "react";
import { useDraftProspects } from "@/hooks/useNflData";
import { Select } from "@/components/ui/select";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { ErrorMessage } from "@/components/ui/error-message";
import { Trophy } from "lucide-react";
import type { DraftProspect } from "@/types";

const POSITIONS = [
  "QB", "RB", "WR", "TE", "OT", "OG", "C",
  "DE", "DT", "EDGE", "LB", "CB", "S", "K", "P",
];

const ROUNDS = [1, 2, 3, 4, 5, 6, 7];

function GradeBar({ grade }: { grade: number | null | undefined }) {
  if (grade == null) return <span className="text-gray-400">—</span>;
  const pct = Math.min(100, (grade / 10) * 100);
  const color =
    grade >= 9 ? "bg-green-500" :
    grade >= 8 ? "bg-blue-500" :
    grade >= 7 ? "bg-yellow-500" :
    "bg-gray-400";

  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-sm font-semibold text-gray-700">{grade.toFixed(1)}</span>
    </div>
  );
}

function RoundBadge({ round }: { round: number }) {
  const colors: Record<number, string> = {
    1: "bg-yellow-100 text-yellow-800 border-yellow-200",
    2: "bg-blue-100 text-blue-800 border-blue-200",
    3: "bg-green-100 text-green-800 border-green-200",
    4: "bg-purple-100 text-purple-800 border-purple-200",
    5: "bg-orange-100 text-orange-800 border-orange-200",
    6: "bg-red-100 text-red-800 border-red-200",
    7: "bg-gray-100 text-gray-700 border-gray-200",
  };
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${
        colors[round] ?? colors[7]
      }`}
    >
      Rd {round}
    </span>
  );
}

export default function DraftRoomPage() {
  const [roundFilter, setRoundFilter] = useState<number | undefined>();
  const [posFilter, setPosFilter] = useState("");

  const { data: prospects, isLoading, error } = useDraftProspects({
    year: 2026,
    round_number: roundFilter,
    position: posFilter || undefined,
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-1">
          <Trophy className="w-8 h-8 text-yellow-500" />
          <h1 className="text-3xl font-bold text-gray-900">Draft Room 2026</h1>
        </div>
        <p className="text-gray-500">
          2026 NFL Draft order and top prospects with collegiate grades.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <Select
          value={roundFilter?.toString() ?? ""}
          onChange={(e) =>
            setRoundFilter(e.target.value ? Number(e.target.value) : undefined)
          }
          className="w-40"
        >
          <option value="">All Rounds</option>
          {ROUNDS.map((r) => (
            <option key={r} value={r}>
              Round {r}
            </option>
          ))}
        </Select>

        <Select
          value={posFilter}
          onChange={(e) => setPosFilter(e.target.value)}
          className="w-48"
        >
          <option value="">All Positions</option>
          {POSITIONS.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </Select>
      </div>

      {isLoading && <LoadingSpinner message="Loading draft prospects…" />}
      {error && <ErrorMessage message={(error as Error).message} />}

      {!isLoading && !error && (
        <>
          <p className="text-sm text-gray-500 mb-3">
            <strong>{prospects?.length ?? 0}</strong> prospects
          </p>

          {(prospects?.length ?? 0) === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <Trophy className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p>No prospects found.</p>
              <p className="text-sm mt-2">
                Run{" "}
                <code className="bg-gray-100 px-1 rounded">
                  python sync_db.py --draft
                </code>{" "}
                to populate data.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
              <table className="min-w-full divide-y divide-gray-100">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-16">
                      Pick
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider w-20">
                      Round
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Team
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Player
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Pos
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      College
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Ht / Wt
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Grade
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {prospects!.map((prospect: DraftProspect) => (
                    <tr
                      key={prospect.id}
                      className={`hover:bg-gray-50 transition-colors ${
                        prospect.round_number === 1 ? "bg-yellow-50/30" : ""
                      }`}
                    >
                      <td className="px-4 py-3 text-sm font-bold text-gray-700">
                        #{prospect.pick_number}
                      </td>
                      <td className="px-4 py-3">
                        <RoundBadge round={prospect.round_number} />
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500 font-medium">
                        {prospect.team_abbr ?? <span className="text-gray-300">TBD</span>}
                      </td>
                      <td className="px-4 py-3 text-sm font-semibold text-gray-900">
                        {prospect.player_name ?? "—"}
                      </td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700">
                          {prospect.position ?? "—"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {prospect.college ?? "—"}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {prospect.height ?? "—"}{" "}
                        {prospect.weight ? `/ ${prospect.weight} lbs` : ""}
                      </td>
                      <td className="px-4 py-3">
                        <GradeBar grade={prospect.grade} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
