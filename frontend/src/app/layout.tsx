import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { QueryProvider } from "@/components/layout/QueryProvider";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: {
    default: "NFL Data Dashboard",
    template: "%s | NFL Data Dashboard",
  },
  description:
    "Explore real-time NFL roster data, current free agents, and the upcoming 2026 NFL Draft with live stats and filters.",
  keywords: ["NFL", "football", "roster", "free agents", "draft", "2026 NFL Draft"],
  openGraph: {
    title: "NFL Data Dashboard",
    description: "Real-time NFL roster data, free agency tracker, and 2026 draft room.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-50`}>
        <QueryProvider>
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 overflow-auto">{children}</main>
          </div>
        </QueryProvider>
      </body>
    </html>
  );
}
