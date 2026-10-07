# ADR-004: Frontend — styl i design system

**Data:** 2026-05-04  
**Status:** ACCEPTED

## Decyzja

- **Styl:** Apple-like — czysty, minimalistyczny, dużo whitespace, typografia na pierwszym planie
- **Kolory:** Granat (#1B2A4A lub zbliżony) + Biel (#FFFFFF) + opcjonalnie Czarny (#0A0A0A)
- **Accent:** złoto lub jasny granat dla hover/CTA (do ustalenia)
- **Typografia:** Inter lub SF Pro (system font na macOS) — czytelna, prosta
- **Komponenty:** Tailwind CSS + shadcn/ui (minimalny, bez ciężkich bibliotek)
- **Beta badge:** widoczny, subtelny — pasek lub chip w nagłówku

## Uzasadnienie

- Radcowie prawni = środowisko prawnicze, konserwatywne estetycznie — granat/biel = zaufanie i powaga
- Apple style = nowoczesność + czytelność + profesjonalizm bez ostentacji
- Tailwind + shadcn = szybki development, łatwa customizacja kolorystyki

## Paleta kolorów (wstępna)

```css
--color-primary: #1B2A4A;    /* granat KIRP */
--color-primary-light: #2E4272;
--color-surface: #FFFFFF;
--color-surface-muted: #F8F9FB;
--color-text: #0A0A0A;
--color-text-muted: #6B7280;
--color-accent: #C9A84C;     /* złoto - do weryfikacji z Adamem */
--color-border: #E5E7EB;
--color-beta: #F59E0B;       /* amber dla beta badge */
```

## Do weryfikacji

- Czy KIRP ma oficjalną paletę? Jeśli tak — dopasować
- Accent: złoto vs. jasny błękit vs. neutralny szary
