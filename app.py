from pathlib import Path

from datetime import date, timedelta

import json

import streamlit as st

from urllib.parse import urlparse, parse_qsl, parse_qs, urlencode, urlunparse



APP_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = APP_DIR.parent

DATA_FILE = APP_DIR / "data" / "estudos.json"

APP_VERSION = "04D.2.2"



DEFAULT_BIBLE_VERSION = {

    "status": "identificada",

    "sigla": "NAA",

    "nome": "Nova Almeida Atualizada",

    "id_youversion": 1840,

    "fonte": "Padrão do aplicativo quando Carta/mensagem não informa outra versão",

}

YOUVERSION_VERSIONS_URL = "https://www.bible.com/pt/versions"



st.set_page_config(

    page_title="Conexões Sustentáveis",

    page_icon="🌱",

    layout="centered",

)



st.markdown(

    """

    <style>

    .block-container {max-width: 930px; padding-top: 1.5rem; padding-bottom: 3rem;}

    .hero {

        padding: 1.4rem 1.5rem;

        border-radius: 18px;

        background: linear-gradient(135deg, #1f4e79 0%, #548235 100%);

        color: white;

        margin-bottom: 1.2rem;

    }

    .hero h1 {margin: 0; font-size: 2rem;}

    .hero p {margin: .45rem 0 0 0; opacity: .95;}

    .tag {

        display: inline-block;

        padding: .22rem .55rem;

        border-radius: 999px;

        font-size: .78rem;

        font-weight: 700;

        margin-right: .35rem;

        margin-bottom: .4rem;

    }

    .oficial {background:#e2f0d9; color:#375623;}

    .biblico {background:#d9eaf7; color:#1f4e79;}

    .complementar {background:#fff2cc; color:#7f6000;}

    .ia {background:#eadcf8; color:#7030a0;}

    .prioridade {background:#fde9d9; color:#9c5700;}

    .preliminar {background:#fff2cc; color:#7f6000;}

    .atualidade {background:#e8f1fb; color:#1f4e79;}

    .card {

        border: 1px solid #d9dee5;

        border-radius: 14px;

        padding: 1rem 1.1rem;

        margin: .65rem 0 1rem 0;

        background: white;

    }

    .muted {color:#6b7280; font-size:.92rem;}

    @media (max-width: 600px) {

        .block-container {padding-left: 1rem; padding-right: 1rem;}

        .hero h1 {font-size: 1.55rem;}

    }

    </style>

    """,

    unsafe_allow_html=True,

)





def carregar_estudos():

    if not DATA_FILE.exists():

        st.error(f"Arquivo de dados não encontrado: {DATA_FILE}")

        st.stop()

    try:

        return json.loads(DATA_FILE.read_text(encoding="utf-8"))["estudos"]

    except (json.JSONDecodeError, KeyError) as erro:

        st.error(f"Não foi possível ler estudos.json: {erro}")

        st.stop()





def adicionar_inicio_youtube(url, inicio_segundos=None):

    """Acrescenta t=<segundos>s à URL do YouTube, sem duplicar o parâmetro."""

    if not url:

        return url

    try:

        inicio = int(inicio_segundos or 0)

    except (TypeError, ValueError):

        inicio = 0

    if inicio <= 0:

        return url



    parsed = urlparse(url)

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))

    query["t"] = f"{inicio}s"

    return urlunparse(parsed._replace(query=urlencode(query)))





def extrair_video_id_youtube(url):
    # Extrai video_id de watch, live, youtu.be, embed e shorts.
    if not url:
        return None
    try:
        parsed = urlparse(str(url))
    except Exception:
        return None

    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    if "youtu.be" in host:
        return path.strip("/").split("/")[0] or None

    if "youtube.com" in host or "youtube-nocookie.com" in host:
        if path == "/watch":
            return (parse_qs(parsed.query).get("v") or [None])[0]

        for prefix in ("/live/", "/embed/", "/shorts/"):
            if path.startswith(prefix):
                return path[len(prefix):].split("/")[0] or None

    return None


def url_youtube_canonica(url=None, video_id=None):
    video_id = str(video_id or "").strip() or extrair_video_id_youtube(url)
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    return url


def url_video_incorporavel(url):
    # Aceita apenas URLs apropriadas para o player.
    if not url:
        return False

    if extrair_video_id_youtube(url):
        return True

    try:
        parsed = urlparse(str(url))
    except Exception:
        return False

    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").lower()

    if "vimeo.com" in host:
        return True

    return path.endswith((".mp4", ".webm", ".mov", ".m4v"))


def formatar_segundos(segundos):

    try:

        total = int(segundos or 0)

    except (TypeError, ValueError):

        return ""

    if total <= 0:

        return ""

    horas, resto = divmod(total, 3600)

    minutos, segundos = divmod(resto, 60)

    if horas:

        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return f"{minutos:02d}:{segundos:02d}"





def tag(css, texto):

    st.markdown(f'<span class="tag {css}">{texto}</span>', unsafe_allow_html=True)





def status_disponivel(bloco):

    return str((bloco or {}).get("status", "")).lower() in {

        "disponivel", "disponivel_com_alerta", "identificada", "concluida", "consolidado", "ok", "validada"

    }





