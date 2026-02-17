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
.main .block-container { padding-top: 4.5rem; padding-bottom: 2rem; }

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
        return
    try:
        import io
        img_bytes = base64.b64decode(b64_str)
        st.image(io.BytesIO(img_bytes), caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Błąd renderowania wykresu: {e}")


def param_row(name: str, default: str, desc: str) -> str:
    return (
        f'<div class="instr-param">'
        f'  <span class="instr-name">{name}</span>'
        f'  <span class="instr-default">{default}</span>'
        f'  <span class="instr-desc">{desc}</span>'
        f'</div>'
    )


# ==============================================================================
# ZAKŁADKA: INSTRUKCJA (ZAKTUALIZOWANA)
# ==============================================================================

def tab_instrukcja():
    st.markdown("## 📖 Instrukcja Obsługi Projektu")
    
    st.info(
        "👋 Cześć! Ta aplikacja to Twój **weryfikator**. Ona nie wymyśli projektu za Ciebie, "
        "ale sprawdzi, czy to, co zaprojektowałeś (dobrałeś), nie rozpadnie się pod obciążeniem. "
        "Poniżej znajdziesz wyjaśnienie, skąd brać dane i jak czytać wyniki."
    )

    # ── 1. DANE WEJŚCIOWE ───────────────────────────────────────────────────
    st.markdown("### 1️⃣ Panel Boczny: Co tu wpisać?")
    st.markdown(
        "Panel boczny to Twoje „Założenia Projektowe”. Dzielą się na te, które **musisz** wziąć z zadania, "
        "i te, które **dobierasz** sam."
    )

    # Parametry Eksploatacyjne
    rows_eksp = "".join([
        param_row("Siła osiowa F [N]", "ZADANIE",
                  "Ciężar, który podnośnik ma unieść. <b>To wartość święta – bierzesz ją z kartki od prowadzącego.</b> "
                  "Pamiętaj: 1 kN = 1000 N."),
        param_row("Ramię siły e [mm]", "ZADANIE / KONSTRUKCJA",
                  "Odległość osi śruby od środka ciężkości ładunku. Jeśli nie podano w zadaniu, "
                  "przyjmij bezpiecznie 150–250 mm."),
        param_row("Długość śruby [mm]", "ZADANIE",
                  "Wysokość podnoszenia (skok roboczy). Bierzesz z treści zadania."),
        param_row("Prędkość n₂ [obr/min]", "DOBÓR",
                  "Jak szybko ma się kręcić śruba. Wynika z prędkości podnoszenia (v). "
                  "Na początku strzelasz (np. 150 obr/min), a potem korygujesz, gdy dobierzesz gwint (skok P)."),
        param_row("Wsp. wyboczenia µ", "1.0",
                  "Sposób mocowania śruby. <br>• <b>1.0</b> = Przegub-Przegub (standardowy podnośnik).<br>"
                  "• <b>2.0</b> = Wspornik (jeden koniec wolny) – ⚠️ unikać, śruba wyjdzie gruba!"),
    ])
    st.markdown(f'<div class="instr-card"><h4>A. Parametry Pracy (Zadanie)</h4>{rows_eksp}</div>', 
                unsafe_allow_html=True)

    # Materiały
    rows_mat = "".join([
        param_row("Stal C45 / Brąz", "STANDARD",
                  "Najlepszy wybór na start. Stal C45 jest tania i mocna, Brąz na nakrętkę zapewnia poślizg."),
        param_row("Stal 42CrMo4", "OPCJA",
                  "Wybierz tę stal, jeśli przy C45 śruba nie spełnia warunków bezpieczeństwa (wskaźnik nz na czerwono)."),
        param_row("Nacisk pdop [MPa]", "12–15 MPa",
                  "Dopuszczalny nacisk dla brązu. Decyduje o wysokości nakrętki. "
                  "Jeśli nakrętka wychodzi gigantyczna – zmień materiał na taki z wyższym pdop."),
    ])
    st.markdown(f'<div class="instr-card"><h4>B. Materiały (Dobór)</h4>{rows_mat}</div>', 
                unsafe_allow_html=True)

    # Przekładnia
    rows_drive = "".join([
        param_row("Silnik n₁", "710 / 960 / 1440",
                  "Obroty silnika elektrycznego. Wybierz z szeregu normatywnego. "
                  "Zalecane wolniejsze (710 lub 960), żeby przełożenie nie wyszło kosmiczne."),
        param_row("Zęby z₁ / z₂", "DOBÓR",
                  "Liczba zębów kół pasowych. <br>• z₁ (małe) na silniku.<br>• z₂ (duże) na śrubie.<br>"
                  "<b>Cel:</b> Stosunek z₂/z₁ ma być taki sam jak n₁/n₂ (z dokładnością do 5%)."),
    ])
    st.markdown(f'<div class="instr-card"><h4>C. Napęd (Dobór)</h4>{rows_drive}</div>', 
                unsafe_allow_html=True)

    # ── 2. KONFIGURACJA WAŁÓW ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 2️⃣ Konfiguracja Wałów (Najtrudniejsze!)")
    
    st.markdown(
        """
        <div class="warn-box">
        ⚠️ <b>Nie projektuj wału w pamięci!</b><br>
        1. Weź kartkę.<br>
        2. Narysuj wał (stopnie, czopy pod łożyska, miejsce na koło pasowe).<br>
        3. Wymiaruj go (długości i średnice).<br>
        4. Dopiero wtedy wpisz dane do programu.
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("**Jak czytać parametry wału w programie?**")
    st.markdown("""
    - **Segmenty:** To klocki, z których budujesz wał, idąc od lewej strony. Każdy klocek ma długość i średnicę.
    - **Lokalizacje (Offset):** Program pyta: *"Na którym klocku (Seg) i jak daleko od jego początku (Offset) leży środek elementu?"*
    """)

    st.code(
        """
        PRZYKŁAD:
        Wał ma 3 segmenty:
        [Seg 1: 30mm] -> [Seg 2: 50mm] -> [Seg 3: 30mm]
        
        Chcesz łożysko na środku Seg 1?
        -> Seg: 1, Offset: 15 (połowa z 30)
        
        Chcesz koło pasowe na środku Seg 2?
        -> Seg: 2, Offset: 25 (połowa z 50)
        """, language=None
    )

    # ── 3. INTERPRETACJA WYNIKÓW ────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 3️⃣ Jak czytać wyniki? (Zielone vs Czerwone)")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔩 Śruba")
        st.markdown("""
        - **Samohamowność:** Musi być <span style='color:#4caf84'>**TAK**</span>. Jeśli jest NIE – ładunek spadnie Ci na głowę po wyłączeniu silnika.
          *Naprawa:* Zmniejsz skok gwintu (P) lub zmień średnicę.
        - **nz (Wsp. bezpieczeństwa):** Musi być **> 1.5**.
          *Naprawa:* Jeśli czerwone, weź lepszą stal (np. 42CrMo4) lub grubszą śrubę.
        - **Wysokość nakrętki:** Powinna być w granicach 1.2 – 2.5 średnicy gwintu.
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🔧 Wały")
        st.markdown("""
        - **sf (Safety Factor):** Musi być **> 1.5**. Oznacza, że wał nie pęknie.
          *Naprawa:* Zwiększ średnicę wału w miejscu, gdzie wykres naprężeń jest najwyższy.
        - **Ugięcie:** Musi być mniejsze niż limit.
          *Naprawa:* Zwiększ średnicę wału (sztywność zależy od średnicy w 4. potędze!).
        - **Kąt w łożysku:** Musi być **< 0.001 rad**. Łożyska nie lubią krzywych wałów.
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tip-box">
        💡 <b>Wskazówka:</b>
        Jeśli zmieniasz coś w panelu bocznym, kliknij <b>OBLICZ</b> ponownie. 
        Dopiero gdy wszystko świeci się na zielono, idź do zakładki <b>Dokumentacja</b>, 
        aby wygenerować PDF.
        </div>
        """, unsafe_allow_html=True
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
    n_sruby       = st.sidebar.number_input("Prędkość śruby n₂ [obr/min]", 1.0,   2000.0,   177.5,  10.0)
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


# ==============================================================================
# KONFIGURACJA WAŁÓW
# ==============================================================================

def get_wal_config(numer: int, seg_default, loc_defaults) -> dict:
    with st.expander(f"⚙️ Konfiguracja Wału {numer} — kliknij aby rozwinąć i wpisać własne wymiary",
                     expanded=False):

        st.caption(
            "⚠️ Domyślne wartości to projekt wzorcowy — zastąp je geometrią swojego wału. "
            "Moment skręcający i siłę poprzeczną program oblicza automatycznie."
        )

        st.markdown("**Segmenty wału** — każdy stopień jako długość × średnica [mm]")
        st.caption("Numeruj od lewej do prawej zgodnie z rysunkiem złożeniowym")
        segmenty = []
        for i, (l_def, d_def) in enumerate(seg_default):
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
    col_cb = st.columns(3)
    run_sruba = col_cb[0].checkbox("Śruba + nakrętka",  True)
    run_przek = col_cb[1].checkbox("Przekładnia pasowa", True)
    run_waly  = col_cb[2].checkbox("Wały napędowe",     True)

    st.markdown("---")

    wal1_cfg = wal2_cfg = None
    if run_waly:
        st.markdown("### Konfiguracja wałów")
        wal1_cfg = get_wal_config(
            numer=1,
            seg_default=[(30, 28), (120, 20)],
            loc_defaults=[(2, 11.0), (2, 109.0), (2, 60.0)],
        )
        wal2_cfg = get_wal_config(
            numer=2,
            seg_default=[(51, 20), (49.108, 22), (99.785, 24), (20.108, 22)],
            loc_defaults=[(2, 42.108), (4, 7.0), (3, 49.892)],
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
        wyniki = call_api("pelny", payload)

    if "_error" in wyniki:
        st.error(f"❌ {wyniki['_error']}")
        st.info("Upewnij się, że API jest uruchomione i poprawnie skonfigurowane w secrets.toml")
        return

    # Zapisz do session_state dla zakładki Dokumentacja
    wyniki_bez_wykresow = {}
    for k, v in wyniki.items():
        if isinstance(v, dict):
            wyniki_bez_wykresow[k] = {kk: vv for kk, vv in v.items() if kk != "wykres_b64"}
        else:
            wyniki_bez_wykresow[k] = v
    st.session_state["ostatnie_wyniki"] = wyniki_bez_wykresow
    st.session_state["ostatnie_inp"] = inp

    if run_sruba:  section_sruba(wyniki)
    if run_przek:  section_przekladnia(wyniki)
    if run_waly:
        section_wal(wyniki, "wal1", "Wał 1: Silnik (Napędowy)")
        section_wal(wyniki, "wal2", "Wał 2: Śruba (Napędzany)")

    all_ok = all(
        wyniki.get(k, {}).get("ok", True)
        for k in ["sruba", "przekladnia", "wal1", "wal2"]
        if k in wyniki
    )
    if all_ok:
        st.success("✅ Wszystkie warunki wytrzymałościowe i sztywnościowe spełnione.")
    else:
        st.warning("⚠️ Niektóre warunki nie zostały spełnione — sprawdź czerwone wskaźniki powyżej.")

# ==============================================================================
# ZAKŁADKA: KALKULATOR ŁOŻYSKA
# ==============================================================================

def tab_kalkulator_lozyska(inp: dict):
    st.markdown("""
    <div style='margin-bottom:1rem;'>
        <h1>🛡️ Kalkulator Łożysk (ISO 281)</h1>
        <p style='color:#4a5a7a; font-size:0.88rem; margin-top:-0.5rem;'>
            Weryfikacja trwałości i nośności wybranego łożyska
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "ℹ️ Ten moduł służy do sprawdzenia konkretnego łożyska z katalogu. "
        "Wpisz dane z katalogu (C, C₀) i sprawdź czy wytrzyma zadane obciążenie."
    )

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown("### 1. Parametry pracy")
        typ_lozyska = st.selectbox("Typ łożyska", [
            "kulkowe_skosne_dwurzedowe",
            "kulkowe_jednorzedowe",
            "kulkowe_oporowe",
            "walcowe_oporowe",
            "stozkowe",
            "barylkowe_oporowe"
        ])
        
        # Domyślne wartości pobieramy z bocznego panelu (inp), ale pozwalamy edytować
        Fa_N = st.number_input("Siła osiowa Fa [N]", 0.0, 500000.0, float(inp.get("sila_F", 10000.0)))
        Fr_N = st.number_input("Siła promieniowa Fr [N]", 0.0, 500000.0, 0.0)
        n_obr = st.number_input("Prędkość n [obr/min]", 0.0, 10000.0, float(inp.get("n_sruby", 177.5)))
        Lh_wym = st.number_input("Wymagana trwałość Lh [h]", 100.0, 100000.0, 10000.0)

    with col2:
        st.markdown("### 2. Dane z katalogu łożyska")
        c1, c2 = st.columns(2)
        d_wew = c1.number_input("Średnica wew. d [mm]", 10.0, 500.0, 30.0)
        
        st.markdown("---")
        c3, c4 = st.columns(2)
        C_kat = c3.number_input("Nośność dyn. C [kN]", 1.0, 5000.0, 30.0)
        C0_kat = c4.number_input("Nośność stat. C₀ [kN]", 1.0, 5000.0, 20.0)
        
        st.markdown("---")
        st.markdown("**Współczynniki obciążenia (z katalogu):**")
        c5, c6 = st.columns(2)
        X = c5.number_input("Współczynnik X", 0.0, 10.0, 0.67)
        Y = c6.number_input("Współczynnik Y", 0.0, 10.0, 0.67)

    st.markdown("---")
    
    if st.button("🧮 SPRAWDŹ ŁOŻYSKO", use_container_width=True):
        payload = {
            "typ": typ_lozyska,
            "Fa_N": Fa_N, "Fr_N": Fr_N, "n": n_obr,
            "Lh_wymagane": Lh_wym,
            "C_kat": C_kat, "C0_kat": C0_kat,
            "X": X, "Y": Y, "d_wew": d_wew
        }
        
        with st.spinner("Liczenie..."):
            wynik = call_api("lozysko_kalkulator", payload)
        
        if "_error" in wynik:
            st.error(wynik["_error"])
        else:
            # Wyświetlanie wyników
            st.markdown("### Wyniki weryfikacji")
            
            w1, w2, w3, w4 = st.columns(4)
            w1.metric("Wymagane C", f"{wynik.get('C_wym_kN', 0):.2f} kN")
            w2.metric("Katalogowe C", f"{C_kat:.2f} kN", 
                      delta=f"{C_kat - wynik.get('C_wym_kN', 0):.2f} kN")
            
            Lh_os = wynik.get('Lh_osiagalne', 0)
            lh_str = f"{Lh_os:.0f} h" if Lh_os < 900000 else "> 900 000 h"
            w3.metric("Trwałość L10h", lh_str)
            
            s0 = wynik.get('s0', 0)
            w4.metric("Bezpieczeństwo s₀", f"{s0:.2f}")

            # Szczegóły i alerty
            with st.expander("📋 Szczegółowe wyniki", expanded=True):
                render_logs(wynik.get("logs", []))
            
            render_alerts(wynik.get("errors", []), wynik.get("warnings", []))
            
            if wynik.get("ok"):
                st.success("✅ Łożysko dobrane poprawnie!")
            else:
                st.error("❌ Łożysko nie spełnia wymagań.")


# ==============================================================================
# MAIN
# ==============================================================================

def tab_dokumentacja():
    st.markdown("""
    <div style='margin-bottom:1rem;'>
        <h1>📄 Dokumentacja</h1>
        <p style='color:#4a5a7a; font-size:0.88rem; margin-top:-0.5rem;'>
            Generowanie dokumentacji technicznej w formacie LaTeX
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "ostatnie_wyniki" not in st.session_state:
        st.info("⚠️ Najpierw uruchom obliczenia w zakładce **Obliczenia**, a następnie wróć tutaj.")
        return

    wyniki = st.session_state["ostatnie_wyniki"]
    inp    = st.session_state["ostatnie_inp"]

    st.success("✅ Wyniki obliczeń dostępne — gotowe do wygenerowania dokumentacji.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Co zostanie wygenerowane:")
        st.markdown("""
        - Wstęp i założenia projektowe z Twoimi parametrami
        - Obliczenia śruby (wyboczenie, naprężenia, nakrętka)
        - Obliczenia przekładni pasowej
        - Wyniki analizy wałów (tabele z wartościami)
        - Opis konstrukcji i podsumowanie
        - Bibliografia
        """)
    with col2:
        generuj_btn = st.button("📄 GENERUJ LaTeX", use_container_width=True, key="gen_latex_btn")

    st.markdown("---")

    if not generuj_btn and "latex_code" not in st.session_state:
        return

    if generuj_btn:
        with st.spinner("Generowanie dokumentacji..."):
            result = call_api("dokumentacja", {"wyniki": wyniki, "inp": inp})
        if "_error" in result:
            st.error(f"❌ {result['_error']}")
            return
        st.session_state["latex_code"] = result.get("latex", "")

    latex = st.session_state.get("latex_code", "")
    if not latex:
        st.error("Brak kodu LaTeX — spróbuj ponownie.")
        return

    st.success("✅ Dokumentacja wygenerowana pomyślnie!")

    # Podgląd i pobieranie
    tab_kod, tab_podglad = st.tabs(["Kod LaTeX", "Podgląd kodu"])

    with tab_kod:
        st.markdown("""
        <div class="tip-box">
        💡 <b>Jak skompilować?</b>
        Skopiuj kod poniżej i wklej do <a href="https://www.overleaf.com" target="_blank">Overleaf</a>
        lub skompiluj lokalnie: <code>pdflatex dokumentacja.tex</code>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="⬇️ Pobierz plik .tex",
            data=latex.encode("utf-8"),
            file_name="dokumentacja_podnosnik.tex",
            mime="text/plain",
            use_container_width=True,
        )

        st.code(latex, language="latex")

    with tab_podglad:
        st.markdown("**Podgląd struktury dokumentu:**")
        # Wyciągnij sekcje z LaTeX dla podglądu
        import re
        sections = re.findall(r"\\section\{([^}]+)\}", latex)
        subsections = re.findall(r"\\subsection\{([^}]+)\}", latex)
        st.markdown("**Sekcje główne:**")
        for sec in sections:
            st.markdown(f"- {sec}")
        st.markdown("**Podsekcje:**")
        for sub in subsections:
            st.markdown(f"  - {sub}")
        st.info("Pełny podgląd PDF dostępny po skompilowaniu w Overleaf lub LaTeX lokalnie.")


def main():
    if not check_password():
        return

    inp = sidebar_inputs()

    tab_obl, tab_loz, tab_dok, tab_instr = st.tabs([
        "Obliczenia", "Kalkulator Łożysk", "Dokumentacja", "Instrukcja"
    ])

    with tab_obl:
        tab_obliczenia(inp)

    with tab_loz:
        tab_kalkulator_lozyska(inp)

    with tab_dok:
        tab_dokumentacja()

    with tab_instr:
        tab_instrukcja()


if __name__ == "__main__":
    main()
