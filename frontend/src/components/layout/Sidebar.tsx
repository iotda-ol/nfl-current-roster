"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useTeams } from "@/hooks/useNflData";
import {
  Users,
  UserCheck,
  Trophy,
  ChevronDown,
  ChevronRight,
  Loader2,
  Home,
} from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { label: "Home", href: "/", icon: Home },
  { label: "Free Agency", href: "/free-agents", icon: UserCheck },
  { label: "Draft Room 2026", href: "/draft-room", icon: Trophy },
];

const CONFERENCES = ["AFC", "NFC"];
const DIVISIONS = ["North", "South", "East", "West"];

export function Sidebar() {
  const pathname = usePathname();
  const { data: teams, isLoading } = useTeams();
  const [teamsOpen, setTeamsOpen] = useState(true);

  const groupedTeams = teams
    ? CONFERENCES.flatMap((conf) =>
        DIVISIONS.map((div) => ({
          label: `${conf} ${div}`,
          teams: teams.filter(
            (t) =>
              t.team_conf === conf &&
              t.team_division?.includes(div)
          ),
        }))
      ).filter((g) => g.teams.length > 0)
    : [];

  return (
    <aside className="flex flex-col w-64 min-h-screen bg-gray-900 text-white border-r border-gray-700">
      {/* Logo / Title */}
      <div className="px-6 py-5 border-b border-gray-700">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl">🏈</span>
          <span className="text-lg font-bold tracking-tight">NFL Dashboard</span>
        </Link>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {/* Main nav items */}
        {NAV_ITEMS.map(({ label, href, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            aria-current={pathname === href ? "page" : undefined}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
              pathname === href
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-gray-800 hover:text-white"
            )}
          >
            <Icon className="w-4 h-4 shrink-0" aria-hidden="true" />
            {label}
          </Link>
        ))}

        {/* Teams section */}
        <div className="mt-4">
          <button
            onClick={() => setTeamsOpen((o) => !o)}
            aria-expanded={teamsOpen}
            aria-controls="teams-nav"
            className="flex items-center justify-between w-full px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <span className="flex items-center gap-2">
              <Users className="w-4 h-4" aria-hidden="true" />
              Teams
            </span>
            {teamsOpen ? (
              <ChevronDown className="w-4 h-4" aria-hidden="true" />
            ) : (
              <ChevronRight className="w-4 h-4" aria-hidden="true" />
            )}
          </button>

          {teamsOpen && (
            <div id="teams-nav" className="mt-1 ml-2 space-y-3">
              {isLoading && (
                <div className="flex items-center gap-2 px-3 py-2 text-gray-500 text-sm">
                  <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
                  <span>Loading teams…</span>
                </div>
              )}
              {groupedTeams.map(({ label, teams: divTeams }) => (
                <div key={label}>
                  <p className="px-3 py-1 text-xs uppercase font-semibold text-gray-500 tracking-wider">
                    {label}
                  </p>
                  {divTeams.map((team) => (
                    <Link
                      key={team.team_abbr}
                      href={`/teams/${team.team_abbr}`}
                      aria-current={pathname === `/teams/${team.team_abbr}` ? "page" : undefined}
                      className={cn(
                        "flex items-center gap-2 px-3 py-1.5 rounded-md text-sm transition-colors",
                        pathname === `/teams/${team.team_abbr}`
                          ? "bg-blue-600 text-white"
                          : "text-gray-300 hover:bg-gray-800 hover:text-white"
                      )}
                    >
                      {team.team_logo_espn ? (
                        // eslint-disable-next-line @next/next/no-img-element
                        <img
                          src={team.team_logo_espn}
                          alt=""
                          className="w-5 h-5 object-contain"
                        />
                      ) : (
                        <span className="w-5 h-5 flex items-center justify-center text-xs font-bold bg-gray-700 rounded-sm" aria-hidden="true">
                          {team.team_abbr.slice(0, 2)}
                        </span>
                      )}
                      <span className="truncate">{team.team_nick ?? team.team_name}</span>
                    </Link>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      </nav>
    </aside>
  );
}