def resolver_versao_biblica(estudo):

    """

    Prioridade:

    1. versão explicitamente identificada na Carta/mensagem;

    2. NAA como padrão do aplicativo.

    """

    informada = (estudo or {}).get("versao_biblica") or {}

    if str(informada.get("status", "")).lower() == "identificada" and informada.get("sigla") and informada.get("id_youversion"):

        return informada

    return DEFAULT_BIBLE_VERSION.copy()





def domingo_da_semana(data_ref=None):

    data_ref = data_ref or date.today()

    dias_desde_domingo = (data_ref.weekday() + 1) % 7

    return data_ref - timedelta(days=dias_desde_domingo)





def formatar_data_br(data_ref):

    return data_ref.strftime("%d/%m/%Y")





def formatar_periodo_br(domingo):

    meses = [

        "janeiro", "fevereiro", "março", "abril", "maio", "junho",

        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"

    ]

    sabado = domingo + timedelta(days=6)

    if domingo.month == sabado.month:

        return f"{domingo.day:02d} a {sabado.day:02d} de {meses[domingo.month-1]} de {domingo.year}"

    return f"{domingo.day:02d} de {meses[domingo.month-1]} a {sabado.day:02d} de {meses[sabado.month-1]} de {sabado.year}"





def criar_placeholder_semana_atual(estudos):

    """Inclui somente em memória a semana atual quando ainda não existe registro persistido."""

    domingo = domingo_da_semana()

    estudo_id = domingo.isoformat()

    if any(str(e.get("id")) == estudo_id for e in estudos):

        return estudos



    placeholder = {

        "id": estudo_id,

        "status": "aguardando_mensagem",

        "tema": "Estudo desta semana — aguardando mensagem",

        "texto_principal": "Aguardando identificação",

        "texto_principal_youversion": None,

        "periodo": formatar_periodo_br(domingo),

        "mensagem": {

            "titulo": "Aguardando conclusão do culto de domingo à noite",

            "pregador": "Aguardando identificação",

            "url": None,

            "inicio_segundos": None,

            "observacao": "Assim que a automação detectar a gravação concluída, o registro semanal será atualizado."

        },

        "carta": {"status": "aguardando", "arquivo": None},

        "transcricao": {"status": "aguardando", "arquivo": None},

        "versao_biblica": {

            "status": "padrao_app",

            "sigla": "NAA",

            "nome": "Nova Almeida Atualizada",

            "id_youversion": 1840,

            "fonte": "Padrão do aplicativo"

        },

        "oficial": {}, "preliminar": {}, "referencias_biblicas": [],

        "filmes_series": [], "livros": [], "videos": [],

        "musicas_complementares": [], "atualidade": [],

        "situacoes_cotidianas": [], "dinamicas": [],

        "sustentabilidade": {}, "perguntas_adicionais": [], "prioridades": []

    }

    return [placeholder] + estudos





def rotulo_estudo(estudo):

    try:

        data_txt = date.fromisoformat(str(estudo.get("id"))).strftime("%d/%m/%Y")

    except Exception:

        data_txt = str(estudo.get("id", "Sem data"))

    tema = estudo.get("tema", "Estudo")

    status = str(estudo.get("status", ""))

    if "aguardando" in status or "detectada" in status or "preliminar" in status:

        icone = "🟡"

    elif "historico_importado" in status:

        icone = "📄"

    else:

        icone = "📚"

    return f"{icone} {data_txt} — {tema}"





def url_youversion(caminho_biblico, versao):

    """Monta link direto para Bible.com somente quando a versão foi identificada na fonte."""

    if not caminho_biblico or not versao:

        return None

    if str(versao.get("status", "")).lower() != "identificada":

        return None

    sigla = versao.get("sigla")

    id_youversion = versao.get("id_youversion")

    if not sigla or not id_youversion:

        return None

    return f"https://www.bible.com/pt/bible/{id_youversion}/{caminho_biblico}.{sigla}"





def render_versao_biblica(versao):

    """Exibe de forma compacta qual tradução está sendo usada no estudo."""

    versao = versao or DEFAULT_BIBLE_VERSION

    sigla = versao.get("sigla", "NAA")

    nome = versao.get("nome", "Nova Almeida Atualizada")

    fonte = versao.get("fonte", "Padrão do aplicativo")

    st.caption(f"📖 Versão utilizada: **{nome} ({sigla})** — {fonte}.")



def resolver_arquivo_local(bloco):

    """Resolve arquivo local tanto dentro de 04_APP quanto nas fontes semanais do projeto."""

    bloco = bloco or {}

    arquivo_app = bloco.get("arquivo_app")

    if arquivo_app:

        caminho = APP_DIR / arquivo_app

        if caminho.exists():

            return caminho

    arquivo_fonte = bloco.get("arquivo_fonte")

    if arquivo_fonte:

        caminho = PROJECT_ROOT / arquivo_fonte

        if caminho.exists():

            return caminho

    return None





