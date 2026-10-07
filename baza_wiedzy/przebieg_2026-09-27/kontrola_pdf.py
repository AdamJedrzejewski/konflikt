from pathlib import Path
import fitz
root = Path(__file__).resolve().parents[2]
doc = fitz.open(root / 'Konflikt interesow_16-08-2025 + PS.pdf')
for i, page in enumerate(doc):
    if i == 24 or 'ustanej' in page.get_text() or 'szczególnej formy' in page.get_text():
        target = Path(__file__).parent / f'kontrola_pdf_{i+1}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(target)
        print(target)
