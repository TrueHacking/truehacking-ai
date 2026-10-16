# EP01 — Meu primeiro aplicativo com IA local

Projeto educacional da série True Hacking AI: Do n00b ao Lammer.

## Executar (Windows, Linux, macOS)

Requisitos: Docker Engine/Desktop com Compose v2. Ollama é opcional.

```bash
docker compose up --build -d
```

Abra http://127.0.0.1:8501. Escolha `/` ou `/seguro` e clique **Analisar laboratório**.

```bash
docker compose down
```

### IA opcional

Copie `.env.example` para `.env` (no PowerShell: `Copy-Item .env.example .env`) e defina `OLLAMA_MODEL` com um modelo já instalado. Reinicie os serviços.

No macOS com Apple Silicon prefira Ollama nativo para usar Metal. Em Linux, pode ser necessário configurar o Ollama para aceitar conexões provenientes da rede Docker, restringindo acesso via firewall; nunca exponha a porta 11434 na Internet. O aplicativo também funciona sem Ollama.

As imagens oficiais Python oferecem variantes AMD64 e ARM64, mas o desempenho da IA depende da máquina e do modelo. Valide ambos os builds antes de publicar releases.

O laboratório roda numa rede Compose interna; a aplicação só consulta duas rotas predefinidas, sem redirects ou acesso a alvos externos.

## Objetivos

Entender contêineres, HTTP, LLMs, prompts, desenvolvimento assistido por IA e limites de interpretação dos modelos.

> Apenas uso educacional em ambiente autorizado. Ausência de cabeçalho HTTP, isoladamente, não comprova vulnerabilidade.