def render_carta(carta):

    """Exibe Carta quando disponível e informa claramente quando ainda está pendente."""

    carta = carta or {}

    if not status_disponivel(carta):

        st.warning(

            "⏳ **Carta da Célula ainda não disponível.** "

            "Se houver transcrição da mensagem, o app pode manter um estudo preliminar e consolidá-lo depois."

        )

        return False



    arquivo_exibicao = carta.get("arquivo", "Carta da Célula")

    st.markdown(f"**Carta da Célula:** {arquivo_exibicao}")



    url = carta.get("url")

    if url:

        st.link_button("📄 Abrir Carta da Célula (PDF)", url)

        return True



    caminho = resolver_arquivo_local(carta)

    if caminho:

        dados = caminho.read_bytes()

        st.download_button(

            "📄 Abrir / baixar Carta da Célula (PDF)",

            data=dados,

            file_name=Path(arquivo_exibicao).name,

            mime="application/pdf",

        )

        if carta.get("arquivo_fonte") and not carta.get("arquivo_app"):

            st.caption("PDF lido diretamente da pasta 02_FONTES_SEMANAIS/01_CARTAS.")

        else:

            st.caption("O PDF está incluído no próprio aplicativo.")

        if carta.get("extracao_status") == "automatico_pendente_revisao":

            st.caption("Metadados importados automaticamente da Carta; revisar antes de uma publicação definitiva.")

        return True



    if carta.get("arquivo_app") or carta.get("arquivo_fonte"):

        st.warning(

            "A Carta está registrada, mas o PDF não foi encontrado neste ambiente. "

            "Confira a pasta 02_FONTES_SEMANAIS/01_CARTAS ou assets/cartas."

        )

        return True



    st.info("A Carta está disponível para o estudo, mas ainda não possui URL pública nem arquivo local associado.")

    return True





def lista_simples(itens):

    if not itens:

        st.info("Nenhum conteúdo priorizado nesta versão.")

        return

    for item in itens:

        st.markdown(f"• {item}")







def render_referencias(itens, versao):

    if not itens:

        st.info("Nenhuma referência priorizada nesta versão.")

        return

    for item in itens:

        if not isinstance(item, dict):

            st.warning("Referência complementar em formato inesperado; item ignorado.")

            continue

        referencia = item.get("referencia") or "Referência bíblica"

        st.markdown(f"#### {referencia}")

        if item.get("conexao"):

            st.write(item["conexao"])

        if item.get("como_usar"):

            st.markdown(f"**Como usar:** {item['como_usar']}")

        if item.get("pergunta"):

            st.markdown(f"**Pergunta:** {item['pergunta']}")

        url = url_youversion(item.get("youversion_ref"), versao)

        if url:

            sigla = versao.get("sigla", "")

            st.link_button(f"📖 Ler no YouVersion ({sigla})", url)

        elif item.get("youversion_ref"):

            st.caption("Link direto aguardando identificação da versão bíblica indicada pela Carta ou mensagem.")

        st.divider()







def render_obras(itens, livro=False):

    """

    Renderiza filmes/séries e livros.



    Para LIVROS, a prioridade de acesso é:

    1. trecho/prévia legal;

    2. PDF legal/autorizado;

    3. áudio/audiolivro legal/autorizado;

    4. página da editora, com aviso explícito quando não houver conteúdo

       de leitura/escuta localizado.

    """

    if not itens:

        st.info("Nenhuma referência priorizada nesta versão.")

        return



    for item in itens:

        if not isinstance(item, dict):

            st.warning("Referência complementar em formato inesperado; item ignorado.")

            continue



        titulo = item.get("titulo") or ("Livro" if livro else "Obra")

        if livro and item.get("autor"):

            titulo += f" — {item['autor']}"

        if item.get("tipo"):

            titulo = f"{item['tipo']}: {titulo}"



        st.markdown(f"#### {titulo}")



        if item.get("conexao"):

            st.write(item["conexao"])

        if item.get("como_usar"):

            st.markdown(f"**Como usar:** {item['como_usar']}")

        if item.get("pergunta"):

            st.markdown(f"**Pergunta:** {item['pergunta']}")



        # -------------------------------------------------------------

        # LIVROS: acesso ao conteúdo antes da página comercial/editorial.

        # -------------------------------------------------------------

        if livro:

            url_trecho = item.get("url_trecho") or item.get("url_preview")

            url_pdf = item.get("url_pdf_legal") or item.get("url_pdf")

            url_audio = item.get("url_audio_legal") or item.get("url_audio")

            url_editora = item.get("url_editora") or item.get("url_referencia")

            url_portugues_legado = item.get("url_portugues")



            acessos = []



            if url_trecho:

                acessos.append(("📖 Ler prévia/trecho", url_trecho))

            if url_pdf:

                acessos.append(("📄 Abrir PDF legal", url_pdf))

            if url_audio:

                acessos.append(("🎧 Ouvir prévia/áudio", url_audio))



            # Compatibilidade com registros antigos:

            # se só existir url_portugues, mantém o acesso sem inventar o tipo.

            if not acessos and url_portugues_legado:

                acessos.append(("📚 Abrir conteúdo em português", url_portugues_legado))



            if acessos:

                descricao_acesso = item.get("nota_acesso")

                if descricao_acesso:

                    st.success(descricao_acesso)

                else:

                    st.success(

                        "✅ Foi localizado conteúdo de leitura/escuta em fonte legal ou autorizada."

                    )



                cols = st.columns(min(len(acessos), 3))

                for idx, (label, url) in enumerate(acessos):

                    with cols[idx % len(cols)]:

                        st.link_button(label, url, use_container_width=True)



                # A editora continua disponível como referência secundária.

                if url_editora:

                    st.caption(

                        "A página da editora é mantida como referência da edição; "

                        "o acesso ao conteúdo acima é priorizado."

                    )

                    st.link_button("🏛️ Ver edição na editora", url_editora)

            else:

                st.info(

                    "ℹ️ **Não localizamos trecho/prévia, PDF legal ou áudio/audiolivro em português "

                    "em fonte oficial ou autorizada.** "

                    "O acesso abaixo direciona à editora para consultar a obra."

                )

                if url_editora:

                    st.link_button("🏛️ Ver obra na editora", url_editora)

                else:

                    st.caption(

                        "Também não há página editorial registrada para esta obra nesta versão."

                    )



            st.divider()

            continue



        # -------------------------------------------------------------

        # FILMES / SÉRIES

        # -------------------------------------------------------------

        url_oficial = item.get("url_oficial")

        url_clipe = item.get("url_clipe")

        url_referencia = item.get("url_referencia")



        if url_clipe and item.get("incorporar_clipe"):

            try:

                st.video(adicionar_inicio_youtube(url_clipe, item.get("inicio_segundos")))

            except Exception:

                st.caption("Não foi possível incorporar o trailer/clipe; use o botão de acesso direto.")



        botoes = []

        if url_oficial:

            botoes.append(("🌐 Abrir página oficial", url_oficial))

        if url_clipe:

            botoes.append((

                "▶ Assistir trailer/clipe",

                adicionar_inicio_youtube(url_clipe, item.get("inicio_segundos"))

            ))

        if url_referencia:

            botoes.append(("🌐 Abrir referência", url_referencia))



        if botoes:

            cols = st.columns(len(botoes))

            for col, (label, url) in zip(cols, botoes):

                with col:

                    st.link_button(label, url, use_container_width=True)



        st.divider()





