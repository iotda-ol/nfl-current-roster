import Link from "next/link";
import { UserCheck, Trophy, Users } from "lucide-react";

export default function Home() {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">NFL Data Dashboard</h1>
        <p className="text-lg text-gray-600">
          Real-time roster data, free agency tracker, and 2026 draft room.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          href="/free-agents"
          className="group flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:border-blue-300 transition-all"
        >
          <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center group-hover:bg-blue-200 transition-colors">
            <UserCheck className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Free Agency</h2>
            <p className="mt-1 text-sm text-gray-500">
              Browse available free agents with position filters and search.
            </p>
          </div>
        </Link>

        <Link
          href="/draft-room"
          className="group flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md hover:border-yellow-300 transition-all"
        >
          <div className="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center group-hover:bg-yellow-200 transition-colors">
            <Trophy className="w-6 h-6 text-yellow-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Draft Room 2026</h2>
            <p className="mt-1 text-sm text-gray-500">
              2026 NFL Draft order with collegiate stats and grades.
            </p>
          </div>
        </Link>

        <div className="flex flex-col gap-4 p-6 rounded-xl border border-gray-200 bg-white shadow-sm">
          <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
            <Users className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Team Rosters</h2>
            <p className="mt-1 text-sm text-gray-500">
              Select any team from the sidebar to view their current roster.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

