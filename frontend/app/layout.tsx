import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

export const metadata: Metadata = {
  title: "OBSIL — Badanie konfliktu interesów",
  description:
    "Narzędzie wspomagające ocenę konfliktu interesów dla radców prawnych",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl" className={cn("h-full antialiased", "font-sans", geist.variable)}>
      <body className="min-h-full flex flex-col">
        {/* Beta banner */}
        <div className="bg-beta text-white text-center text-sm py-1.5 font-medium">
          WERSJA BETA — Narzędzie wspomagające, nie zastępuje oceny radcy
          prawnego
        </div>

        {/* Navigation */}
        <header className="bg-surface border-b border-border px-6 py-4">
          <nav className="max-w-5xl mx-auto flex items-center justify-between">
            <Link
              href="/"
              className="text-xl font-bold text-primary tracking-tight"
            >
              OBSIL
            </Link>
            <Link
              href="/history"
              className="text-sm text-ink-muted hover:text-ink transition-colors"
            >
              Historia
            </Link>
          </nav>
        </header>

        {/* Main content */}
        <main className="flex-1">{children}</main>

        {/* Footer */}
        <footer className="border-t border-border py-6 text-center text-sm text-ink-muted">
          © KIRP 2026 | Narzędzie wspomagające
        </footer>
      </body>
    </html>
  );
}
