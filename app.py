"""
Podnośnik Śrubowy — Aplikacja obliczeniowa
Streamlit frontend | Kod obliczeniowy ukryty w prywatnym API
"""

import streamlit as st
import base64
from api_client import call_api, health_check

# ==============================================================================
# KONFIGURACJA STRONY
# ==============================================================================

st.set_page_config(
    page_title="Podnośnik Śrubowy",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
code, .stCode, [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0c11 0%, #111520 100%);
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] label {
    color: #8899bb !important; font-size: 0.78rem !important;
    letter-spacing: 0.06em; text-transform: uppercase;
}

.stApp { background-color: #0d1117; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important;
     color: #e8edf8 !important; letter-spacing: -0.02em; }
h2 { font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
     color: #c5d0e8 !important; border-bottom: 1px solid #1e2535;
     padding-bottom: 0.4rem; margin-top: 1.5rem !important; }
h3 { color: #7ea8f8 !important; font-size: 0.9rem !important;
     font-weight: 600 !important; letter-spacing: 0.05em; text-transform: uppercase; }

[data-testid="stMetric"] {
    background: #13192b; border: 1px solid #1e2f50;
    border-radius: 8px; padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"] { color: #6a7fa8 !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #7ea8f8 !important; font-size: 1.4rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #1a3a8f, #1565c0) !important;
    color: white !important; border: none !important; border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important; font-weight: 600 !important;
    letter-spacing: 0.05em !important; padding: 0.6rem 2rem !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2040b0, #1976d2) !important;
    transform: translateY(-1px); box-shadow: 0 4px 16px rgba(26,115,232,0.3) !important;
}

.result-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.45rem 0.8rem; border-bottom: 1px solid #151c2e;
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
}
.result-row:hover { background: #131929; }
.result-label { color: #7888a8; }
.result-value { color: #c8d8f8; font-weight: 600; }
.result-unit  { color: #445577; font-size: 0.75rem; margin-left: 4px; }
.status-ok    { color: #4caf84; }
.status-error { color: #ef5350; }
.status-info  { color: #7ea8f8; }
.status-warning { color: #ffb74d; }

.section-card {
    background: #0f1520; border: 1px solid #1a2440;
    border-radius: 10px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.error-banner {
    background: #1a0a0a; border: 1px solid #7f1c1c; border-radius: 8px;
    padding: 0.8rem 1.2rem; color: #ff7070;
    font-family: 'JetBrains Mono', monospace; font-size: 0.83rem; margin-top: 0.5rem;
}
.warn-banner {
    background: #1a1400; border: 1px solid #7f6000; border-radius: 8px;
    padding: 0.8rem 1.2rem; color: #ffc060;
    font-family: 'JetBrains Mono', monospace; font-size: 0.83rem; margin-top: 0.5rem;
}
.api-status-ok  { color: #4caf84; font-size: 0.75rem; }
.api-status-err { color: #ef5350; font-size: 0.75rem; }

/* Instrukcja */
.instr-card {
    background: #0f1a2e; border: 1px solid #1e3060; border-radius: 10px;
    padding: 1.4rem 1.8rem; margin-bottom: 1.2rem;
}
.instr-card h4 {
    color: #7ea8f8 !important; font-size: 0.95rem !important;
    font-weight: 700 !important; letter-spacing: 0.04em;
    text-transform: uppercase; margin-bottom: 0.6rem !important;
    border: none !important;
}
.instr-param {
    display: flex; gap: 1rem; padding: 0.5rem 0;
    border-bottom: 1px solid #131e30; align-items: flex-start;
}
.instr-param:last-child { border-bottom: none; }
.instr-name {
    font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
    color: #a8c0f8; font-weight: 600; min-width: 180px; flex-shrink: 0;
}
.instr-default {
    font-family: 'JetBrains Mono', monospace; font-size: 0.80rem;
    color: #4caf84; background: #0a1f10; border-radius: 4px;
    padding: 0.1rem 0.5rem; white-space: nowrap; flex-shrink: 0;
}
.instr-desc { color: #8898b8; font-size: 0.83rem; line-height: 1.5; }
.tip-box {
    background: #0a1828; border-left: 3px solid #1565c0;
    border-radius: 0 6px 6px 0; padding: 0.7rem 1rem;
    color: #7898c8; font-size: 0.83rem; margin: 0.8rem 0;
}
.warn-box {
    background: #1a1200; border-left: 3px solid #f59e0b;
    border-radius: 0 6px 6px 0; padding: 0.7rem 1rem;
    color: #d4a017; font-size: 0.83rem; margin: 0.8rem 0;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# AUTORYZACJA
# ==============================================================================

def check_password() -> bool:
    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
    <div style='max-width:420px; margin: 6rem auto 0; text-align:center;'>
        <div style='font-size:3rem; margin-bottom:0.5rem;'>⚙️</div>
        <h1 style='margin-bottom:0.2rem;'>Podnośnik Śrubowy</h1>
        <p style='color:#5a6a8a; font-size:0.9rem; margin-bottom:2rem;'>Program obliczeniowy — dostęp chroniony hasłem</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pwd = st.text_input("Hasło dostępu", type="password",
                            label_visibility="collapsed", placeholder="Wpisz hasło...")
        if st.button("Zaloguj się →", use_container_width=True):
            if pwd == st.secrets.get("APP_PASSWORD", ""):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Nieprawidłowe hasło.")
    return False


# ==============================================================================
# HELPERS
# ==============================================================================

def render_logs(logs: list):
    if not logs:
        return
    rows = []
    for item in logs:
        status  = item.get("status", "")
        val_cls = f"status-{status}" if status else "result-value"
        icon    = {"ok": "✔", "error": "✘", "info": "ℹ", "warning": "⚠"}.get(status, "")
        rows.append(
            f'<div class="result-row">'
            f'  <span class="result-label">{item["label"]}</span>'
            f'  <span>'
            f'    <span class="{val_cls}">{icon} {item["value"]}</span>'
            f'    <span class="result-unit">{item.get("unit","")}</span>'
            f'  </span>'
            f'</div>'
        )
    st.markdown('<div class="section-card">' + "".join(rows) + "</div>",
                unsafe_allow_html=True)


def render_alerts(errors: list, warnings: list):
    for e in errors:
        st.markdown(f'<div class="error-banner">✘ {e}</div>', unsafe_allow_html=True)
    for w in warnings:
        st.markdown(f'<div class="warn-banner">⚠ {w}</div>', unsafe_allow_html=True)


def render_wykres(b64_str: str, caption: str = ""):
    if not b64_str:
        st.warning(f"Brak wykresu: {caption}")
        return
    try:
        import io
        img_bytes = base64.b64decode(b64_str)
        st.image(io.BytesIO(img_bytes), caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Błąd renderowania wykresu: {e} | Długość b64: {len(b64_str)} znaków")


def param_row(name: str, default: str, desc: str) -> str:
    return (
        f'<div class="instr-param">'
        f'  <span class="instr-name">{name}</span>'
        f'  <span class="instr-default">{default}</span>'
        f'  <span class="instr-desc">{desc}</span>'
        f'</div>'
    )


# ==============================================================================
# ZAKŁADKA: INSTRUKCJA
# ==============================================================================

def tab_instrukcja():
    st.markdown("## 📖 Instrukcja obsługi")
    st.markdown(
        "Poniżej opisano każdy parametr: co oznacza, skąd pochodzi wartość domyślna "
        "i co należy wpisać dla własnego projektu."
    )

    # ── 1. PARAMETRY EKSPLOATACYJNE ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 1 · Parametry eksploatacyjne")
    st.markdown(
        "Dane z treści zadania projektowego. Każdy student dostaje inne wartości "
        "od prowadzącego — to jedyne parametry które **na pewno** musisz zmienić."
    )

    rows_eksp = "".join([
        param_row("Siła osiowa F [N]", "10 000 N",
                  "Udźwig podnośnika — siła którą śruba musi podnieść. "
                  "<b>Znajdziesz ją w treści zadania.</b> Wpisz w niutonach "
                  "(np. 10 kN = 10 000 N)."),
        param_row("Ramię siły e [mm]", "200 mm",
                  "Odległość między osią śruby a miejscem przyłożenia momentu na kluczu. "
                  "Zazwyczaj zadana przez prowadzącego lub dobrana przez studenta "
                  "na podstawie ergonomii (typowo 150–300 mm)."),
        param_row("Długość robocza śruby [mm]", "1 000 mm",
                  "Skok roboczy podnośnika — o ile milimetrów śruba musi się wysunąć. "
                  "<b>Znajdziesz ją w treści zadania.</b>"),
        param_row("Prędkość śruby n₂ [obr/min]", "200 obr/min",
                  "Wymagana prędkość obrotowa śruby — wynika z zadanej prędkości "
                  "podnoszenia lub jest zadana wprost. "
                  "Zależy od doboru silnika i przełożenia."),
        param_row("Wys. elementu mocującego h [mm]", "130 mm",
                  "Szacunkowa wysokość nakrętki lub obudowy, która wydłuża obliczeniową "
                  "długość wyboczeniową śruby. Jeśli śruba ma 1000 mm, a h = 130 mm, "
                  "program liczy wyboczenie dla L = 1130 mm. "
                  "Przyjmuje się wstępnie ok. 10–15% długości śruby "
                  "i weryfikuje po obliczeniu nakrętki — jeśli wyszło Hn = 55 mm, "
                  "możesz poprawić h na ok. 60–70 mm i przeliczyć ponownie."),
        param_row("Współczynnik wyboczenia µ", "1.0 (obustronny przegub)",
                  "Sposób podparcia śruby na końcach. "
                  "Dla typowego podnośnika śruba jest podparta przegubowo z obu stron → µ = 1.0. "
                  "µ = 0.5 jeśli oba końce są utwierdzone (rzadkie). "
                  "µ = 2.0 jeśli śruba jest wspornikowa (jeden koniec wolny)."),
    ])
    st.markdown(f'<div class="instr-card"><h4>Parametry zadania</h4>{rows_eksp}</div>',
                unsafe_allow_html=True)

    # ── 2. MATERIAŁY ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 2 · Materiały")
    st.markdown(
        "Wybierz gotowy zestaw materiałowy lub wpisz własne wartości. "
        "Wartości Re i E to standardowe dane tablicowe — znajdziesz je "
        "w podręczniku PKM lub normach materiałowych."
    )

    rows_mat = "".join([
        param_row("Stal C45 / Brąz CuSn", "Re=355, E=210 GPa / Re=210, E=130 GPa",
                  "Najczęściej stosowana para dla podnośników — dobra wytrzymałość śruby "
                  "i dobry materiał nakrętki (brąz zmniejsza tarcie i zużycie). "
                  "To domyślny zestaw w projekcie wzorcowym."),
        param_row("Stal 42CrMo4 / Brąz CuSn", "Re=650 MPa",
                  "Stal stopowa o wyższej wytrzymałości. Wybierz jeśli C45 nie przechodzi "
                  "warunków wytrzymałościowych (program pokaże czerwony wskaźnik nz)."),
        param_row("Stal C35 / Poliamid", "Re=305 MPa, pdop=5 MPa",
                  "Lekkie rozwiązanie z tworzywem sztucznym zamiast brązu. "
                  "Niższy nacisk dopuszczalny — nakrętka wychodzi większa."),
        param_row("Współczynnik tarcia µ", "0.13",
                  "Tarcie w gwincie dla pary stal-brąz ze smarowaniem. "
                  "Wartość tablicowa z PKM. Nie zmieniaj jeśli używasz gotowego zestawu."),
        param_row("Nacisk dopuszczalny pdop [MPa]", "14 MPa",
                  "Dopuszczalny nacisk na powierzchnię gwintu dla pary stal-brąz "
                  "przy małych prędkościach (v < 0.05 m/s). Wartość tablicowa z PKM."),
    ])
    st.markdown(f'<div class="instr-card"><h4>Zestawy materiałowe</h4>{rows_mat}</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="tip-box">💡 <b>Skąd wziąć Re i E dla własnego materiału?</b> '
        'Poszukaj w tablicach PKM, normie PN-EN 10083 (stale) lub katalogu producenta. '
        'Re to granica plastyczności [MPa], E to moduł Younga [GPa].</div>',
        unsafe_allow_html=True
    )

    # ── 3. PRZEKŁADNIA ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 3 · Przekładnia pasowa zębata")
    st.markdown(
        "Przekładnia przenosi napęd z silnika elektrycznego na śrubę. "
        "Przełożenie i = z₂/z₁ = n₁/n₂ — dobieram tak, żeby silnik "
        "kręcił się z prędkością katalogową, a śruba z wymaganą n₂."
    )

    rows_przek = "".join([
        param_row("Prędkość silnika n₁ [obr/min]", "710 obr/min",
                  "Prędkość znamionowa silnika elektrycznego. "
                  "Typowe wartości dla silników 50 Hz: 3000 (2-bieg.), 1500 (4-bieg.), "
                  "1000 (6-bieg.), 710 (8-bieg.), 600 (10-bieg.). "
                  "<b>Wybierz silnik tak, żeby i = n₁/n₂ wyszło rozsądne (2–8).</b>"),
        param_row("Zęby koła napędowego z₁", "34",
                  "Liczba zębów na kole zamocowanym na wale silnika (mniejsze koło). "
                  "Dobierana przez studenta — typowo 20–50 zębów. "
                  "Przełożenie i = z₂/z₁ musi być równe n₁/n₂."),
        param_row("Zęby koła napędzanego z₂", "136",
                  "Liczba zębów na kole zamocowanym na wale śruby (większe koło). "
                  "Tu: 136/34 = 4.0 = 710/177.5 ✔. "
                  "<b>Sprawdź czy z₂/z₁ ≈ n₁/n₂ — program poinformuje o błędzie jeśli odchylenie > 5%.</b>"),
        param_row("Podziałka pasa [mm]", "5 mm (HTD 5M)",
                  "Odstęp między zębami pasa. Dostępne pasy zębate: 3M, 5M, 8M, 14M. "
                  "Pas 5M to standardowy wybór dla małych/średnich mocy. "
                  "Większa podziałka = większa przenoszona moc, ale też większe koła."),
        param_row("Szerokość pasa b [mm]", "15 mm",
                  "Szerokość pasa zębatego. Typowe dla 5M: 9, 15, 25 mm. "
                  "Jeśli program wyświetla błąd 'pas niewystarczający' — zwiększ szerokość."),
    ])
    st.markdown(f'<div class="instr-card"><h4>Dobór przełożenia</h4>{rows_przek}</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="tip-box">💡 <b>Jak dobrać z₁ i z₂?</b> '
        'Oblicz wymagane przełożenie: i = n₁/n₂. Np. n₁=710, n₂=200 → i=3.55. '
        'Wybierz z₁ tak żeby z₂ = z₁ × i wyszło całkowite — np. z₁=34 → z₂=120.7 (nie OK), '
        'z₁=36 → z₂=127.8 (nie OK), z₁=40 → z₂=142 (OK). '
        'Małe odchylenia (do 5%) są akceptowalne.</div>',
        unsafe_allow_html=True
    )

    # ── 4. ŁOŻYSKO ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 4 · Łożysko wzdłużne")
    st.markdown(
        "Program oblicza wymaganą nośność dynamiczną C [kN] — na tej podstawie "
        "dobierasz łożysko z katalogu SKF lub podobnego."
    )

    rows_loz = "".join([
        param_row("Żywotność L10h [h]", "10 000 h",
                  "Wymagana trwałość łożyska w godzinach pracy. "
                  "10 000 h to typowa wartość dla maszyn przemysłowych (ok. 5 lat × 2000 h/rok). "
                  "Dla urządzeń sporadycznie używanych można przyjąć 5 000 h."),
        param_row("Kąt działania α [°]", "30°",
                  "Kąt ustawienia rolek/kulek w łożysku skośnym. "
                  "Odpowiada współczynnikowi Y z katalogu. "
                  "Dla łożysk oporowych: α=90° (Y=0.5). "
                  "Dla łożysk skośnych kulkowych: α=15°, 25°, 30°, 40°. "
                  "<b>Sprawdź w katalogu SKF dla wybranego łożyska.</b>"),
    ])
    st.markdown(f'<div class="instr-card"><h4>Trwałość łożyska</h4>{rows_loz}</div>',
                unsafe_allow_html=True)

    # ── 5. WAŁY ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 5 · Analiza wałów")
    st.markdown(
        "To jedyna sekcja gdzie student wprowadza **własną geometrię** — "
        "program sprawdza czy zaprojektowane wały wytrzymają obliczone obciążenia. "
        "Domyślne wartości to projekt wzorcowy — zastąp je własnym projektem."
    )

    st.markdown(
        '<div class="warn-box">⚠️ <b>Ważne:</b> Program nie projektuje wałów — on je sprawdza. '
        'Najpierw narysuj wał (podcięcia pod łożyska, kliny, uszczelnienia), '
        'wyznacz długości i średnice poszczególnych stopni, a dopiero potem wpisz je tutaj.</div>',
        unsafe_allow_html=True
    )

    rows_wal = "".join([
        param_row("Segmenty wału", "własny projekt",
                  "Wpisz każdy stopień wału jako parę: długość [mm] × średnica [mm]. "
                  "Kolejność od lewej do prawej zgodnie z rysunkiem złożeniowym. "
                  "Minimalna liczba segmentów: 2 (czop + część robocza)."),
        param_row("Lokalizacja podpór A i B", "własny projekt",
                  "Gdzie siedzą łożyska — środek łożyska na osi wału. "
                  "<b>Seg</b> = numer segmentu (1 = pierwszy od lewej). "
                  "<b>Offset</b> = odległość środka łożyska od początku tego segmentu [mm]."),
        param_row("Lokalizacja koła pasowego", "własny projekt",
                  "Środek koła pasowego na wale — taki sam format jak podpory. "
                  "To tu działa siła poprzeczna od pasa."),
        param_row("Moment skręcający Ms", "automatycznie",
                  "Program oblicza Ms z wyników sekcji Śruba i Przekładnia — "
                  "nie musisz tego wpisywać."),
        param_row("Siła poprzeczna Ft", "automatycznie",
                  "Siła obwodowa od pasa (Fo1 / Fo2 z wyników przekładni). "
                  "Mnożona wewnętrznie przez wsp. naciągu 2.5 — "
                  "celowo zawyżony żeby projekt był po bezpiecznej stronie."),
    ])
    st.markdown(f'<div class="instr-card"><h4>Parametry wału</h4>{rows_wal}</div>',
                unsafe_allow_html=True)

    # Przykład z rysunkiem
    st.markdown("#### Przykład — jak wpisać lokalizacje")
    st.markdown(
        '<div class="tip-box">'
        '💡 <b>Jak czytać ten schemat:</b> każdy prostokąt to jeden segment wału. '
        'Numeracja od lewej (1, 2, 3...). Offset = odległość od lewej krawędzi segmentu.'
        '</div>',
        unsafe_allow_html=True
    )
    st.code(
        "Rysunek wału (widok z boku):\n"
        "\n"
        "  Seg 1          Seg 2              Seg 3          Seg 4\n"
        "  Ø25, L=35      Ø30, L=20          Ø22, L=100     Ø25, L=35\n"
        " ┌─────────┐┌────────────┐┌──────────────────────┐┌─────────┐\n"
        " │         ││            ││                       ││         │\n"
        " └─────────┘└────────────┘└──────────────────────┘└─────────┘\n"
        "       ↑                           ↑                    ↑\n"
        "   Łożysko A                  Koło pasowe           Łożysko B\n"
        "  (środek = 17mm               (środek = 50mm       (środek = 17mm\n"
        "   od lewej seg.1)              od lewej seg.3)      od lewej seg.4)\n"
        "\n"
        "Wpisz:\n"
        "  Łożysko A:   Seg = 1,  Offset = 17\n"
        "  Łożysko B:   Seg = 4,  Offset = 17\n"
        "  Koło pasowe: Seg = 3,  Offset = 50\n"
        "\n"
        "Segmenty:\n"
        "  Seg 1: dług=35,  śred=25\n"
        "  Seg 2: dług=20,  śred=30   ← np. podcięcie pod pierścień ustalający\n"
        "  Seg 3: dług=100, śred=22\n"
        "  Seg 4: dług=35,  śred=25",
        language=None
    )

    # ── 6. INTERPRETACJA WYNIKÓW ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 6 · Jak interpretować wyniki")

    st.markdown("""
**Kolory w tabeli wyników:**
- ✔ **zielony** — warunek spełniony
- ✘ **czerwony** — warunek niespełniony → zmień parametry (większa średnica, inny materiał)
- ℹ **niebieski** — wartość informacyjna (nie ocenia spełnienia warunku)

**Najważniejsze wskaźniki:**

| Wskaźnik | Co znaczy | Wymaganie |
|---|---|---|
| **nz** | Współczynnik bezp. śruby (kr / σ_HMH) | ≥ 1.5 |
| **sf** | Współczynnik bezp. wału (Re / σ_max) | ≥ 1.5 |
| **Samohamowność** | Czy ładunek nie opadnie sam | TAK (ρ' > γ) |
| **Ugięcie wału** | Max ugięcie vs. L/3000 | ≤ limit |
| **Kąt w łożysku** | Kąt ugięcia osi wału | ≤ 0.001 rad |

**Co zrobić gdy warunek nie jest spełniony?**
- Śruba: wybierz wyższy zestaw materiałowy (C45 → 42CrMo4) lub zmniejsz siłę
- Wał: zwiększ średnicę w miejscu gdzie jest największe naprężenie
- Przekładnia: zwiększ szerokość pasa lub zmień podziałkę na większą
""")

    st.markdown(
        '<div class="tip-box">💡 <b>Co program sprawdza dla wału?</b><br>'
        '(1) Naprężenie HMH — maksymalne naprężenie zredukowane vs. Re materiału (wymagany sf ≥ 1.5)<br>'
        '(2) Ugięcie — max ugięcie vs. L/3000 (warunek sztywności)<br>'
        '(3) Kąty ugięcia w łożyskach — wymagane ≤ 0.001 rad dla łożysk tocznych<br>'
        '(4) Dobór wpustu pryzmatycznego — automatycznie na podstawie średnicy w miejscu koła pasowego</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="warn-box">⚠️ <b>Siły obliczane automatycznie:</b> '
        'Program sam pobiera moment skręcający i siłę od pasa z wyników sekcji Śruba i Przekładnia — '
        'nie musisz ich wpisywać. Siła jest mnożona przez wsp. 2.5 (konserwatywny szacunek naciągu pasa) '
        'który celowo "wybacza" niedokładności w geometrii wału.</div>',
        unsafe_allow_html=True
    )


# ==============================================================================
# SIDEBAR
# ==============================================================================

def sidebar_inputs() -> dict:
    st.sidebar.markdown("## ⚙️ Podnośnik Śrubowy")
    st.sidebar.markdown("---")

    if st.sidebar.button("🔌 Sprawdź połączenie z API", use_container_width=True):
        ok = health_check()
        if ok:
            st.sidebar.markdown('<span class="api-status-ok">✔ API działa poprawnie</span>',
                                unsafe_allow_html=True)
        else:
            st.sidebar.markdown('<span class="api-status-err">✘ API niedostępne</span>',
                                unsafe_allow_html=True)

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 1 · Parametry eksploatacyjne")
    st.sidebar.caption("📌 Dane z treści zadania — zmień na swoje wartości")
    sila_F        = st.sidebar.number_input("Siła osiowa F [N]",          100.0, 500000.0, 10000.0, 500.0)
    ramie_sily    = st.sidebar.number_input("Ramię siły e [mm]",            0.0,   2000.0,   200.0,  10.0)
    dlugosc_sruby = st.sidebar.number_input("Długość robocza śruby [mm]",  50.0,  10000.0,  1000.0,  50.0)
    n_sruby       = st.sidebar.number_input("Prędkość śruby n₂ [obr/min]", 1.0,   2000.0,   200.0,  10.0)
    h_element     = st.sidebar.number_input("Wys. elementu mocującego h [mm]", 10.0, 500.0,  130.0,   5.0)
    st.sidebar.caption("h ≈ wys. nakrętki — wpisz 130 wstępnie, po obliczeniach popraw na Hn+10 mm")
    alfa = st.sidebar.selectbox(
        "Współczynnik wyboczenia µ",
        [0.5, 0.7, 1.0, 2.0], index=2,
        format_func=lambda v: {
            0.5: "0.5 – obustronne utwierdzenie",
            0.7: "0.7 – utwierdzenie + przegub",
            1.0: "1.0 – obustronny przegub ← typowy",
            2.0: "2.0 – wspornik"
        }[v]
    )

    st.sidebar.markdown("### 2 · Materiały")
    st.sidebar.caption("📌 Zmień jeśli prowadzący podał inny materiał")
    mat_preset = st.sidebar.selectbox("Zestaw materiałowy", [
        "Stal C45 / Brąz CuSn (domyślne)",
        "Stal 42CrMo4 / Brąz CuSn",
        "Stal C35 / Poliamid",
        "Własne"
    ])
    presets = {
        "Stal C45 / Brąz CuSn (domyślne)": (355, 210, 210, 130, 0.13, 14),
        "Stal 42CrMo4 / Brąz CuSn":        (650, 210, 210, 130, 0.12, 16),
        "Stal C35 / Poliamid":              (305, 210,  70,   3, 0.25,  5),
    }
    if mat_preset in presets:
        Re_s, E_s, Re_n, E_n, mi, pdop = presets[mat_preset]
    else:
        Re_s  = st.sidebar.number_input("Re śruby [MPa]",      100.0, 2000.0, 355.0)
        E_s   = st.sidebar.number_input("E śruby [GPa]",        50.0,  300.0, 210.0)
        Re_n  = st.sidebar.number_input("Re nakrętki [MPa]",    30.0, 1000.0, 210.0)
        E_n   = st.sidebar.number_input("E nakrętki [GPa]",      1.0,  300.0, 130.0)
        mi    = st.sidebar.number_input("Wsp. tarcia µ",        0.01,    0.5,  0.13, 0.01)
        pdop  = st.sidebar.number_input("Nacisk pdop [MPa]",     1.0,   50.0,  14.0)

    st.sidebar.markdown("### 3 · Przekładnia pasowa")
    st.sidebar.caption("📌 Dobierz z₁, z₂ tak aby z₂/z₁ = n₁/n₂")
    n1        = st.sidebar.number_input("Prędkość silnika n₁ [obr/min]", 100.0, 3000.0, 710.0, 10.0)
    z1        = st.sidebar.number_input("Zęby koła napędowego z₁", 6, 200, 34)
    z2        = st.sidebar.number_input("Zęby koła napędzanego z₂", 6, 500, 136)
    i_check   = z2 / z1 if z1 > 0 else 0
    i_wymagane = n1 / n_sruby if n_sruby > 0 else 0
    st.sidebar.caption(f"i = z₂/z₁ = {i_check:.3f} | wymagane n₁/n₂ = {i_wymagane:.3f}")
    podzialka = st.sidebar.selectbox("Podziałka pasa [mm]", [3, 5, 8, 14], index=1)
    szer_pas  = st.sidebar.number_input("Szerokość pasa b [mm]", 5.0, 100.0, 15.0, 5.0)

    st.sidebar.markdown("### 4 · Łożysko wzdłużne")
    loz_Lh  = st.sidebar.number_input("Żywotność L10h [h]", 500.0, 100000.0, 10000.0, 500.0)
    loz_kat = st.sidebar.selectbox("Kąt działania α [°]", [15, 25, 30, 40, 45], index=2)
    Y_map   = {15: 1.0, 25: 0.78, 30: 0.66, 40: 0.55, 45: 0.50}
    loz_Y   = Y_map[loz_kat]
    st.sidebar.caption(f"Współczynnik Y = {loz_Y} (z katalogu SKF)")

    return {
        "sila_F": sila_F, "ramie_sily": ramie_sily,
        "dlugosc_sruby": dlugosc_sruby, "n_sruby": n_sruby,
        "h_element": h_element, "alfa": float(alfa),
        "Re_sruby": Re_s, "E_sruby": E_s,
        "Re_nakretki": Re_n, "E_nakretki": E_n,
        "mi": mi, "pdop": pdop,
        "n1": n1, "z1": int(z1), "z2": int(z2),
        "podzialka": float(podzialka), "szerokosc": szer_pas,
        "hz": 2.1, "T_rob": 650.0, "m_metr": 0.360,
        "loz_Lh": loz_Lh, "loz_Y": loz_Y,
    }


# ==============================================================================
# SEKCJE WYNIKÓW
# ==============================================================================

def section_sruba(wyniki: dict):
    st.markdown("## 🔩 Śruba i nakrętka")
    w = wyniki.get("sruba", {})
    if "_error" in w:
        st.error(w["_error"]); return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gwint", w.get("gwint", "—"))
    col2.metric("d nominalna", f"{w.get('d_nom','—')} mm")
    col3.metric("Skok P", f"{w.get('P','—')} mm")
    col4.metric("Ms", f"{w.get('Ms_Nm',0):.1f} Nm")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("σ_HMH", f"{w.get('sigma_z',0):.1f} MPa")
    col6.metric("nz (bezp.)", f"{w.get('nz',0):.2f}")
    col7.metric("Nakrętka Dz×Hn", f"{w.get('Dz','?')}×{w.get('Hn','?')} mm")
    col8.metric("v podnosz.", f"{w.get('v_mm_s',0):.1f} mm/s")

    with st.expander("📋 Szczegółowe kroki obliczeniowe"):
        render_logs(w.get("logs", []))
    render_alerts(w.get("errors", []), w.get("warnings", []))


def section_przekladnia(wyniki: dict):
    st.markdown("## ⚙️ Przekładnia pasowa zębata")
    w = wyniki.get("przekladnia", {})
    if "_error" in w:
        st.error(w["_error"]); return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Przełożenie i", f"{w.get('i', 0):.4f}")
    col2.metric("Długość pasa L", f"{w.get('L_pas', 0):.0f} mm")
    col3.metric("Odległość osi", f"{w.get('a_wl', 0):.1f} mm")
    col4.metric("Fo₁ (silnik)", f"{w.get('Fo1', 0):.1f} N")

    with st.expander("📋 Szczegółowe kroki obliczeniowe"):
        render_logs(w.get("logs", []))
    render_alerts(w.get("errors", []), w.get("warnings", []))


def section_wal(wyniki: dict, klucz: str, tytul: str):
    st.markdown(f"## 🔧 {tytul}")
    w = wyniki.get(klucz, {})
    if "_error" in w:
        st.error(w["_error"]); return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Max σ_HMH", f"{w.get('max_sigma',0):.1f} MPa")
    col2.metric("sf (bezp.)",  f"{w.get('sf',0):.2f}")
    col3.metric("Max ugięcie", f"{w.get('max_ug',0):.4f} mm")
    col4.metric("Limit ugięcia", f"{w.get('lim_ug',0):.4f} mm")

    if w.get("wykres_b64"):
        render_wykres(w.get("wykres_b64", ""), tytul)

    with st.expander("📋 Szczegółowe kroki obliczeniowe"):
        render_logs(w.get("logs", []))
    render_alerts(w.get("errors", []), w.get("warnings", []))


def section_lozysko(wyniki: dict):
    st.markdown("## 🔵 Łożyskowanie")
    w = wyniki.get("lozysko", {})
    if "_error" in w:
        st.error(w["_error"]); return

    col1, col2 = st.columns(2)
    col1.metric("Wymagana nośność C", f"{w.get('C_kN', 0):.2f} kN")
    col2.metric("Żywotność L10h", f"{w.get('loz_Lh', 0):.0f} h")

    with st.expander("📋 Szczegółowe kroki obliczeniowe"):
        render_logs(w.get("logs", []))
    render_alerts(w.get("errors", []), w.get("warnings", []))


# ==============================================================================
# KONFIGURACJA WAŁÓW
# ==============================================================================

def get_wal_config(numer: int, seg_default, loc_defaults) -> dict:
    # Klucz session_state dla liczby segmentów tego wału
    key_n = f"w{numer}_n_seg"
    if key_n not in st.session_state:
        st.session_state[key_n] = len(seg_default)

    with st.expander(f"⚙️ Konfiguracja Wału {numer} — kliknij aby rozwinąć i wpisać własne wymiary",
                     expanded=False):

        st.caption(
            "⚠️ Domyślne wartości to projekt wzorcowy — zastąp je geometrią swojego wału. "
            "Moment skręcający i siłę poprzeczną program oblicza automatycznie."
        )

        st.markdown("**Segmenty wału** — każdy stopień jako długość × średnica [mm]")
        st.caption("Numeruj od lewej do prawej zgodnie z rysunkiem złożeniowym")

        # Przyciski + / - do zmiany liczby segmentów
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 6])
        with btn_col1:
            if st.button("＋ Dodaj segment", key=f"w{numer}_add"):
                st.session_state[key_n] = min(st.session_state[key_n] + 1, 10)
        with btn_col2:
            if st.button("－ Usuń segment", key=f"w{numer}_rem"):
                st.session_state[key_n] = max(st.session_state[key_n] - 1, 1)

        n_seg = st.session_state[key_n]
        segmenty = []
        for i in range(n_seg):
            # Domyślne wartości: z seg_default jeśli istnieje, inaczej ostatni znany
            if i < len(seg_default):
                l_def, d_def = seg_default[i]
            else:
                l_def, d_def = seg_default[-1]
            cs1, cs2 = st.columns(2)
            l = cs1.number_input(f"Seg {i+1} — dług. [mm]", 1.0, 2000.0, float(l_def), key=f"w{numer}_sl{i}")
            d = cs2.number_input(f"Seg {i+1} — śred. [mm]", 1.0,  200.0, float(d_def), key=f"w{numer}_sd{i}")
            segmenty.append({"length": l, "diameter": d})

        st.markdown("**Lokalizacje podpór i koła pasowego**")
        st.caption(
            "Seg = numer segmentu (1 = pierwszy od lewej) · "
            "Offset = odległość od początku tego segmentu [mm]"
        )
        la1, la2, lb1, lb2, lf1, lf2 = st.columns(6)
        sA = int(la1.number_input("Łoż.A — seg",    1, 10, loc_defaults[0][0], key=f"w{numer}_sA"))
        oA =     la2.number_input("Łoż.A — offset", 0.0, 1000.0, loc_defaults[0][1], key=f"w{numer}_oA")
        sB = int(lb1.number_input("Łoż.B — seg",    1, 10, loc_defaults[1][0], key=f"w{numer}_sB"))
        oB =     lb2.number_input("Łoż.B — offset", 0.0, 1000.0, loc_defaults[1][1], key=f"w{numer}_oB")
        sF = int(lf1.number_input("Koło — seg",     1, 10, loc_defaults[2][0], key=f"w{numer}_sF"))
        oF =     lf2.number_input("Koło — offset",  0.0, 1000.0, loc_defaults[2][1], key=f"w{numer}_oF")

    return {
        "nazwa": f"Wał {numer}: {'Silnik (Napędowy)' if numer == 1 else 'Śruba (Napędzany)'}",
        "segmenty": segmenty,
        "loc_support_A": {"seg_idx": sA - 1, "offset": oA},
        "loc_support_B": {"seg_idx": sB - 1, "offset": oB},
        "loc_load":      {"seg_idx": sF - 1, "offset": oF},
    }


# ==============================================================================
# ZAKŁADKA: OBLICZENIA
# ==============================================================================

def tab_obliczenia(inp: dict):
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h1>⚙️ Podnośnik Śrubowy</h1>
        <p style='color:#4a5a7a; font-size:0.88rem; margin-top:-0.5rem;'>
            Program obliczeniowy · v2.0
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Wybierz zakres obliczeń")
    col_cb = st.columns(5)
    run_sruba = col_cb[0].checkbox("Śruba + nakrętka",  True)
    run_przek = col_cb[1].checkbox("Przekładnia pasowa", True)
    run_waly  = col_cb[2].checkbox("Wały napędowe",     True)
    run_loz   = col_cb[3].checkbox("Łożysko",           True)

    st.markdown("---")

    wal1_cfg = wal2_cfg = None
    if run_waly:
        st.markdown("### Konfiguracja wałów")
        wal1_cfg = get_wal_config(
            numer=1,
            seg_default=[(30, 28), (120, 20)],
            loc_defaults=[(1, 11.0), (1, 109.0), (1, 60.0)],
        )
        wal2_cfg = get_wal_config(
            numer=2,
            seg_default=[(51, 20), (49.108, 22), (99.785, 24), (20.108, 22)],
            loc_defaults=[(1, 42.108), (3, 7.0), (2, 49.892)],
        )
        st.markdown("---")

    col_btn = st.columns([2, 1, 2])
    with col_btn[1]:
        oblicz = st.button("▶ OBLICZ", use_container_width=True)

    if not oblicz:
        st.markdown("""
        <div style='text-align:center; margin-top:3rem; color:#2a3a5a;'>
            <div style='font-size:4rem;'>⚙️</div>
            <p style='font-size:1rem;'>
                Uzupełnij parametry w panelu bocznym i kliknij <strong>OBLICZ</strong><br>
                <span style='font-size:0.85rem;'>Nie wiesz co wpisać? Zajrzyj do zakładki <b>📖 Instrukcja</b></span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    with st.spinner("Trwa obliczanie... ⏳"):
        material = {
            "Re_sruby": inp["Re_sruby"], "E_sruby": inp["E_sruby"],
            "Re_nakretki": inp["Re_nakretki"], "E_nakretki": inp["E_nakretki"],
            "mi": inp["mi"], "pdop": inp["pdop"],
        }
        payload = {
            "sruba": {
                "sila_F": inp["sila_F"], "ramie_sily": inp["ramie_sily"],
                "dlugosc_sruby": inp["dlugosc_sruby"], "n_sruby": inp["n_sruby"],
                "h_element": inp["h_element"], "alfa": inp["alfa"],
                "material": material,
            }
        }
        if run_przek:
            payload["przekladnia"] = {
                "n1": inp["n1"], "n2": inp["n_sruby"],
                "z1": inp["z1"], "z2": inp["z2"],
                "podzialka": inp["podzialka"], "szerokosc": inp["szerokosc"],
                "hz": inp["hz"], "T_rob": inp["T_rob"], "m_metr": inp["m_metr"],
                "Ms_Nm": 34.0, "Pm_kW": 1.1,
            }
        if run_waly and wal1_cfg:
            payload["wal1"] = {**wal1_cfg, "material": material}
        if run_waly and wal2_cfg:
            payload["wal2"] = {**wal2_cfg, "material": material}
        if run_loz:
            payload["lozysko"] = {
                "Fw_kN": inp["sila_F"] / 1000,
                "Lh": inp["loz_Lh"],
                "Y": inp["loz_Y"],
                "n_sruby": inp["n_sruby"],
            }
        wyniki = call_api("pelny", payload)

    if "_error" in wyniki:
        st.error(f"❌ {wyniki['_error']}")
        st.info("Upewnij się, że API jest uruchomione i poprawnie skonfigurowane w secrets.toml")
        return

    if run_sruba:  section_sruba(wyniki)
    if run_przek:  section_przekladnia(wyniki)
    if run_waly:
        section_wal(wyniki, "wal1", "Wał 1: Silnik (Napędowy)")
        section_wal(wyniki, "wal2", "Wał 2: Śruba (Napędzany)")
    if run_loz:    section_lozysko(wyniki)

    all_ok = all(
        wyniki.get(k, {}).get("ok", True)
        for k in ["sruba", "przekladnia", "wal1", "wal2", "lozysko"]
        if k in wyniki
    )
    if all_ok:
        st.success("✅ Wszystkie warunki wytrzymałościowe i sztywnościowe spełnione.")
    else:
        st.warning("⚠️ Niektóre warunki nie zostały spełnione — sprawdź czerwone wskaźniki powyżej.")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    if not check_password():
        return

    inp = sidebar_inputs()

    tab_obl, tab_instr = st.tabs(["🔢 Obliczenia", "📖 Instrukcja"])

    with tab_obl:
        tab_obliczenia(inp)

    with tab_instr:
        tab_instrukcja()


if __name__ == "__main__":
    main()