def render_videos(itens):
    if not itens:
        st.info("Nenhum vídeo priorizado nesta versão.")
        return

    for item in itens:
        if not isinstance(item, dict):
            st.warning("Vídeo complementar em formato inesperado; item ignorado.")
            continue

        st.markdown(f"#### {item.get('titulo') or 'Vídeo complementar'}")

        if item.get("fonte"):
            st.caption(item["fonte"])
        if item.get("conexao"):
            st.write(item["conexao"])
        if item.get("como_usar"):
            st.markdown(f"**Como usar:** {item['como_usar']}")
        if item.get("pergunta"):
            st.markdown(f"**Pergunta:** {item['pergunta']}")

        if item.get("url"):
            url_base = url_youtube_canonica(item["url"])

            try:
                inicio = int(item.get("inicio_segundos") or 0)
            except (TypeError, ValueError):
                inicio = 0

            url_botao = adicionar_inicio_youtube(url_base, inicio)

            if url_video_incorporavel(url_base):
                try:
                    st.video(url_base, start_time=inicio)
                except Exception:
                    st.caption(
                        "Não foi possível incorporar esta mídia; "
                        "use o botão abaixo."
                    )
            else:
                st.caption(
                    "Este recurso é uma página externa. "
                    "Abra pelo botão abaixo."
                )

            st.link_button(
                "🎞️ Abrir recurso diretamente",
                url_botao,
            )
        else:
            st.caption("Link do vídeo ainda não disponível.")

        st.divider()

def render_musicas_oficiais(itens):
    if not itens:
        st.info("Nenhuma música indicada na Carta.")
        return

    for item in itens:
        if isinstance(item, str):
            st.markdown(f"• {item}")
            continue

        if not isinstance(item, dict):
            st.warning("Música oficial em formato inesperado; item ignorado.")
            continue

        titulo = item.get("titulo", "Música")
        interprete = item.get("interprete", "")

        st.markdown(
            f"**🎵 {titulo}**"
            + (f" — {interprete}" if interprete else "")
        )

        if item.get("url_oficial"):
            st.link_button(
                "▶ Ouvir/assistir em fonte oficial",
                item["url_oficial"],
            )
        elif item.get("url_busca_youtube"):
            st.link_button(
                "🔎 Procurar versão oficial no YouTube",
                item["url_busca_youtube"],
            )
            st.caption(
                "Link de busca: a versão oficial ainda não foi "
                "validada automaticamente."
            )

def render_musicas_complementares(itens):

    if not itens:

        st.info("Nenhuma música complementar priorizada nesta versão.")

        return



    for item in itens:

        if isinstance(item, str):

            st.markdown(f"• {item}")

            continue

        if not isinstance(item, dict):

            st.warning("Música complementar em formato inesperado; item ignorado.")

            continue



        titulo = item.get("titulo")

        decisao = str(item.get("decisao") or "").strip()



        # Compatibilidade com o formato legado que registra apenas a decisão

        # (ex.: "Nenhuma música complementar foi priorizada nesta versão.").

        if not titulo:

            if decisao:

                st.info(decisao)

            if item.get("motivo"):

                st.write(item["motivo"])

            continue



        st.markdown(f"#### 🎵 {titulo}")

        if item.get("interprete"):

            st.caption(item["interprete"])

        if item.get("conexao"):

            st.write(item["conexao"])

        if item.get("pergunta"):

            st.markdown(f"**Pergunta:** {item['pergunta']}")



        if item.get("url_oficial"):

            url = adicionar_inicio_youtube(item["url_oficial"], item.get("inicio_segundos"))

            if item.get("incorporar"):

                try:

                    st.video(url)

                except Exception:

                    st.caption("Não foi possível incorporar a música; use o botão de acesso direto.")

            st.link_button("▶ Ouvir/assistir em fonte oficial", url)



        if decisao:

            st.caption(f"Curadoria: {decisao}.")

        if item.get("motivo"):

            st.caption(item["motivo"])

        st.divider()







