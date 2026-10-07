import Link from "next/link";

const steps = [
  {
    number: "1",
    title: "Opisz stan faktyczny",
    description: "Wprowadź opis sprawy i podmiotów zaangażowanych",
  },
  {
    number: "2",
    title: "System przeanalizuje",
    description: "Automatyczna ekstrakcja podmiotów, ról i relacji",
  },
  {
    number: "3",
    title: "Oceń wynik",
    description: "Otrzymaj klasyfikację ryzyka z uzasadnieniem prawnym",
  },
];

export default function HomePage() {
  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      {/* Hero */}
      <section className="text-center mb-16">
        <h1 className="text-3xl font-bold text-ink mb-3">
          Badanie konfliktu interesów
        </h1>
        <p className="text-lg text-ink-muted mb-8">
          Narzędzie wspomagające dla radców prawnych
        </p>
        <Link
          href="/analyze"
          className="inline-flex items-center px-6 py-3 bg-primary text-white font-medium rounded-lg hover:bg-primary-light transition-colors"
        >
          Rozpocznij analizę
        </Link>
      </section>

      {/* How it works */}
      <section>
        <h2 className="text-lg font-semibold text-ink mb-6 text-center">
          Jak to działa
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {steps.map((step) => (
            <div
              key={step.number}
              className="bg-surface rounded-xl border border-border p-6 text-center"
            >
              <div className="w-10 h-10 bg-primary text-white rounded-full flex items-center justify-center text-sm font-bold mx-auto mb-4">
                {step.number}
              </div>
              <h3 className="font-medium text-ink mb-2">{step.title}</h3>
              <p className="text-sm text-ink-muted">{step.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
