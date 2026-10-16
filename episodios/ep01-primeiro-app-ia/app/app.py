import os
import time
import json
import httpx
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(page_title="True Hacking AI | EP01", page_icon="🤖")
st.title("🤖 True Hacking AI: meu primeiro app")
st.caption("Episódio 01 • IA local, Docker e tecnologia")
st.write("Analise nosso laboratório HTTP sem acessar sites de terceiros.")
endpoint = st.selectbox("Escolha uma página", ["/", "/seguro"])
model = st.text_input("Modelo Ollama (opcional)", value=os.getenv("OLLAMA_MODEL", ""), placeholder="Modelo já instalado")
if st.button("Analisar laboratório", type="primary"):
    url = os.environ.get("LAB_URL", "http://lab:3000").rstrip("/") + endpoint
    start = time.monotonic()
    try:
        response = httpx.get(url, follow_redirects=False, timeout=5)
        elapsed = round((time.monotonic() - start) * 1000)
        soup = BeautifulSoup(response.text[:100000], "html.parser")
        evidence = {
            "endpoint": endpoint, "status": response.status_code, "latency_ms": elapsed,
            "title": soup.title.get_text(strip=True) if soup.title else None,
            "headers": dict(response.headers),
            "checks": {h: h in response.headers for h in
                       ["content-security-policy", "referrer-policy", "x-content-type-options"]}
        }
        st.metric("HTTP", str(response.status_code))
        st.metric("Resposta", f"{elapsed} ms")
        st.write("Título:", evidence["title"])
        st.json(evidence)
        st.download_button("Baixar JSON", json.dumps(evidence, ensure_ascii=False, indent=2),
                           file_name="evidencias.json", mime="application/json")
        if model.strip():
            st.subheader("Explicação com IA local")
            try:
                ai = httpx.post(os.getenv("OLLAMA_URL", "http://host.docker.internal:11434").rstrip("/") + "/api/chat",
                    json={"model": model.strip(), "stream": False, "messages": [
                        {"role": "system", "content": "Explique evidências HTTP em português simples. Separe fatos de hipóteses. Header ausente não comprova vulnerabilidade. Não invente achados."},
                        {"role": "user", "content": json.dumps(evidence, ensure_ascii=False)}
                    ]}, timeout=120)
                ai.raise_for_status()
                st.write(ai.json()["message"]["content"])
            except (httpx.HTTPError, KeyError, ValueError) as err:
                st.warning(f"Ollama indisponível: {err}")
    except httpx.HTTPError as err:
        st.error(f"Laboratório indisponível: {err}")