def render_situacoes(itens):

    """

    Compatível com:

    - formato legado 04B.7: area / cenario / pergunta;

    - formato 04B.8+: contexto / titulo / situacao / pergunta.

    """

    if not itens:

        st.info("Nenhuma situação priorizada nesta versão.")

        return



    for item in itens:

        if not isinstance(item, dict):

            st.warning("Situação cotidiana em formato inesperado; item ignorado.")

            continue



        contexto = item.get("contexto") or item.get("area") or "Vida cotidiana"

        titulo = item.get("titulo")

        situacao = item.get("situacao") or item.get("cenario") or ""

        pergunta = item.get("pergunta") or ""



        if titulo:

            st.markdown(f"#### {titulo}")

            st.caption(contexto)

        else:

            st.markdown(f"#### {contexto}")



        if situacao:

            st.write(situacao)

        else:

            st.caption("Descrição da situação ainda não disponível.")



        if pergunta:

            st.markdown(f"**Para discutir:** {pergunta}")

        st.divider()







def render_atualidade(itens):

    if not itens:

        st.info(

            "Nenhuma notícia foi associada a esta massa histórica de teste. "

            "Na rotina semanal, este módulo poderá receber curadoria local/regional, Brasil e mundo, sempre com fonte e data."

        )

        return

    for item in itens:

        if not isinstance(item, dict):

            st.warning("Item de atualidade em formato inesperado; item ignorado.")

            continue

        st.markdown(f"#### {item.get('abrangencia', 'Atualidade')} — {item.get('titulo', 'Sem título')}")

        st.caption(f"{item.get('veiculo', '')} • {item.get('data', '')}")

        if item.get("conexao"):

            st.markdown(f"**Conexão com o tema:** {item['conexao']}")

        if item.get("dilema"):

            st.markdown(f"**Dilema:** {item['dilema']}")

        if item.get("pergunta"):

            st.markdown(f"**Pergunta:** {item['pergunta']}")

        if item.get("url"):

            st.link_button("📰 Abrir fonte", item["url"])

        st.divider()







def render_dinamicas(itens):

    if not itens:

        st.info("Nenhuma dinâmica priorizada nesta versão.")

        return

    for item in itens:

        if not isinstance(item, dict):

            st.warning("Dinâmica em formato inesperado; item ignorado.")

            continue

        titulo = item.get("titulo") or "Dinâmica"

        duracao = item.get("duracao") or "tempo não informado"

        st.markdown(f"#### {titulo} · {duracao}")

        if item.get("objetivo"):

            st.markdown(f"**Objetivo:** {item['objetivo']}")

        if item.get("materiais"):

            st.markdown(f"**Materiais:** {item['materiais']}")

        passos = item.get("passos") or []

        if passos:

            st.markdown("**Passo a passo:**")

            for idx, passo in enumerate(passos, 1):

                st.markdown(f"{idx}. {passo}")

        perguntas = item.get("perguntas") or []

        if perguntas:

            st.markdown("**Perguntas finais:**")

            for pergunta in perguntas:

                st.markdown(f"• {pergunta}")

        st.divider()







def render_perguntas(itens):

    if not itens:

        st.info("Nenhuma pergunta adicional priorizada nesta versão.")

        return

    for item in itens:

        if isinstance(item, str):

            st.markdown(f"• {item}")

            continue

        if not isinstance(item, dict):

            st.warning("Pergunta adicional em formato inesperado; item ignorado.")

            continue

        tipo = item.get("tipo") or "Pergunta"

        pergunta = item.get("pergunta") or ""

        if pergunta:

            st.markdown(f"**{tipo}:** {pergunta}")





def analise_video_disponivel(estudo):

    # Autoriza preliminar após análise humana OU automática confiável.
    # GATE_04D_4_2_AUTOMATICO
    preliminar = estudo.get("preliminar") or {}
    mensagem = estudo.get("mensagem") or {}
    status = str(preliminar.get("status") or "").lower()

    try:
        inicio = int(mensagem.get("inicio_segundos") or 0)
    except (TypeError, ValueError):
        inicio = 0

    if inicio <= 0 or not bool(preliminar.get("ideias_centrais")):
        return False

    if status == "video_analisado_revisado_humanamente":
        return True

    if status == "video_analisado_automaticamente_confiavel":
        try:
            confianca = float(
                mensagem.get("analise_video_confianca_tema")
                or preliminar.get("confianca_conteudo")
                or 0
            )
        except (TypeError, ValueError):
            confianca = 0.0
        return confianca >= 0.85

    return False



