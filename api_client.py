"""
Klient API — wysyła żądania do backendu obliczeniowego.
"""

import requests
import streamlit as st
from typing import Dict, Any


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {st.secrets['API_TOKEN']}",
        "Content-Type": "application/json",
    }


def _api_url(endpoint: str) -> str:
    base = st.secrets["API_URL"].rstrip("/")
    return f"{base}/oblicz/{endpoint}"


def call_api(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Wywołuje endpoint API i zwraca wyniki lub słownik z błędem."""
    try:
        r = requests.post(
            _api_url(endpoint),
            json=payload,
            headers=_headers(),
            timeout=60,
        )
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            return {"_error": "Błąd autoryzacji API. Sprawdź API_TOKEN w secrets."}
        elif r.status_code == 422:
            detail = r.json().get("detail", "Błąd walidacji danych.")
            return {"_error": str(detail)}
        else:
            return {"_error": f"Błąd API: HTTP {r.status_code} — {r.text[:300]}"}
    except requests.exceptions.ConnectionError:
        return {"_error": "Nie można połączyć się z API. Sprawdź API_URL w secrets lub czy serwer działa."}
    except requests.exceptions.Timeout:
        return {"_error": "Przekroczono czas oczekiwania (60s). Serwer może być przeciążony."}
    except Exception as e:
        return {"_error": f"Nieoczekiwany błąd: {e}"}


def health_check() -> bool:
    """Sprawdza czy API jest dostępne."""
    try:
        base = st.secrets["API_URL"].rstrip("/")
        r = requests.get(f"{base}/health", timeout=10)
        return r.status_code == 200
    except Exception:
        return False
