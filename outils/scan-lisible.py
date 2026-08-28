import io, sys, numpy as np, cv2, pymupdf
from PIL import Image


def smoothstep(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

def background(gray, scale=0.03):
    """Estimation de l'eclairage / du papier : fermeture morphologique + flou."""
    h, w = gray.shape
    k = max(25, int(min(h, w) * scale) | 1)
    small = cv2.resize(gray, (w // 4, h // 4), interpolation=cv2.INTER_AREA)
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k // 4 | 1, k // 4 | 1))
    bg = cv2.morphologyEx(small, cv2.MORPH_CLOSE, ker)
    bg = cv2.dilate(bg, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    bg = cv2.GaussianBlur(bg, (0, 0), 15)
    return cv2.resize(bg, (w, h), interpolation=cv2.INTER_LINEAR)

def enhance(rgb):
    img = rgb.astype(np.float32)
    # 1. Aplanissement de l'eclairage, canal par canal -> papier blanc, encre intacte
    ff = np.empty_like(img)
    for c in range(3):
        bg = background(img[:, :, c])
        ff[:, :, c] = img[:, :, c] / np.maximum(bg, 1e-3)
    ff = np.clip(ff, 0, 1.25)

    L = ff.max(2) * 0.5 + ff.min(2) * 0.5          # luminosite
    chroma = ff.max(2) - ff.min(2)                  # couleur (cachets)

    # 2a. Lissage du grain du papier sans toucher aux traits (filtre bilateral)
    L8 = np.clip(L * 200.0, 0, 255).astype(np.uint8)
    L = cv2.bilateralFilter(L8, 7, 45, 7).astype(np.float32) / 200.0

    # 2b. Second passage local : efface les ombres de pliure et les salissures du papier
    Ln = np.clip(L / np.maximum(background(L, 0.018), 1e-3), 0, 1.25)

    # 2c. Points noir/blanc adaptes a la page (le scan est tres pale)
    lo = float(np.clip(np.percentile(Ln, 1.0), 0.55, 0.90))
    hi = float(np.clip(np.percentile(Ln, 60.0), 0.93, 1.02))
    strong = np.clip((Ln - lo) / (hi - lo), 0, 1) ** 1.25         # texte -> noir franc
    glo = lo - 0.28
    gentle = np.clip((L - glo) / ((hi + 0.03) - glo), 0, 1) ** 1.5   # cachets : plus denses
    alpha = smoothstep(chroma, 0.05, 0.16)          # 1 = pixel colore
    Lout = (1 - alpha) * strong + alpha * gentle

    # 2d. Fond papier ramene au blanc franc (les taches tres pales disparaissent)
    ink = 1.0 - Lout
    Lout = 1.0 - ink * smoothstep(ink, 0.06, 0.22)

    # 3. Recomposition couleur : on garde la teinte, on renforce la saturation
    # saturation forte sur les cachets, papier ramene au neutre (pas de voile rose)
    sat = (0.45 + 1.35 * alpha)[:, :, None]
    out = Lout[:, :, None] + sat * (ff - L[:, :, None])
    out = np.clip(out, 0, 1) * 255.0

    # 4. Accentuation legere pour l'impression
    blur = cv2.GaussianBlur(out, (0, 0), 1.6)
    out = np.clip(out + 0.45 * (out - blur), 0, 255)
    return out.astype(np.uint8)

def main(src, out_pdf, pages=None, preview=None):
    doc = pymupdf.open(src)
    new = pymupdf.open()
    idx = pages if pages is not None else range(doc.page_count)
    for i in idx:
        page = doc[i]
        info = doc.extract_image(page.get_images(full=True)[0][0])
        rgb = np.asarray(Image.open(io.BytesIO(info['image'])).convert('RGB'))
        res = enhance(rgb)
        buf = io.BytesIO()
        Image.fromarray(res).save(buf, 'JPEG', quality=88, optimize=True, subsampling=0)
        if preview:
            Image.fromarray(res).save(f'{preview}/p{i:02d}.jpg', quality=88)
        if out_pdf:
            p = new.new_page(width=page.rect.width, height=page.rect.height)
            p.insert_image(p.rect, stream=buf.getvalue())
        print('page', i + 1, 'ok', len(buf.getvalue()) // 1024, 'Ko', flush=True)
    if out_pdf:
        new.save(out_pdf, deflate=True, garbage=4)
        print('->', out_pdf)

USAGE = """Nettoyage d'un scan photo pour l'impression (RA-QDMS).

    python3 outils/scan-lisible.py scan.pdf scan-lisible.pdf

Aplanit l'eclairage de la photo, ramene le papier au blanc et le texte au noir,
tout en preservant les cachets et signatures en couleur (ANACM, Royal Air).
Le contenu n'est ni recadre, ni redresse, ni retouche.
Dependances : pip install pymupdf pillow numpy opencv-python-headless
"""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