def avaliar_estado_fontes(estudo):

    """Retorna os estados das fontes e exibe apenas o status geral do estudo."""

    carta = estudo.get("carta") or {}

    transcricao = estudo.get("transcricao") or {}

    mensagem = estudo.get("mensagem") or {}



    carta_ok = status_disponivel(carta)

    transcricao_ok = status_disponivel(transcricao)

    mensagem_ok = bool(mensagem.get("url"))



    if carta_ok:

        st.success(

            "🟢 **Estudo com Carta disponível.** "

            "O conteúdo oficial está organizado logo abaixo e separado da curadoria complementar."

        )

    elif transcricao_ok:

        st.warning(

            "🟡 **Estudo preliminar.** A Carta ainda não chegou; a mensagem/transcrição pode sustentar "

            "a preparação preliminar, que deverá ser conciliada quando a Carta for recebida."

        )

    elif mensagem_ok and analise_video_disponivel(estudo):

        st.warning(

            "🟡 **Estudo preliminar baseado na mensagem em vídeo.** "

            "O trecho da pregação foi identificado e analisado automaticamente com controle de confiança. "

            "A Carta da Célula ainda não chegou; quando chegar, o conteúdo deverá ser conciliado."

        )

    elif mensagem_ok:

        st.warning(

            "🟡 **Mensagem localizada, mas ainda sem Carta e sem transcrição confiável.** "

            "O app não deve gerar enriquecimento automático supondo o conteúdo da pregação."

        )

    else:

        st.error("🔴 **Fontes insuficientes.** Aguardando mensagem/transcrição ou Carta da Célula.")



    return carta_ok, transcricao_ok, mensagem_ok





