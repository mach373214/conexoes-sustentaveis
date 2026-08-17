# Conexões Sustentáveis — Snapshot Publicável 04E.1

Este diretório é uma **cópia de publicação**. Ele não contém as automações
operacionais do Windows e não deve substituir a pasta `04_APP`.

## Conteúdo

- `app.py` — aplicação Streamlit homologada;
- `data/estudos.json` — 13 estudos preparados para o ambiente público;
- `assets/cartas` — PDFs necessários ao app, quando disponíveis;
- `requirements.txt` — dependência mínima do app;
- `MANIFESTO_PUBLICACAO_04E_1.json` — hashes e controles da geração;
- `REVISAO_ANTES_DE_PUBLICAR.md` — conferência humana obrigatória antes do upload.

## Execução local

```bash
python -m streamlit run app.py
```

## Segurança

Este snapshot foi gerado sem `.env`, `secrets.toml`, BATs, logs,
scripts de automação ou caminhos absolutos do computador operacional.

A etapa de envio para GitHub/serviço de hospedagem deve ocorrer somente
após a revisão visual indicada em `REVISAO_ANTES_DE_PUBLICAR.md`.
