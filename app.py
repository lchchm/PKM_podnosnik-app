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

# CSS — industrial dark theme z precyzyjną typografią
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
code, .stCode, [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0c11 0%, #111520 100%);
    border-right: 1px solid #1e2535;
}
[data-testid="stSidebar"] label {
    color: #8899bb !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* Main background */
.stApp { background-color: #0d1117; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Headers */
h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important;
     color: #e8edf8 !important; letter-spacing: -0.02em; }
h2 { font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
     color: #c5d0e8 !important; border-bottom: 1px solid #1e2535;
     padding-bottom: 0.4rem; margin-top: 1.5rem !important; }
h3 { color: #7ea8f8 !important; font-size: 0.9rem !important;
     font-weight: 600 !important; letter-spacing: 0.05em; text-transform: uppercase; }

/* Metrics */
[data-testid="stMetric"] {
    background: #13192b;
    border: 1px solid #1e2f50;
    border-radius: 8px;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"] { color: #6a7fa8 !important; font-size: 0.75rem !important; }
[data-testid="stMetricValue"] { color: #7ea8f8 !important; font-size: 1.4rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1a3a8f, #1565c0) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2040b0, #1976d2) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(26,115,232,0.3) !important;
}

/* Result rows */
.result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0.8rem;
    border-bottom: 1px solid #151c2e;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
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
    background: #0f1520;
    border: 1px solid #1a2440;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.error-banner {
    background: #1a0a0a;
    border: 1px solid #7f1c1c;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    color: #ff7070;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    margin-top: 0.5rem;
}
.warn-banner {
    background: #1a1400;
    border: 1px solid #7f6000;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    color: #ffc060;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.83rem;
    margin-top: 0.5rem;
}
.api-status-ok  { color: #4caf84; font-size: 0.75rem; }
.api-status-err { color: #ef5350; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# AUTORYZACJA HASŁEM
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
        pwd = st.text_input("Hasło dostępu", type="password", label_visibility="collapsed",
                            placeholder="Wpisz hasło...")
        if st.button("Zaloguj się →", use_container_width=True):
            if pwd == st.secrets.get("APP_PASSWORD", ""):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Nieprawidłowe hasło.")
    return False


# ==============================================================================
# HELPERS UI
# ==============================================================================

def render_logs(logs: list):
    """Renderuje tabelę wyników z kolorowymi statusami."""
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
    st.markdown('<div class="section-card">' + "".join(rows) + "</div>", unsafe_allow_html=True)


def render_alerts(errors: list, warnings: list):
    for e in errors:
        st.markdown(f'<div class="error-banner">✘ {e}</div>', unsafe_allow_html=True)
    for w in warnings:
        st.markdown(f'<div class="warn-banner">⚠ {w}</div>', unsafe_allow_html=True)


def render_wykres(b64_str: str, caption: str = ""):
    if b64_str:
        img_bytes = base64.b64decode(b64_str)
        st.image(img_bytes, caption=caption, use_container_width=True)


# ==============================================================================
# SIDEBAR — DANE WEJŚCIOWE
# ==============================================================================

def sidebar_inputs() -> dict:
    st.sidebar.markdown("## ⚙️ Podnośnik Śrubowy")
    st.sidebar.markdown("---")

    # Status API
    if st.sidebar.button("🔌 Sprawdź połączenie z API", use_container_width=True):
        ok = health_check()
        if ok:
            st.sidebar.markdown('<span class="api-status-ok">✔ API działa poprawnie</span>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown('<span class="api-status-err">✘ API niedostępne</span>', unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # ── SEKCJA: Parametry eksploatacyjne ──
    st.sidebar.markdown("### 1 · Parametry eksploatacyjne")
    sila_F        = st.sidebar.number_input("Siła osiowa F [N]",         100.0, 500000.0, 10000.0, 500.0)
    ramie_sily    = st.sidebar.number_input("Ramię siły e [mm]",          0.0,  2000.0,   200.0,   10.0)
    dlugosc_sruby = st.sidebar.number_input("Długość robocza śruby [mm]", 50.0, 10000.0, 1000.0,   50.0)
    n_sruby       = st.sidebar.number_input("Prędkość śruby n₂ [obr/min]",1.0,  2000.0,   200.0,   10.0)
    h_element     = st.sidebar.number_input("Wys. elementu moc. h [mm]", 10.0,  500.0,    130.0,    5.0)
    alfa          = st.sidebar.selectbox("Współczynnik wyboczenia µ",
                                         [0.5, 0.7, 1.0, 2.0],
                                         index=2,
                                         format_func=lambda v: {0.5:"0.5 – obustronne utwierdzenie",
                                                                  0.7:"0.7 – utwierdzenie + przegub",
                                                                  1.0:"1.0 – obustronny przegub",
                                                                  2.0:"2.0 – wspornik"}[v])

    # ── SEKCJA: Materiały ──
    st.sidebar.markdown("### 2 · Materiały")
    mat_preset = st.sidebar.selectbox("Zestaw materiałowy",
        ["Stal C45 / Brąz CuSn (domyślne)", "Stal 42CrMo4 / Brąz CuSn", "Stal C35 / Poliamid", "Własne"])

    presets = {
        "Stal C45 / Brąz CuSn (domyślne)":  (355, 210, 210, 130, 0.13, 14),
        "Stal 42CrMo4 / Brąz CuSn":          (650, 210, 210, 130, 0.12, 16),
        "Stal C35 / Poliamid":               (305, 210,  70,   3, 0.25,  5),
    }
    if mat_preset in presets:
        Re_s, E_s, Re_n, E_n, mi, pdop = presets[mat_preset]
    else:
        Re_s  = st.sidebar.number_input("Re śruby [MPa]",    100.0, 2000.0, 355.0)
        E_s   = st.sidebar.number_input("E śruby [GPa]",      50.0,  300.0, 210.0)
        Re_n  = st.sidebar.number_input("Re nakrętki [MPa]",  30.0, 1000.0, 210.0)
        E_n   = st.sidebar.number_input("E nakrętki [GPa]",    1.0,  300.0, 130.0)
        mi    = st.sidebar.number_input("Wsp. tarcia µ",      0.01,    0.5,  0.13, 0.01)
        pdop  = st.sidebar.number_input("Nacisk pdop [MPa]",   1.0,   50.0,  14.0)

    # ── SEKCJA: Przekładnia ──
    st.sidebar.markdown("### 3 · Przekładnia pasowa")
    n1       = st.sidebar.number_input("Prędkość silnika n₁ [obr/min]", 100.0, 3000.0, 710.0, 10.0)
    z1       = st.sidebar.number_input("Zęby koła napędowego z₁", 6, 200, 34)
    z2       = st.sidebar.number_input("Zęby koła napędzanego z₂", 6, 500, 136)
    podzialka = st.sidebar.selectbox("Podziałka pasa [mm]", [3, 5, 8, 14], index=1)
    szer_pas = st.sidebar.number_input("Szerokość pasa b [mm]", 5.0, 100.0, 15.0, 5.0)

    # ── SEKCJA: Łożysko ──
    st.sidebar.markdown("### 4 · Łożysko wzdłużne")
    loz_Lh = st.sidebar.number_input("Żywotność L10h [h]", 500.0, 100000.0, 10000.0, 500.0)
    loz_kat = st.sidebar.selectbox("Kąt działania α [°]", [15, 25, 30, 40, 45], index=2)
    Y_map   = {15: 1.0, 25: 0.78, 30: 0.66, 40: 0.55, 45: 0.50}
    loz_Y   = Y_map[loz_kat]
    st.sidebar.caption(f"Współczynnik Y = {loz_Y}")

    return {
        # Ogólne
        "sila_F": sila_F, "ramie_sily": ramie_sily,
        "dlugosc_sruby": dlugosc_sruby, "n_sruby": n_sruby,
        "h_element": h_element, "alfa": float(alfa),
        # Materiały
        "Re_sruby": Re_s, "E_sruby": E_s,
        "Re_nakretki": Re_n, "E_nakretki": E_n,
        "mi": mi, "pdop": pdop,
        # Przekładnia
        "n1": n1, "z1": int(z1), "z2": int(z2),
        "podzialka": float(podzialka), "szerokosc": szer_pas,
        "hz": 2.1, "T_rob": 650.0, "m_metr": 0.360,
        # Łożysko
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
    col6.metric("Nz (bezp.)", f"{w.get('nz',0):.2f}")
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
        render_wykres(w["wykres_b64"], tytul)

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
    col2.metric("Żywotność L10h", f"{w.get('Lh', 0):.0f} h")

    with st.expander("📋 Szczegółowe kroki obliczeniowe"):
        render_logs(w.get("logs", []))
    render_alerts(w.get("errors", []), w.get("warnings", []))


# ==============================================================================
# KONFIGURACJA WAŁÓW (zaawansowana sekcja)
# ==============================================================================

def get_wal_config(numer: int, torque_default: float, force_default: float,
                   seg_default, loc_defaults) -> dict:
    with st.expander(f"⚙️ Konfiguracja Wału {numer} (kliknij aby rozwinąć)", expanded=False):
        c1, c2, c3 = st.columns(3)
        torque  = c1.number_input(f"Moment Ms [Nm]",    0.01, 5000.0, torque_default,  key=f"w{numer}_ms")
        force_t = c2.number_input(f"Siła Ft [N]",       1.0, 50000.0, force_default,   key=f"w{numer}_ft")
        naciag  = c3.number_input(f"Wsp. naciągu",      1.0,     5.0,           2.0,   key=f"w{numer}_nc")

        st.markdown("**Segmenty wału** (długość × średnica [mm])")
        segmenty = []
        for i, (l_def, d_def) in enumerate(seg_default):
            cs1, cs2 = st.columns(2)
            l = cs1.number_input(f"Seg {i+1} — długość [mm]", 1.0, 2000.0, float(l_def), key=f"w{numer}_sl{i}")
            d = cs2.number_input(f"Seg {i+1} — średnica [mm]", 1.0,  200.0, float(d_def), key=f"w{numer}_sd{i}")
            segmenty.append({"length": l, "diameter": d})

        st.markdown("**Lokalizacje podpór**")
        la1, la2, lb1, lb2, lf1, lf2 = st.columns(6)
        sA = int(la1.number_input("A — seg", 0, 9, loc_defaults[0][0], key=f"w{numer}_sA"))
        oA = la2.number_input("A — offset", 0.0, 1000.0, loc_defaults[0][1], key=f"w{numer}_oA")
        sB = int(lb1.number_input("B — seg", 0, 9, loc_defaults[1][0], key=f"w{numer}_sB"))
        oB = lb2.number_input("B — offset", 0.0, 1000.0, loc_defaults[1][1], key=f"w{numer}_oB")
        sF = int(lf1.number_input("F — seg", 0, 9, loc_defaults[2][0], key=f"w{numer}_sF"))
        oF = lf2.number_input("F — offset", 0.0, 1000.0, loc_defaults[2][1], key=f"w{numer}_oF")

    return {
        "nazwa": f"Wał {numer}: {'Silnik (Napędowy)' if numer == 1 else 'Śruba (Napędzany)'}",
        "torque": torque, "force_t": force_t, "naciag_factor": naciag,
        "segmenty": segmenty,
        "loc_support_A": {"seg_idx": sA, "offset": oA},
        "loc_support_B": {"seg_idx": sB, "offset": oB},
        "loc_load":      {"seg_idx": sF, "offset": oF},
    }


# ==============================================================================
# GŁÓWNA APLIKACJA
# ==============================================================================

def main():
    if not check_password():
        return

    inp = sidebar_inputs()

    # ── Header ──
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <h1>⚙️ Podnośnik Śrubowy</h1>
        <p style='color:#4a5a7a; font-size:0.88rem; margin-top:-0.5rem;'>
            Program obliczeniowy · Projekt v2.0 · FastAPI + Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Zakres obliczeń ──
    st.markdown("### Wybierz zakres obliczeń")
    col_cb = st.columns(5)
    run_sruba  = col_cb[0].checkbox("Śruba + nakrętka", True)
    run_przek  = col_cb[1].checkbox("Przekładnia pasowa", True)
    run_waly   = col_cb[2].checkbox("Wały napędowe", True)
    run_loz    = col_cb[3].checkbox("Łożysko", True)

    st.markdown("---")

    # ── Konfiguracja wałów (jeśli zaznaczono) ──
    wal1_cfg = wal2_cfg = None
    if run_waly:
        st.markdown("### Konfiguracja wałów")
        Ms_def  = 34.0
        Fo1_def = 440.47
        Fo2_def = 314.16

        wal1_cfg = get_wal_config(
            numer=1,
            torque_default=11.92,
            force_default=Fo1_def,
            seg_default=[(30, 28), (120, 20)],
            loc_defaults=[(1, 11.0), (1, 109.0), (1, 60.0)],
        )
        wal2_cfg = get_wal_config(
            numer=2,
            torque_default=Ms_def,
            force_default=Fo2_def,
            seg_default=[(51, 20), (49.108, 22), (99.785, 24), (20.108, 22)],
            loc_defaults=[(1, 42.108), (3, 7.0), (2, 49.892)],
        )
        st.markdown("---")

    # ── PRZYCISK OBLICZ ──
    col_btn = st.columns([2, 1, 2])
    with col_btn[1]:
        oblicz = st.button("▶ OBLICZ", use_container_width=True)

    if not oblicz:
        # Ekran powitalny
        st.markdown("""
        <div style='text-align:center; margin-top:3rem; color:#2a3a5a;'>
            <div style='font-size:4rem;'>⚙️</div>
            <p style='font-size:1rem;'>Uzupełnij parametry w panelu bocznym i kliknij <strong>OBLICZ</strong></p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── WYWOŁANIE API ──
    with st.spinner("Trwa obliczanie... ⏳"):
        material = {
            "Re_sruby": inp["Re_sruby"], "E_sruby": inp["E_sruby"],
            "Re_nakretki": inp["Re_nakretki"], "E_nakretki": inp["E_nakretki"],
            "mi": inp["mi"], "pdop": inp["pdop"],
        }

        # Buduj payload dla endpointu /oblicz/pelny
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
                "Ms_Nm": 34.0, "Pm_kW": 1.1,  # placeholders, API zaktualizuje
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

    # ── WYŚWIETLANIE WYNIKÓW ──
    if "_error" in wyniki:
        st.error(f"❌ {wyniki['_error']}")
        st.info("Upewnij się, że API jest uruchomione i poprawnie skonfigurowane w secrets.toml")
        return

    if run_sruba:
        section_sruba(wyniki)
    if run_przek:
        section_przekladnia(wyniki)
    if run_waly:
        section_wal(wyniki, "wal1", "Wał 1: Silnik (Napędowy)")
        section_wal(wyniki, "wal2", "Wał 2: Śruba (Napędzany)")
    if run_loz:
        section_lozysko(wyniki)

    # ── PODSUMOWANIE ──
    all_ok = all(
        wyniki.get(k, {}).get("ok", True)
        for k in ["sruba", "przekladnia", "wal1", "wal2", "lozysko"]
        if k in wyniki
    )
    if all_ok:
        st.success("✅ Wszystkie warunki wytrzymałościowe i sztywnościowe spełnione.")
    else:
        st.warning("⚠️ Niektóre warunki nie zostały spełnione — sprawdź czerwone wskaźniki powyżej.")


if __name__ == "__main__":
    main()