def render_fonte_oficial_semana(estudo, carta_ok, transcricao_ok, mensagem_ok):

    """Agrupa todas as fontes e conteúdos oficiais em menus lineares e próximos."""

    carta = estudo.get("carta") or {}

    transcricao = estudo.get("transcricao") or {}

    mensagem = estudo.get("mensagem") or {}

    nucleo_oficial = estudo.get("oficial") or {}

    nucleo_preliminar = estudo.get("preliminar") or {}



    st.subheader("📚 Fonte oficial da semana")

    st.caption(

        "Mensagem, transcrição e Carta ficam reunidas aqui. Itens exclusivos da Carta permanecem "

        "como aguardando quando ela ainda não estiver disponível."

    )



    with st.expander("🎥 Mensagem"):

        if mensagem_ok:

            tag("oficial", "FONTE OFICIAL")

            st.markdown(f"**Título:** {mensagem.get('titulo') or 'Mensagem de domingo'}")

            st.markdown(f"**Pregador:** {mensagem.get('pregador') or 'Não informado'}")

            if mensagem.get("inicio_segundos"):

                inicio_formatado = formatar_segundos(mensagem.get("inicio_segundos"))

                if inicio_formatado:

                    st.caption(f"Início da pregação identificado em {inicio_formatado}.")

            if mensagem.get("observacao"):

                st.caption(mensagem["observacao"])

            # CORRECAO_04B_8_3_START_TIME

            url_base = url_youtube_canonica(mensagem.get("url"), mensagem.get("video_id"))

            try:

                inicio_video = int(mensagem.get("inicio_segundos") or 0)

            except (TypeError, ValueError):

                inicio_video = 0



            # O botão externo usa ?t=; o player Streamlit usa start_time.

            url_direta = adicionar_inicio_youtube(url_base, inicio_video)



            st.markdown("**Vídeo oficial da mensagem:**")

            try:

                if inicio_video > 0:

                    st.video(url_base, start_time=inicio_video)

                else:

                    st.video(url_base)

            except Exception:

                st.caption("Não foi possível incorporar o vídeo neste navegador; use o botão abaixo.")



            label = "🎥 Abrir no início da mensagem" if inicio_video > 0 else "🎥 Assistir ao culto"

            st.link_button(label, url_direta, use_container_width=False)

        else:

            st.info("⏳ Mensagem da semana ainda não localizada.")



    with st.expander("📝 Transcrição"):
        if transcricao_ok:
            tag("preliminar", "TRANSCRIÇÃO AUTOMÁTICA")
            st.caption(
                "Fonte: legenda/transcrição pública do vídeo oficial • Processamento automático. "
                "Pequenas diferenças de pontuação ou reconhecimento de fala podem ocorrer."
            )

            inicio_transcricao = formatar_segundos(transcricao.get("inicio_segundos"))
            fim_transcricao = formatar_segundos(transcricao.get("fim_segundos"))

            if inicio_transcricao and fim_transcricao:
                st.caption(
                    f"Trecho da mensagem: {inicio_transcricao} até {fim_transcricao}."
                )
            elif inicio_transcricao:
                st.caption(
                    f"Trecho da mensagem a partir de {inicio_transcricao}."
                )

            caminho = resolver_arquivo_local(transcricao)

            if caminho:
                try:
                    texto_transcricao = caminho.read_text(encoding="utf-8")
                except Exception as erro:
                    st.warning(f"Não foi possível ler o arquivo de transcrição: {erro}")
                else:
                    st.text_area(
                        "Texto da transcrição",
                        value=texto_transcricao,
                        height=520,
                        disabled=True,
                    )
                    st.download_button(
                        "⬇️ Baixar transcrição (.txt)",
                        data=texto_transcricao.encode("utf-8"),
                        file_name=Path(
                            transcricao.get("arquivo") or caminho.name
                        ).name,
                        mime="text/plain",
                    )

                if transcricao.get("url"):
                    st.link_button(
                        "🌐 Abrir fonte da transcrição",
                        transcricao["url"],
                        use_container_width=False,
                    )

            elif transcricao.get("url"):
                st.link_button(
                    "📝 Abrir transcrição",
                    transcricao["url"],
                    use_container_width=False,
                )

            else:
                st.info(
                    "Transcrição disponível para análise, mas ainda sem "
                    "link/arquivo exposto no app."
                )
        else:
            st.info("⏳ Aguardando transcrição confiável da mensagem.")

    with st.expander("📄 Carta da Célula"):

        if carta_ok:

            tag("oficial", "FONTE OFICIAL")

            nome_carta = carta.get("arquivo") or "Carta da Célula"

            st.markdown(f"**Documento:** {nome_carta}")

            if carta.get("url"):

                st.link_button("📄 Abrir Carta", carta["url"], use_container_width=False)

            else:

                caminho = resolver_arquivo_local(carta)

                if caminho:

                    st.download_button(

                        "📄 Abrir / baixar Carta",

                        data=caminho.read_bytes(),

                        file_name=Path(nome_carta).name,

                        mime="application/pdf",

                    )

                    if carta.get("arquivo_fonte") and not carta.get("arquivo_app"):

                        st.caption("Fonte local: 02_FONTES_SEMANAIS/01_CARTAS.")

                    if carta.get("extracao_status") == "automatico_pendente_revisao":

                        st.caption("Metadados extraídos automaticamente; revisão humana recomendada antes da publicação definitiva.")

                    conflito = carta.get("conflito_importacao") or {}

                    if conflito:

                        st.warning("Foram encontrados PDFs diferentes para a mesma semana. Revise os candidatos antes de consolidar a Carta oficial.")

                elif carta.get("arquivo_app") or carta.get("arquivo_fonte"):

                    st.warning("A Carta está registrada, mas o PDF não foi encontrado neste ambiente.")

                else:

                    st.info("A Carta está disponível, mas ainda não possui URL pública nem arquivo local associado.")

        else:

            st.info("⏳ Carta da Célula ainda não disponível.")



    with st.expander("💡 Ideias centrais"):

        if carta_ok:

            tag("oficial", "OFICIAL — CARTA")

            lista_simples(nucleo_oficial.get("ideias_centrais", []))

        elif transcricao_ok or analise_video_disponivel(estudo):

            tag("preliminar", "PRELIMINAR — MENSAGEM")

            lista_simples(nucleo_preliminar.get("ideias_centrais", []))

            if analise_video_disponivel(estudo) and not transcricao_ok:

                st.caption(

                    "Ideias extraídas da mensagem oficial em vídeo por análise automatizada. "

                    "A Carta, quando chegar, terá prioridade na conciliação."

                )

        else:

            st.info("⏳ Aguardando Carta ou transcrição confiável para identificar as ideias centrais.")



    with st.expander("❓ Perguntas oficiais"):

        if carta_ok:

            tag("oficial", "OFICIAL — CARTA")

            perguntas = nucleo_oficial.get("perguntas", [])

            if perguntas:

                for idx, pergunta in enumerate(perguntas, start=1):

                    st.markdown(f"**{idx}.** {pergunta}")

            else:

                st.info("A Carta não trouxe perguntas oficiais registradas neste estudo.")

        else:

            st.info("⏳ Aguardando a Carta da Célula para exibir as perguntas oficiais.")



    with st.expander("🎵 Músicas indicadas"):

        if carta_ok:

            tag("oficial", "OFICIAL — CARTA")

            render_musicas_oficiais(nucleo_oficial.get("musicas", []))

        else:

            st.info("⏳ Aguardando a Carta da Célula para confirmar as músicas indicadas oficialmente.")



    with st.expander("🎯 Desafio prático"):

        if carta_ok:

            tag("oficial", "OFICIAL — CARTA")

            desafio = nucleo_oficial.get("desafio")

            if desafio:

                st.write(desafio)

            else:

                st.info("A Carta não trouxe desafio prático registrado neste estudo.")

        else:

            st.info("⏳ Aguardando a Carta da Célula para exibir o desafio prático oficial.")





estudos = carregar_estudos()

if not estudos:

    st.warning("Nenhum estudo cadastrado.")

    st.stop()



estudos = criar_placeholder_semana_atual(estudos)

estudos = sorted(estudos, key=lambda e: str(e.get("id", "")), reverse=True)



st.markdown(

    """

    <div class="hero">

      <h1>🌱 Conexões Sustentáveis</h1>

      <p>Inteligência Artificial • Bíblia • Cultura • Vida cotidiana • Sustentabilidade</p>

    </div>

    """,

    unsafe_allow_html=True,

)



opcoes = {rotulo_estudo(e): e for e in estudos}

