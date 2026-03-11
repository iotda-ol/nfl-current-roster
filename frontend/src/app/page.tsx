"use client";

import Link from "next/link";
import { UserCheck, Trophy, Users, ArrowRight } from "lucide-react";
import { useTeams, useFreeAgents, useDraftProspects } from "@/hooks/useNflData";

function StatCard({ label, value }: { label: string; value: number | undefined }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm text-center">
      <p className="text-3xl font-bold text-gray-900">
        {value !== undefined ? value.toLocaleString() : "—"}
      </p>
      <p className="mt-1 text-sm text-gray-500">{label}</p>
    </div>
  );
}

export default function Home() {
  const { data: teams } = useTeams();
  const { data: agents } = useFreeAgents();
  const { data: prospects } = useDraftProspects({ year: 2026 });

  return (
    <div className="p-8 max-w-5xl mx-auto">
      {/* Hero */}
      <div className="mb-10">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          🏈 NFL Data Dashboard
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl">
          Explore real-time NFL roster data, current free agents, and the upcoming
          2026 draft — all in one place.
        </p>
      </div>

      {/* Live stats */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-10">
        <StatCard label="NFL Teams" value={teams?.length} />
        <StatCard label="Free Agents" value={agents?.length} />
        <StatCard label="2026 Draft Prospects" value={prospects?.length} />
      </div>

      {/* Feature cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/free-agents"
          className="group flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:border-blue-300 transition-all"
          aria-label="Browse free agents"
        >
          <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors">
            <UserCheck className="w-6 h-6 text-blue-600" aria-hidden="true" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900">Free Agency</h2>
            <p className="mt-1 text-sm text-gray-500">
              Browse available free agents with position filters and name search.
            </p>
          </div>
          <span className="flex items-center gap-1 text-xs font-medium text-blue-600 group-hover:gap-2 transition-all">
            View free agents <ArrowRight className="w-3 h-3" aria-hidden="true" />
          </span>
        </Link>

        <Link
          href="/draft-room"
          className="group flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:border-yellow-300 transition-all"
          aria-label="Open 2026 Draft Room"
        >
          <div className="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center group-hover:bg-yellow-200 transition-colors">
            <Trophy className="w-6 h-6 text-yellow-600" aria-hidden="true" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900">Draft Room 2026</h2>
            <p className="mt-1 text-sm text-gray-500">
              2026 NFL Draft order with collegiate stats and prospect grades.
            </p>
          </div>
          <span className="flex items-center gap-1 text-xs font-medium text-yellow-600 group-hover:gap-2 transition-all">
            View prospects <ArrowRight className="w-3 h-3" aria-hidden="true" />
          </span>
        </Link>

        <div className="flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm">
          <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
            <Users className="w-6 h-6 text-green-600" aria-hidden="true" />
          </div>
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-900">Team Rosters</h2>
            <p className="mt-1 text-sm text-gray-500">
              Select any of the {teams?.length ?? 32} NFL teams from the sidebar to
              view their current roster grouped by position.
            </p>
          </div>
          <span className="text-xs text-gray-400">Use the sidebar →</span>
        </div>
      </div>
    </div>
  );
}

