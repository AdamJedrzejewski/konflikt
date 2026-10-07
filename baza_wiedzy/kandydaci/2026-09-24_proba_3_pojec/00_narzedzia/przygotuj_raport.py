from pathlib import Path
trial=Path(__file__).resolve().parent.parent
p=trial/'00_narzedzia/karty.py'
s=p.read_text(encoding='utf-8')
a=s.index("    out += ['', '## Kontrola fikcyjnych fragmentów'")
b=s.index("    (trial / (name + '.md'))",a)
s=s[:a]+'''    out += ['', '## Odbiór Astry', '']
    review = d.get('review', {})
    for change in review.get('changes', []):
        out.append('- ' + change)
    out += ['', review.get('limits', ''), '', 'Wyniki ćwiczeń kontrolnych i zapis samooceny wykonawcy pozostają w pliku JSON. Bieżący stan odbioru określa powyższy opis i raport próby.', '']
'''+s[b:]
p.write_text(s,encoding='utf-8')
p=trial/'00_narzedzia/podsumuj.py'
s=p.read_text(encoding='utf-8-sig')
s=s.replace('- Osoba najbliższa: zakres i ewentualne poprawki są opisane w karcie oraz w polu review jej pliku JSON. Brak materiału z innych dziedzin pozostaje luką, a nie podstawą dopisania definicji.', '- Osoba najbliższa: Luna samodzielnie wskazała rozbieżność § 1/§ 11 w odesłaniu przytoczonym w wyborze orzeczeń. Zachowano ją do rozstrzygnięcia, bez poprawiania źródła. Odróżniono pogląd komentatora o bliskoznaczności relacji od definicji KERP. Brak materiału z innych instytucji prawa pozostaje luką.')
s=s.replace('Automatyczna kontrola potwierdziła zgodność wszystkich przytoczeń z podanymi wierszami,', 'Automatyczna kontrola potwierdziła zgodność wszystkich przytoczeń z podanymi wierszami (z ujednoliceniem wyłącznie konwencji końca wiersza CRLF/LF),')
p.write_text(s,encoding='utf-8')
p=trial/'00_narzedzia/sprawdz_karty.py'
s=p.read_text(encoding='utf-8-sig').replace("['01_klient','02_sprawa']", "['01_klient','02_sprawa','03_osoba_najblizsza']")
p.write_text(s,encoding='utf-8')