rotulo_selecionado = st.selectbox(

    "🗂️ Histórico de mensagens e estudos",

    options=list(opcoes.keys()),

    index=0,

    help="Os encontros anteriores permanecem disponíveis. A semana atual aparece primeiro."

)

estudo = opcoes[rotulo_selecionado]



st.caption("MVP acadêmico — conteúdo complementar sujeito a revisão humana")

st.header(estudo["tema"])



versao = resolver_versao_biblica(estudo)

url_texto_principal = url_youversion(estudo.get("texto_principal_youversion"), versao)

col_texto, col_biblia, col_versoes = st.columns([0.52, 0.24, 0.24])

with col_texto:

    st.subheader(f"📖 {estudo['texto_principal']}")

with col_biblia:

    if url_texto_principal:

        st.link_button(

            f"📖 Ler na {versao.get('sigla', 'NAA')}",

            url_texto_principal,

            use_container_width=True,

        )

with col_versoes:

    st.link_button(

        "📚 Escolher outra versão",

        YOUVERSION_VERSIONS_URL,

        use_container_width=True,

    )



render_versao_biblica(versao)

st.write(f"**Período:** {estudo['periodo']}")



carta_ok, transcricao_ok, mensagem_ok = avaliar_estado_fontes(estudo)

render_fonte_oficial_semana(estudo, carta_ok, transcricao_ok, mensagem_ok)



# Sem Carta, somente uma transcrição confiável autoriza a preparação preliminar.

pode_enriquecer = carta_ok or transcricao_ok or analise_video_disponivel(estudo)

if not pode_enriquecer:

    st.divider()

    if mensagem_ok:

        st.info(

            "A mensagem em vídeo já foi localizada, mas ainda não existe Carta nem transcrição confiável. "

            "Por segurança, o bloco **Enriquecendo a discussão** permanece oculto até haver conteúdo suficiente para análise."

        )

    else:

        st.info(

            "Ainda não há mensagem em vídeo, Carta ou transcrição confiável para esta semana. "

            "Por segurança, o bloco **Enriquecendo a discussão** permanece oculto até existir uma fonte suficiente para análise."

        )

    st.caption("Conexões Sustentáveis • Extensão II • MVP 04D.4.2")

    st.stop()



st.divider()

st.subheader("⭐ Três recursos prioritários para este encontro")

tag("prioridade", "CURADORIA 04D.4.2")

for item in estudo.get("prioridades", []):

    if isinstance(item, dict):

        recurso = item.get("recurso") or "Recurso complementar"

        motivo = item.get("motivo") or ""

        st.markdown(f"**{recurso}**" + (f" — {motivo}" if motivo else ""))

    else:

        st.markdown(f"• {item}")



st.divider()

st.subheader("🔎 Enriquecendo a discussão")

st.caption(

    "Conteúdo complementar separado das fontes oficiais. "

    "Quando a Carta estiver pendente, o material é preliminar e deve ser conciliado depois."

)



with st.expander("📖 Outros textos bíblicos", expanded=False):

    tag("biblico", "BÍBLICO")

    render_referencias(estudo.get("referencias_biblicas", []), versao)



with st.expander("🎬 Filmes e séries"):

    tag("complementar", "COMPLEMENTAR")

    render_obras(estudo.get("filmes_series", []))



with st.expander("📚 Livros"):

    tag("complementar", "COMPLEMENTAR")

    render_obras(estudo.get("livros", []), livro=True)



with st.expander("🎞️ Vídeos e animações"):

    tag("complementar", "COMPLEMENTAR")

    render_videos(estudo.get("videos", []))



with st.expander("🎵 Músicas complementares"):

    tag("complementar", "COMPLEMENTAR")

    render_musicas_complementares(estudo.get("musicas_complementares", []))



with st.expander("📰 Tema na atualidade"):

    tag("atualidade", "ATUALIDADE + FONTE")

    render_atualidade(estudo.get("atualidade", []))



with st.expander("💭 Situações da vida cotidiana"):

    tag("ia", "IA + REVISÃO HUMANA")

    render_situacoes(estudo.get("situacoes_cotidianas", []))



with st.expander("🎲 Dinâmicas"):

    tag("ia", "IA + REVISÃO HUMANA")

    render_dinamicas(estudo.get("dinamicas", []))



with st.expander("🌱 Conexão sustentável"):

    tag("ia", "IA + REVISÃO HUMANA")

    sustentabilidade = estudo.get("sustentabilidade") or {}

    if not sustentabilidade:

        st.info("Nenhuma conexão sustentável foi incluída nesta versão.")

    else:

        st.markdown(f"**ODS principal:** {sustentabilidade.get('ods_principal', '')}")

        st.markdown(f"**Conexão:** {sustentabilidade.get('conexao', '')}")

        st.markdown(f"**Aplicação prática:** {sustentabilidade.get('aplicacao', '')}")

        st.markdown(f"**Pergunta:** {sustentabilidade.get('pergunta', '')}")



with st.expander("❓ Perguntas adicionais"):

    tag("ia", "IA + REVISÃO HUMANA")

    render_perguntas(estudo.get("perguntas_adicionais", []))



st.divider()

st.caption("Conexões Sustentáveis • Extensão II • MVP 04D.4.2")

