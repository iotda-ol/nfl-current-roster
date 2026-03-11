"use client";

import { useState, useMemo } from "react";
import { useFreeAgents } from "@/hooks/useNflData";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { ErrorMessage } from "@/components/ui/error-message";
import { Search } from "lucide-react";

const POSITIONS = [
  "QB", "RB", "FB", "WR", "TE", "OT", "OG", "C",
  "DE", "DT", "LB", "CB", "S", "K", "P", "LS",
];

export default function FreeAgentsPage() {
  const [search, setSearch] = useState("");
  const [position, setPosition] = useState("");

  const { data: agents, isLoading, error } = useFreeAgents();

  const filtered = useMemo(() => {
    if (!agents) return [];
    return agents.filter((a) => {
      const matchesSearch =
        !search ||
        (a.full_name ?? "").toLowerCase().includes(search.toLowerCase());
      const matchesPos =
        !position || a.position === position;
      return matchesSearch && matchesPos;
    });
  }, [agents, search, position]);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Free Agents</h1>
        <p className="text-gray-500 mt-1">
          Current unrestricted and restricted free agents.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            type="text"
            placeholder="Search player name…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select
          value={position}
          onChange={(e) => setPosition(e.target.value)}
          className="w-full sm:w-48"
        >
          <option value="">All Positions</option>
          {POSITIONS.map((pos) => (
            <option key={pos} value={pos}>
              {pos}
            </option>
          ))}
        </Select>
      </div>

      {isLoading && <LoadingSpinner message="Loading free agents…" />}

      {error && (
        <ErrorMessage message={(error as Error).message} />
      )}

      {!isLoading && !error && (
        <>
          <p className="text-sm text-gray-500 mb-3">
            Showing <strong>{filtered.length}</strong> of{" "}
            <strong>{agents?.length ?? 0}</strong> free agents
          </p>

          {filtered.length === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <Search className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p>No free agents found matching your criteria.</p>
              {agents?.length === 0 && (
                <p className="text-sm mt-2">
                  Run <code className="bg-gray-100 px-1 rounded">python sync_db.py --free-agents</code> to populate data.
                </p>
              )}
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
              <table className="min-w-full divide-y divide-gray-100">
                <thead className="bg-gray-50">
                  <tr>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Player
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Position
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Last Team
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Age
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Ht / Wt
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Exp
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      College
                    </th>
                    <th scope="col" className="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">
                      Contract Value
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {filtered.map((agent) => (
                    <tr key={agent.player_id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-3">
                          {agent.headshot_url ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img
                              src={agent.headshot_url}
                              alt=""
                              className="w-9 h-9 rounded-full object-cover bg-gray-200"
                              onError={(e) => {
                                (e.target as HTMLImageElement).style.display = "none";
                              }}
                            />
                          ) : (
                            <div className="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center text-xs text-gray-500 font-bold" aria-hidden="true">
                              {(agent.full_name ?? "?")[0]}
                            </div>
                          )}
                          <span className="text-sm font-medium text-gray-900">
                            {agent.full_name ?? "Unknown"}
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {agent.position ?? "—"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">{agent.last_team ?? "—"}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {agent.age != null ? agent.age : "—"}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {agent.height ?? "—"} / {agent.weight ? `${agent.weight} lbs` : "—"}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {agent.years_exp !== null && agent.years_exp !== undefined
                          ? agent.years_exp === 0
                            ? "Rookie"
                            : `${agent.years_exp} yrs`
                          : "—"}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">{agent.college ?? "—"}</td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {agent.contract_value ? (
                          <span className="text-green-700 font-medium">{agent.contract_value}</span>
                        ) : (
                          "—"
                        )}
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
