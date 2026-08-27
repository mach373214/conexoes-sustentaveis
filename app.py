# LAYOUT_MOBILE_IDOSOS_V1_0_6 — histórico isolado; base V1.0.5 preservada.
from pathlib import Path



from datetime import date, timedelta



import json

import re

import unicodedata



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



    
    /* LAYOUT_MOBILE_IDOSOS_V1_0_5 */
    p, li {font-size: 1.06rem; line-height: 1.65;}

    .stCaption p {
        font-size: 1rem !important;
        line-height: 1.55 !important;
        color: #4b5563 !important;
    }

    div.stButton > button {
        min-height: 64px;
        width: 100%;
        border-radius: 14px;
        font-size: 1.1rem;
        font-weight: 750;
        text-align: left;
        justify-content: flex-start;
        padding: .9rem 1rem;
        border: 1px solid #c9d2dc;
        box-shadow: 0 2px 7px rgba(0,0,0,.06);
    }

    [data-testid="stLinkButton"] a {
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1rem !important;
        font-weight: 650 !important;
        padding: .7rem .9rem !important;
        border-radius: 12px !important;
    }

    div[data-testid="stExpander"] summary {
        min-height: 58px;
        font-size: 1.07rem;
        font-weight: 650;
    }

    textarea:disabled {
        color: #1f2937 !important;
        -webkit-text-fill-color: #1f2937 !important;
        opacity: 1 !important;
        background-color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.62 !important;
    }

    .mobile-nav-title {
        font-size: 1.4rem;
        line-height: 1.25;
        font-weight: 800;
        margin: .5rem 0 .25rem 0;
        color: #1f2937;
    }

    .mobile-nav-help {
        font-size: 1.06rem;
        line-height: 1.58;
        color: #374151;
        margin-bottom: .8rem;
    }

    .mobile-nav-note {
        font-size: 1.02rem;
        line-height: 1.5;
        color: #4b5563;
        margin-top: -.1rem;
        margin-bottom: .75rem;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-left: .85rem !important;
            padding-right: .85rem !important;
            padding-top: .9rem !important;
        }
        .hero {padding: 1.15rem 1rem; border-radius: 15px;}
        .hero h1 {font-size: 1.65rem !important; line-height: 1.2;}
        .hero p {font-size: 1.02rem; line-height: 1.5;}
        h1 {font-size: 1.8rem !important;}
        h2 {font-size: 1.5rem !important;}
        h3 {font-size: 1.28rem !important;}
        div.stButton > button {min-height: 68px; font-size: 1.14rem;}
        [data-testid="stLinkButton"] a {min-height: 52px !important; font-size: 1.04rem !important;}
    }


    /* =========================================================
       MENU_CARTOES_3X2_V1_0_0
       Escopo estrito: somente os seis cartões do menu principal.
       ========================================================= */

    .menu-card-icon {
        width: 58px;
        height: 58px;
        margin: .15rem auto .45rem auto;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        line-height: 1;
        background: #eef5ff;
    }

    .menu-card-note {
        margin: .35rem .08rem .05rem .08rem;
        text-align: center;
        color: #4b5563;
        font-size: .96rem;
        line-height: 1.38;
    }

    .st-key-menu_card_avisos,
    .st-key-menu_card_mensagem,
    .st-key-menu_card_carta,
    .st-key-menu_card_estudo,
    .st-key-menu_card_enriquecer,
    .st-key-menu_card_historico {
        min-height: 258px;
        border-radius: 16px;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(15, 23, 42, .07);
    }

    .st-key-menu_card_avisos .menu-card-icon {background:#fff0f3;}
    .st-key-menu_card_mensagem .menu-card-icon {background:#edf6ff;}
    .st-key-menu_card_carta .menu-card-icon {background:#f3efff;}
    .st-key-menu_card_estudo .menu-card-icon {background:#edf6ff;}
    .st-key-menu_card_enriquecer .menu-card-icon {background:#fff4e6;}
    .st-key-menu_card_historico .menu-card-icon {background:#f3efff;}

    .st-key-menu_card_avisos div.stButton > button,
    .st-key-menu_card_mensagem div.stButton > button,
    .st-key-menu_card_carta div.stButton > button,
    .st-key-menu_card_estudo div.stButton > button,
    .st-key-menu_card_enriquecer div.stButton > button,
    .st-key-menu_card_historico div.stButton > button {
        min-height: 58px;
        width: 100%;
        padding: .45rem .3rem;
        border: 0;
        border-radius: 11px;
        box-shadow: none;
        background: transparent;
        color: #111827;
        font-size: 1rem;
        line-height: 1.18;
        font-weight: 800;
        text-align: center;
        justify-content: center;
        white-space: normal;
    }

    .st-key-menu_card_avisos div.stButton > button:hover,
    .st-key-menu_card_mensagem div.stButton > button:hover,
    .st-key-menu_card_carta div.stButton > button:hover,
    .st-key-menu_card_estudo div.stButton > button:hover,
    .st-key-menu_card_enriquecer div.stButton > button:hover,
    .st-key-menu_card_historico div.stButton > button:hover {
        border: 0;
        background: #f8fafc;
        color: #111827;
        box-shadow: none;
    }

    @media (max-width: 600px) {
        /* =========================================================
           MENU_CARTOES_3X2_MOBILE_V1_0_5
           Somente no celular: cada fileira do menu vira uma grade
           real de 3 colunas iguais. O desktop permanece V1.0.2.
           ========================================================= */

        .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
            column-gap: .42rem !important;
            row-gap: .42rem !important;
            width: 100% !important;
            max-width: 100% !important;
            overflow: visible !important;
            align-items: stretch !important;
        }

        .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important;
            min-width: 0 !important;
            max-width: none !important;
            flex: none !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }

        .st-key-menu_grid_3x2 {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }

        .menu-card-icon {
            width: 50px;
            height: 50px;
            font-size: 1.75rem;
            margin-bottom: .28rem;
        }

        .menu-card-note {
            font-size: .88rem;
            line-height: 1.30;
        }

        .st-key-menu_card_avisos,
        .st-key-menu_card_mensagem,
        .st-key-menu_card_carta,
        .st-key-menu_card_estudo,
        .st-key-menu_card_enriquecer,
        .st-key-menu_card_historico {
            min-height: 242px;
        }

        .st-key-menu_card_avisos div.stButton > button,
        .st-key-menu_card_mensagem div.stButton > button,
        .st-key-menu_card_carta div.stButton > button,
        .st-key-menu_card_estudo div.stButton > button,
        .st-key-menu_card_enriquecer div.stButton > button,
        .st-key-menu_card_historico div.stButton > button {
            min-height: 60px;
            padding: .34rem .12rem;
            font-size: .90rem;
            line-height: 1.16;
        }
    }


    /* =========================================================
       MENU_CARTOES_TAMANHO_FIXO_V1_0_0

       Grade:
       - desktop/tablet: 3 x 2
       - smartphone <= 430 px: 2 x 3

       Regra adicional:
       - todos os cartões têm altura FIXA por breakpoint;
       - títulos e descrições têm áreas estáveis;
       - o tamanho do cartão NÃO depende do conteúdo.
       ========================================================= */

    .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        column-gap: .72rem !important;
        row-gap: .72rem !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow: visible !important;
        align-items: stretch !important;
    }

    .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        flex: none !important;
        flex-basis: auto !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        box-sizing: border-box !important;
    }

    .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
    .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        flex: none !important;
        flex-basis: auto !important;
    }

    /* ---------------------------------------------------------
       TAMANHO FIXO — DESKTOP / TABLET
       --------------------------------------------------------- */
    .st-key-menu_card_avisos,
    .st-key-menu_card_mensagem,
    .st-key-menu_card_carta,
    .st-key-menu_card_estudo,
    .st-key-menu_card_enriquecer,
    .st-key-menu_card_historico {
        height: 258px !important;
        min-height: 258px !important;
        max-height: 258px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }

    .st-key-menu_card_avisos div.stButton > button,
    .st-key-menu_card_mensagem div.stButton > button,
    .st-key-menu_card_carta div.stButton > button,
    .st-key-menu_card_estudo div.stButton > button,
    .st-key-menu_card_enriquecer div.stButton > button,
    .st-key-menu_card_historico div.stButton > button {
        height: 68px !important;
        min-height: 68px !important;
        max-height: 68px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
    }

    .menu-card-note {
        min-height: 68px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    @media (max-width: 430px) {
        .st-key-menu_grid_3x2 div[data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            column-gap: .70rem !important;
            row-gap: .70rem !important;
        }

        /* -----------------------------------------------------
           TAMANHO FIXO — CELULAR REAL
           246 px comporta o maior texto observado sem deixar
           os demais cartões menores.
           ----------------------------------------------------- */
        .st-key-menu_card_avisos,
        .st-key-menu_card_mensagem,
        .st-key-menu_card_carta,
        .st-key-menu_card_estudo,
        .st-key-menu_card_enriquecer,
        .st-key-menu_card_historico {
            height: 246px !important;
            min-height: 246px !important;
            max-height: 246px !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }

        .menu-card-icon {
            width: 54px !important;
            height: 54px !important;
            font-size: 1.9rem !important;
            margin-bottom: .35rem !important;
        }

        .st-key-menu_card_avisos div.stButton > button,
        .st-key-menu_card_mensagem div.stButton > button,
        .st-key-menu_card_carta div.stButton > button,
        .st-key-menu_card_estudo div.stButton > button,
        .st-key-menu_card_enriquecer div.stButton > button,
        .st-key-menu_card_historico div.stButton > button {
            height: 72px !important;
            min-height: 72px !important;
            max-height: 72px !important;
            padding: .42rem .22rem !important;
            font-size: .98rem !important;
            line-height: 1.22 !important;
            word-break: normal !important;
            overflow-wrap: normal !important;
            hyphens: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .menu-card-note {
            height: 78px !important;
            min-height: 78px !important;
            max-height: 78px !important;
            margin: .35rem .20rem .10rem .20rem !important;
            font-size: .92rem !important;
            line-height: 1.35 !important;
            word-break: normal !important;
            overflow-wrap: normal !important;
            hyphens: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }
    }

    @media (prefers-color-scheme: dark) and (max-width: 430px) {
        .mobile-nav-title {color:#f8fafc !important;}
        .mobile-nav-help {color:#d1d5db !important;}
    }


    /* =========================================================
       MENU_CARD_NATIVO_CLICAVEL_V1_0_2
       REGRA: o próprio st.button ocupa 100% do cartão.
       Sem overlay, sem href, sem query-param e sem botão invisível.
       ========================================================= */

    .st-key-menu_card_avisos,
    .st-key-menu_card_mensagem,
    .st-key-menu_card_carta,
    .st-key-menu_card_estudo,
    .st-key-menu_card_enriquecer,
    .st-key-menu_card_historico {
        padding: 0 !important;
        cursor: pointer !important;
    }

    .st-key-menu_card_avisos div[data-testid="stVerticalBlock"],
    .st-key-menu_card_mensagem div[data-testid="stVerticalBlock"],
    .st-key-menu_card_carta div[data-testid="stVerticalBlock"],
    .st-key-menu_card_estudo div[data-testid="stVerticalBlock"],
    .st-key-menu_card_enriquecer div[data-testid="stVerticalBlock"],
    .st-key-menu_card_historico div[data-testid="stVerticalBlock"] {
        height: 100% !important;
        min-height: 100% !important;
        padding: 0 !important;
        gap: 0 !important;
    }

    .st-key-menu_card_avisos div.stButton,
    .st-key-menu_card_mensagem div.stButton,
    .st-key-menu_card_carta div.stButton,
    .st-key-menu_card_estudo div.stButton,
    .st-key-menu_card_enriquecer div.stButton,
    .st-key-menu_card_historico div.stButton {
        height: 100% !important;
        min-height: 100% !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .st-key-menu_card_avisos div.stButton > button,
    .st-key-menu_card_mensagem div.stButton > button,
    .st-key-menu_card_carta div.stButton > button,
    .st-key-menu_card_estudo div.stButton > button,
    .st-key-menu_card_enriquecer div.stButton > button,
    .st-key-menu_card_historico div.stButton > button {
        width: 100% !important;
        height: 100% !important;
        min-height: 100% !important;
        max-height: none !important;
        padding: 1.05rem .70rem !important;
        margin: 0 !important;
        border: 1px solid #d9dee5 !important;
        border-radius: 14px !important;
        background: white !important;
        box-shadow: 0 2px 5px rgba(15, 23, 42, .07) !important;
        cursor: pointer !important;

        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: .55rem !important;

        white-space: normal !important;
        overflow: hidden !important;
    }

    .st-key-menu_card_avisos div.stButton > button:hover,
    .st-key-menu_card_mensagem div.stButton > button:hover,
    .st-key-menu_card_carta div.stButton > button:hover,
    .st-key-menu_card_estudo div.stButton > button:hover,
    .st-key-menu_card_enriquecer div.stButton > button:hover,
    .st-key-menu_card_historico div.stButton > button:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, .11) !important;
    }

    .st-key-menu_card_avisos div.stButton > button > div[data-testid="stMarkdownContainer"],
    .st-key-menu_card_mensagem div.stButton > button > div[data-testid="stMarkdownContainer"],
    .st-key-menu_card_carta div.stButton > button > div[data-testid="stMarkdownContainer"],
    .st-key-menu_card_estudo div.stButton > button > div[data-testid="stMarkdownContainer"],
    .st-key-menu_card_enriquecer div.stButton > button > div[data-testid="stMarkdownContainer"],
    .st-key-menu_card_historico div.stButton > button > div[data-testid="stMarkdownContainer"] {
        order: 2 !important;
        min-height: 58px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .st-key-menu_card_avisos div.stButton > button p,
    .st-key-menu_card_mensagem div.stButton > button p,
    .st-key-menu_card_carta div.stButton > button p,
    .st-key-menu_card_estudo div.stButton > button p,
    .st-key-menu_card_enriquecer div.stButton > button p,
    .st-key-menu_card_historico div.stButton > button p {
        margin: 0 !important;
        color: #111827 !important;
        font-size: .98rem !important;
        line-height: 1.22 !important;
        font-weight: 800 !important;
        text-align: center !important;
    }

    .st-key-menu_card_avisos div.stButton > button::before,
    .st-key-menu_card_mensagem div.stButton > button::before,
    .st-key-menu_card_carta div.stButton > button::before,
    .st-key-menu_card_estudo div.stButton > button::before,
    .st-key-menu_card_enriquecer div.stButton > button::before,
    .st-key-menu_card_historico div.stButton > button::before {
        order: 1 !important;
        width: 54px !important;
        height: 54px !important;
        min-width: 54px !important;
        min-height: 54px !important;
        border-radius: 999px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1.85rem !important;
        line-height: 1 !important;
    }

    .st-key-menu_card_avisos div.stButton > button::after,
    .st-key-menu_card_mensagem div.stButton > button::after,
    .st-key-menu_card_carta div.stButton > button::after,
    .st-key-menu_card_estudo div.stButton > button::after,
    .st-key-menu_card_enriquecer div.stButton > button::after,
    .st-key-menu_card_historico div.stButton > button::after {
        order: 3 !important;
        min-height: 68px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #4b5563 !important;
        font-size: .92rem !important;
        line-height: 1.35 !important;
        font-weight: 400 !important;
        text-align: center !important;
        white-space: normal !important;
    }

    .st-key-menu_card_avisos div.stButton > button::before {
        content: "📣";
        background: #fff0f3 !important;
    }
    .st-key-menu_card_avisos div.stButton > button::after {
        content: "Comunicados oficiais da semana.";
    }

    .st-key-menu_card_mensagem div.stButton > button::before {
        content: "▶️";
        background: #eaf4ff !important;
    }
    .st-key-menu_card_mensagem div.stButton > button::after {
        content: "Vídeo oficial já posicionado no início da pregação.";
    }

    .st-key-menu_card_carta div.stButton > button::before {
        content: "📄";
        background: #f3edff !important;
    }
    .st-key-menu_card_carta div.stButton > button::after {
        content: "Material oficial do encontro, quando disponível.";
    }

    .st-key-menu_card_estudo div.stButton > button::before {
        content: "📖";
        background: #eaf4ff !important;
    }
    .st-key-menu_card_estudo div.stButton > button::after {
        content: "Transcrição, ideias, perguntas, músicas e desafio.";
    }

    .st-key-menu_card_enriquecer div.stButton > button::before {
        content: "✨";
        background: #fff3df !important;
    }
    .st-key-menu_card_enriquecer div.stButton > button::after {
        content: "Bíblia, cultura, atualidade, dinâmica e aplicação.";
    }

    .st-key-menu_card_historico div.stButton > button::before {
        content: "📅";
        background: #f3edff !important;
    }
    .st-key-menu_card_historico div.stButton > button::after {
        content: "Consulte semanas e materiais já publicados.";
    }

    @media (max-width: 430px) {
        .st-key-menu_card_avisos div.stButton > button,
        .st-key-menu_card_mensagem div.stButton > button,
        .st-key-menu_card_carta div.stButton > button,
        .st-key-menu_card_estudo div.stButton > button,
        .st-key-menu_card_enriquecer div.stButton > button,
        .st-key-menu_card_historico div.stButton > button {
            padding: .85rem .45rem !important;
        }

        .st-key-menu_card_avisos div.stButton > button p,
        .st-key-menu_card_mensagem div.stButton > button p,
        .st-key-menu_card_carta div.stButton > button p,
        .st-key-menu_card_estudo div.stButton > button p,
        .st-key-menu_card_enriquecer div.stButton > button p,
        .st-key-menu_card_historico div.stButton > button p {
            font-size: .96rem !important;
        }

        .st-key-menu_card_avisos div.stButton > button::after,
        .st-key-menu_card_mensagem div.stButton > button::after,
        .st-key-menu_card_carta div.stButton > button::after,
        .st-key-menu_card_estudo div.stButton > button::after,
        .st-key-menu_card_enriquecer div.stButton > button::after,
        .st-key-menu_card_historico div.stButton > button::after {
            min-height: 78px !important;
            font-size: .90rem !important;
        }
    }


    /* =========================================================
       CABECALHO_PERIODO_DESTAQUE_V1_0_3
       ========================================================= */
    .periodo-destaque {
        margin: .08rem 0 .55rem 0;
        color: #1f2937;
        font-size: 1.30rem;
        line-height: 1.35;
        font-weight: 500;
    }

    .periodo-destaque strong {
        font-weight: 800;
    }

    /* =========================================================
       ACESSOS_AUXILIARES_2COL_V1_0_3
       ========================================================= */
    .st-key-acessos_auxiliares div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: .65rem !important;
        width: 100% !important;
        align-items: start !important;
    }

    .st-key-acessos_auxiliares div[data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        min-width: 0 !important;
        max-width: none !important;
        flex: none !important;
    }

    @media (max-width: 600px) {
        .periodo-destaque {
            font-size: 1.22rem;
            line-height: 1.38;
            margin-bottom: .50rem;
        }

        .st-key-acessos_auxiliares div[data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
            gap: .45rem !important;
        }
    }


    /* =========================================================
       AJUSTES_BOTOES_HISTORICO_256_V1_0_1
       ========================================================= */

    /* COMO USAR: st.expander */
    .st-key-acessos_auxiliares div[data-testid="stExpander"] details > summary,
    .st-key-acessos_auxiliares div[data-testid="stExpander"] summary {
        min-height: 3.15rem !important;
        height: 3.15rem !important;
        padding-top: .60rem !important;
        padding-bottom: .60rem !important;
        padding-left: .85rem !important;
        padding-right: .85rem !important;
        display: flex !important;
        align-items: center !important;
        font-size: 1rem !important;
        line-height: 1.2 !important;
    }

    .st-key-acessos_auxiliares div[data-testid="stExpander"] summary p,
    .st-key-acessos_auxiliares div[data-testid="stExpander"] summary span {
        font-size: 1rem !important;
        line-height: 1.2 !important;
    }

    /* AVALIAÇÃO: st.popover */
    .st-key-acessos_auxiliares div[data-testid="stPopover"] > button,
    .st-key-acessos_auxiliares div[data-testid="stPopover"] button {
        min-height: 3.15rem !important;
        height: 3.15rem !important;
        padding-top: .60rem !important;
        padding-bottom: .60rem !important;
        padding-left: .85rem !important;
        padding-right: .85rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 1rem !important;
        line-height: 1.2 !important;
    }

    .st-key-acessos_auxiliares div[data-testid="stPopover"] button p,
    .st-key-acessos_auxiliares div[data-testid="stPopover"] button span {
        font-size: 1rem !important;
        line-height: 1.2 !important;
    }

    .st-key-acessos_auxiliares div[data-testid="stHorizontalBlock"] > div {
        align-self: stretch !important;
    }

    /* HISTÓRICO */
    .historico-label-maior {
        font-size: 1.12rem !important;
        line-height: 1.35 !important;
        font-weight: 700 !important;
        color: #1f2937 !important;
        margin: .10rem 0 .42rem 0 !important;
    }

    .st-key-historico_seletor_maior div[data-baseweb="select"] > div {
        min-height: 3.15rem !important;
        height: auto !important;
        font-size: 1.17rem !important;
    }

    .st-key-historico_seletor_maior div[data-baseweb="select"] div,
    .st-key-historico_seletor_maior div[data-baseweb="select"] span,
    .st-key-historico_seletor_maior div[data-baseweb="select"] input,
    .st-key-historico_seletor_maior [role="combobox"],
    .st-key-historico_seletor_maior [role="combobox"] * {
        font-size: 1.17rem !important;
        line-height: 1.35 !important;
    }

    @media (max-width: 600px) {
        .st-key-acessos_auxiliares div[data-testid="stExpander"] details > summary,
        .st-key-acessos_auxiliares div[data-testid="stExpander"] summary,
        .st-key-acessos_auxiliares div[data-testid="stPopover"] > button,
        .st-key-acessos_auxiliares div[data-testid="stPopover"] button {
            min-height: 3.35rem !important;
            height: 3.35rem !important;
            font-size: .98rem !important;
        }

        .historico-label-maior {
            font-size: 1.16rem !important;
        }

        .st-key-historico_seletor_maior div[data-baseweb="select"] > div {
            min-height: 3.30rem !important;
        }

        .st-key-historico_seletor_maior div[data-baseweb="select"] div,
        .st-key-historico_seletor_maior div[data-baseweb="select"] span,
        .st-key-historico_seletor_maior div[data-baseweb="select"] input,
        .st-key-historico_seletor_maior [role="combobox"],
        .st-key-historico_seletor_maior [role="combobox"] * {
            font-size: 1.20rem !important;
        }
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
    # CARTA_CANONICA_POR_DATA_V1_0_0
    bloco = bloco or {}

    arquivo_app = bloco.get("arquivo_app")
    if arquivo_app:
        rel = Path(str(arquivo_app).replace("\\", "/"))
        caminho = APP_DIR / rel
        if caminho.exists():
            return caminho

    data_documento = str(bloco.get("data_documento") or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", data_documento):
        nome_canonico = f"carta_{data_documento}.pdf"
        for rel in (
            Path("static") / "cartas" / nome_canonico,
            Path("assets") / "cartas" / nome_canonico,
        ):
            caminho = APP_DIR / rel
            if caminho.exists():
                return caminho

    arquivo_fonte = bloco.get("arquivo_fonte")
    if arquivo_fonte:
        rel_fonte = Path(str(arquivo_fonte).replace("\\", "/"))
        caminho = PROJECT_ROOT / rel_fonte
        if caminho.exists():
            return caminho

    return None


def url_carta_estatica(carta, caminho=None):

    """Retorna a URL pública da cópia estática canônica da Carta."""



    carta = carta or {}

    arquivo_app = carta.get("arquivo_app")



    if arquivo_app:

        nome = Path(arquivo_app).name

    elif caminho:

        nome = Path(caminho).name

    else:

        return None



    destino = APP_DIR / "static" / "cartas" / nome



    if not destino.is_file():

        return None



    return f"app/static/cartas/{nome}"









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



        url_estatica = url_carta_estatica(carta, caminho)



        if url_estatica:



            st.link_button(



                "📄 Abrir Carta da Célula em nova aba",



                url_estatica,



            )



            st.caption(



                "A Carta abre em uma nova aba para manter este aplicativo aberto."



            )



        else:



            st.warning(



                "A cópia estática da Carta não foi encontrada. "



                "Reexecute a sincronização de arquivos públicos antes de disponibilizar o app."



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
















# COMPLEMENTARES_SEM_DUPLICAR_OFICIAL_V1_0_0
BOOKS={"genesis":"GEN","exodo":"EXO","levitico":"LEV","numeros":"NUM","deuteronomio":"DEU",
"josue":"JOS","juizes":"JDG","rute":"RUT","1 samuel":"1SA","2 samuel":"2SA","1 reis":"1KI","2 reis":"2KI",
"1 cronicas":"1CH","2 cronicas":"2CH","esdras":"EZR","neemias":"NEH","ester":"EST","jo":"JOB","salmos":"PSA",
"salmo":"PSA","proverbios":"PRO","eclesiastes":"ECC","canticos":"SNG","cantico dos canticos":"SNG",
"isaias":"ISA","jeremias":"JER","lamentacoes":"LAM","ezequiel":"EZK","daniel":"DAN","oseias":"HOS","joel":"JOL",
"amos":"AMO","obadias":"OBA","jonas":"JON","miqueias":"MIC","naum":"NAM","habacuque":"HAB","sofonias":"ZEP",
"ageu":"HAG","zacarias":"ZEC","malaquias":"MAL","mateus":"MAT","marcos":"MRK","lucas":"LUK","joao":"JHN",
"atos":"ACT","romanos":"ROM","1 corintios":"1CO","2 corintios":"2CO","galatas":"GAL","efesios":"EPH",
"filipenses":"PHP","colossenses":"COL","1 tessalonicenses":"1TH","2 tessalonicenses":"2TH","1 timoteo":"1TI",
"2 timoteo":"2TI","tito":"TIT","filemom":"PHM","hebreus":"HEB","tiago":"JAS","1 pedro":"1PE","2 pedro":"2PE",
"1 joao":"1JN","2 joao":"2JN","3 joao":"3JN","judas":"JUD","apocalipse":"REV"}
def _sa(v):
    s=unicodedata.normalize("NFD",str(v or ""))
    return re.sub(r"\s+"," ","".join(c for c in s if unicodedata.category(c)!="Mn")).strip().lower()
def ref_path(v):
    m=re.match(r"^(.+?)\s+(\d+)(?::(\d+)(?:\s*[-–—]\s*(\d+))?)?$",_sa(v))
    if not m or m.group(1) not in BOOKS:return None
    p=f"{BOOKS[m.group(1)]}.{m.group(2)}"
    if m.group(3):p+=f".{m.group(3)}"+(f"-{m.group(4)}" if m.group(4) else "")
    return p
def refs_comp(itens,principal):
    pp=ref_path(principal); out=[]
    for x in (itens or []):
        if not isinstance(x,dict):continue
        rp=ref_path(x.get("referencia"))
        if (pp and rp==pp) or (not pp and _sa(x.get("referencia"))==_sa(principal)):continue
        out.append(x)
    return out
def url_video_generica(url):
    try:p=urlparse(str(url or ""))
    except Exception:return True
    h=(p.netloc or "").lower().replace("www.",""); path=(p.path or "/").rstrip("/").lower()
    return (h=="bibleproject.com" and path in {"","/","/portugues"}) or (h in {"youtube.com","m.youtube.com"} and path in {"","/","/results"})


def render_referencias(itens, versao):
    if not itens:
        st.info("Nenhum outro texto bíblico complementar foi priorizado nesta versão.")
        return
    for item in itens:
        if not isinstance(item, dict):
            st.warning("Referência complementar em formato inesperado; item ignorado."); continue
        referencia=item.get("referencia") or "Referência bíblica"
        st.markdown(f"#### {referencia}")
        if item.get("conexao"): st.write(item["conexao"])
        if item.get("como_usar"): st.markdown(f"**Como usar:** {item['como_usar']}")
        if item.get("pergunta"): st.markdown(f"**Pergunta:** {item['pergunta']}")
        raw=str(item.get("youversion_ref") or "").strip()
        url=raw if raw.lower().startswith(("http://","https://")) else url_youversion(raw or ref_path(referencia),versao)
        if url: st.link_button(f"📖 Ler no YouVersion ({versao.get('sigla','')})",url)
        else: st.caption("Link direto não pôde ser montado com segurança para esta referência.")
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
    # VIDEO_COMPLEMENTAR_LINK_ESPECIFICO_V1_0_0
    if not itens:
        st.info("Nenhum vídeo priorizado nesta versão."); return
    for item in itens:
        if not isinstance(item,dict):
            st.warning("Vídeo complementar em formato inesperado; item ignorado."); continue
        st.markdown(f"#### {item.get('titulo') or 'Vídeo complementar'}")
        if item.get("fonte"): st.caption(item["fonte"])
        if item.get("conexao"): st.write(item["conexao"])
        if item.get("como_usar"): st.markdown(f"**Como usar:** {item['como_usar']}")
        if item.get("pergunta"): st.markdown(f"**Pergunta:** {item['pergunta']}")
        raw=str(item.get("url") or "").strip()
        if raw and not url_video_generica(raw):
            base=url_youtube_canonica(raw)
            try: inicio=int(item.get("inicio_segundos") or 0)
            except (TypeError,ValueError): inicio=0
            direct=adicionar_inicio_youtube(base,inicio)
            if url_video_incorporavel(base):
                try: st.video(base,start_time=inicio)
                except Exception: st.caption("Não foi possível incorporar esta mídia; use o botão abaixo.")
            else: st.caption("Este recurso abre em uma página externa específica.")
            st.link_button("🎞️ Abrir recurso diretamente",direct)
        elif raw: st.warning("O endereço registrado é genérico e foi bloqueado para não abrir um tema incorreto.")
        else: st.caption("Link específico do vídeo ainda não disponível.")
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











def render_fonte_oficial_semana(estudo, carta_ok, transcricao_ok, mensagem_ok, expandir=None, modo=None):



    """Agrupa todas as fontes e conteúdos oficiais em menus lineares e próximos."""



    carta = estudo.get("carta") or {}



    transcricao = estudo.get("transcricao") or {}



    mensagem = estudo.get("mensagem") or {}
    avisos_semana = estudo.get("avisos_semana") or {}



    nucleo_oficial = estudo.get("oficial") or {}



    nucleo_preliminar = estudo.get("preliminar") or {}







    st.subheader("📚 Fonte oficial da semana")



    st.caption(



        "Mensagem, transcrição e Carta ficam reunidas aqui. Itens exclusivos da Carta permanecem "



        "como aguardando quando ela ainda não estiver disponível."



    )







    if modo in (None, "avisos"):
        with st.expander("📢 Avisos da Semana", expanded=(expandir == "avisos")):
            if avisos_semana.get("status") == "disponivel":
                tag("oficial", "FONTE OFICIAL")
                st.caption(
                    "Comunicados oficiais apresentados no mesmo vídeo do culto desta semana. "
                    "Este recurso exibe somente o trecho em vídeo, sem transcrição."
                )

                url_avisos_base = url_youtube_canonica(
                    avisos_semana.get("url") or mensagem.get("url"),
                    avisos_semana.get("video_id") or mensagem.get("video_id"),
                )

                try:
                    inicio_avisos = int(avisos_semana.get("inicio_segundos") or 0)
                except (TypeError, ValueError):
                    inicio_avisos = 0

                try:
                    fim_avisos = int(avisos_semana.get("fim_segundos") or 0)
                except (TypeError, ValueError):
                    fim_avisos = 0

                intervalo_avisos_valido = (
                    bool(url_avisos_base)
                    and inicio_avisos >= 0
                    and fim_avisos > inicio_avisos
                )

                if intervalo_avisos_valido:
                    inicio_avisos_formatado = formatar_segundos(inicio_avisos)
                    fim_avisos_formatado = formatar_segundos(fim_avisos)
                    if inicio_avisos_formatado and fim_avisos_formatado:
                        st.caption(
                            f"Trecho dos avisos: {inicio_avisos_formatado} "
                            f"até {fim_avisos_formatado}."
                        )

                    try:
                        st.video(
                            url_avisos_base,
                            start_time=inicio_avisos,
                            end_time=fim_avisos,
                        )
                    except Exception:
                        st.caption(
                            "Não foi possível incorporar este trecho no navegador; "
                            "use o botão abaixo."
                        )

                    url_avisos_direta = adicionar_inicio_youtube(
                        url_avisos_base,
                        inicio_avisos,
                    )
                    st.link_button(
                        "📢 Abrir avisos no vídeo oficial",
                        url_avisos_direta,
                        use_container_width=False,
                    )
                else:
                    st.warning(
                        "Os Avisos da Semana estão registrados, mas o intervalo "
                        "do vídeo precisa ser revisado."
                    )
            else:
                st.info("⏳ Avisos da Semana ainda não identificados para esta semana.")

    if modo in (None, "mensagem"):
        with st.expander("🎥 Mensagem", expanded=(expandir == "mensagem")):



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







    if modo in (None, "estudo"):
        with st.expander("📝 Transcrição", expanded=(expandir == "transcricao")):

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



    if modo in (None, "carta"):
        with st.expander("📄 Carta da Célula", expanded=(expandir == "carta")):



            if carta_ok:



                tag("oficial", "FONTE OFICIAL")



                nome_carta = carta.get("arquivo") or "Carta da Célula"



                st.markdown(f"**Documento:** {nome_carta}")



                if carta.get("url"):



                    st.link_button("📄 Abrir Carta", carta["url"], use_container_width=False)



                else:



                    caminho = resolver_arquivo_local(carta)



                    if caminho:



                        url_estatica = url_carta_estatica(carta, caminho)



                        if url_estatica:



                            st.link_button(



                                "📄 Abrir Carta em nova aba",



                                url_estatica,



                                use_container_width=False,



                            )



                            st.caption(



                                "A Carta abre em uma nova aba para manter este aplicativo aberto."



                            )



                        else:



                            st.warning(



                                "A cópia estática da Carta não foi encontrada. "



                                "Reexecute a sincronização de arquivos públicos antes de disponibilizar o app."



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







    if modo in (None, "estudo"):
        with st.expander("💡 Ideias centrais", expanded=(expandir == "ideias")):



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







    if modo in (None, "estudo"):
        with st.expander("❓ Perguntas oficiais", expanded=(expandir == "perguntas")):



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







    if modo in (None, "estudo"):
        with st.expander("🎵 Músicas indicadas", expanded=(expandir == "musicas")):



            if carta_ok:



                tag("oficial", "OFICIAL — CARTA")



                render_musicas_oficiais(nucleo_oficial.get("musicas", []))



            else:



                st.info("⏳ Aguardando a Carta da Célula para confirmar as músicas indicadas oficialmente.")







    if modo in (None, "estudo"):
        with st.expander("🎯 Desafio prático", expanded=(expandir == "desafio")):



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

if "estudo_selecionado_rotulo" not in st.session_state:
    st.session_state.estudo_selecionado_rotulo = next(iter(opcoes))

if st.session_state.estudo_selecionado_rotulo not in opcoes:
    st.session_state.estudo_selecionado_rotulo = next(iter(opcoes))

if "nav_mobile_idosos" not in st.session_state:
    st.session_state.nav_mobile_idosos = "inicio"

estudo = opcoes[st.session_state.estudo_selecionado_rotulo]

# V1.0.6 — HISTÓRICO ISOLADO
# A tela de Estudos anteriores é um contexto de navegação independente:
# não mostra tema, texto bíblico, período, status das fontes nem ações do estudo.
nav_mode = st.session_state.get("nav_mobile_idosos", "inicio")

if nav_mode == "historico":
    st.markdown("### 📅 Estudos anteriores")
    rotulos = list(opcoes.keys())
    atual = st.session_state.estudo_selecionado_rotulo
    indice_atual = rotulos.index(atual) if atual in rotulos else 0

    st.markdown(
        '<div class="historico-label-maior">Escolha a semana:</div>',
        unsafe_allow_html=True,
    )
    with st.container(key="historico_seletor_maior"):
        novo_rotulo = st.selectbox(
            "Escolha a semana:",
            options=rotulos,
            index=indice_atual,
            help="A semana atual continua aparecendo primeiro.",
            key="historico_mobile_idosos",
            label_visibility="collapsed",
        )

    if novo_rotulo != st.session_state.estudo_selecionado_rotulo:
        st.session_state.estudo_selecionado_rotulo = novo_rotulo
        st.session_state.nav_mobile_idosos = "inicio"
        st.rerun()

    if st.button("←  VOLTAR AO INÍCIO", key="voltar_historico", use_container_width=True):
        st.session_state.nav_mobile_idosos = "inicio"
        st.rerun()

    st.stop()








# aviso técnico movido para o rodapé



st.markdown(
    f'<div class="periodo-destaque"><strong>Período:</strong> {estudo["periodo"]}</div>',
    unsafe_allow_html=True,
)
carta_ok, transcricao_ok, mensagem_ok = avaliar_estado_fontes(estudo)


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















st.markdown('<div class="mobile-nav-title">O que você quer fazer?</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="mobile-nav-help">Toque em uma opção. Você pode voltar ao início a qualquer momento.</div>',
    unsafe_allow_html=True,
)


if nav_mode == "inicio":
    with st.container(key="menu_grid_3x2"):
        menu_cols = st.columns(6, gap="small")

        with menu_cols[0]:
            with st.container(key="menu_card_avisos"):
                if st.button("AVISOS DA SEMANA", key="nav_avisos", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "avisos"
                    st.rerun()

        with menu_cols[1]:
            with st.container(key="menu_card_mensagem"):
                if st.button("ASSISTIR À MENSAGEM", key="nav_mensagem", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "mensagem"
                    st.rerun()

        with menu_cols[2]:
            with st.container(key="menu_card_carta"):
                if st.button("CARTA DA CÉLULA", key="nav_carta", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "carta"
                    st.rerun()

        with menu_cols[3]:
            with st.container(key="menu_card_estudo"):
                if st.button("ACOMPANHAR O ESTUDO", key="nav_estudo", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "estudo"
                    st.rerun()

        with menu_cols[4]:
            with st.container(key="menu_card_enriquecer"):
                if st.button("ENRIQUECER A DISCUSSÃO", key="nav_enriquecer", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "enriquecer"
                    st.rerun()

        with menu_cols[5]:
            with st.container(key="menu_card_historico"):
                if st.button("ESTUDOS ANTERIORES", key="nav_historico", use_container_width=True):
                    st.session_state.nav_mobile_idosos = "historico"
                    st.rerun()

    st.divider()
    with st.container(key="acessos_auxiliares"):
        col_guia_app, col_avaliacao_app = st.columns(2, gap="small")

        with col_guia_app:
            with st.expander("📘 Como usar este aplicativo — Guia rápido", expanded=False):
                st.write(
                    "Esta versão do guia foi organizada para leitura mais confortável no celular. "
                    "Escolha uma etapa abaixo e siga em sequência."
                )

                guia_png = APP_DIR / "assets" / "guia" / "Guia_Visual_App_Conexoes_Sustentaveis.png"
                guia_pdf = APP_DIR / "assets" / "guia" / "Guia_Visual_App_Conexoes_Sustentaveis.pdf"

                guia_mobile_etapa = st.radio(
                    "Etapas do guia:",
                    [
                        "1. Como começar",
                        "2. Conteúdo Oficial",
                        "3. Conteúdo Complementar",
                        "4. Dicas rápidas",
                    ],
                    index=0,
                    key="guia_mobile_etapa",
                )

                if guia_mobile_etapa == "1. Como começar":
                    st.markdown("#### 1. Como começar")
                    st.markdown(
                        "- Use o **Histórico de Mensagens e Estudos** para consultar a semana atual ou semanas anteriores.\n"
                        "- Abra primeiro a **Fonte oficial da semana**.\n"
                        "- Siga a ordem do estudo apresentada no próprio app.\n"
                        "- Use a **Mensagem**, a **Transcrição** e a **Carta da Célula** como base principal.\n"
                        "- Depois avance para os demais itens oficiais do encontro."
                    )

                    st.markdown("##### 📚 Como funciona o histórico")
                    st.markdown(
                        "- Os estudos e as Cartas anteriores a 09/08/2026 serviram como **referência para calibrar e validar** "
                        "o processo automatizado que identifica novas mensagens do culto de **domingo, às 18h30**.\n"
                        "- A partir da mensagem identificada, o sistema pode produzir material de apoio e "
                        "**conteúdo complementar**, com ou sem uma **Carta da Célula** disponível."
                    )
                    st.warning(
                        "Como parte desse material é produzida com apoio de Inteligência Artificial, "
                        "a revisão e a supervisão humana continuam necessárias antes do uso no encontro."
                    )

                elif guia_mobile_etapa == "2. Conteúdo Oficial":
                    st.markdown("#### 2. Conteúdo Oficial")
                    st.markdown(
                        "Use primeiro os conteúdos oficiais da semana:\n\n"
                        "- **Mensagem**\n"
                        "- **Transcrição**\n"
                        "- **Carta da Célula**\n"
                        "- **Ideias Centrais**\n"
                        "- **Perguntas Oficiais**\n"
                        "- **Músicas Indicadas**\n"
                        "- **Desafio Prático**"
                    )
                    st.success("Esses itens são a base principal do encontro.")

                elif guia_mobile_etapa == "3. Conteúdo Complementar":
                    st.markdown("#### 3. Conteúdo Complementar")
                    st.markdown(
                        "Depois do conteúdo oficial, você pode usar os materiais complementares para enriquecer a conversa:\n\n"
                        "- **Outros textos bíblicos**\n"
                        "- **Filmes**\n"
                        "- **Livros**\n"
                        "- **Músicas**\n"
                        "- **Vídeos animados**\n"
                        "- **Temas na atualidade**"
                    )
                    st.info("O conteúdo complementar amplia a discussão, mas não substitui o conteúdo oficial.")

                else:
                    st.markdown("#### 4. Dicas rápidas")
                    st.markdown(
                        "- No celular, a **Carta da Célula** pode abrir separadamente. Para voltar, retorne ao app no navegador.\n"
                        "- Nem toda semana terá todos os itens disponíveis no mesmo momento.\n"
                        "- Quando houver Carta, o tema deve estar alinhado à semana correspondente.\n"
                        "- Ao final do uso, responda a **Avaliação do app**."
                    )
                    st.warning("Se algum item ainda não estiver disponível, siga normalmente com o restante do estudo.")

                st.divider()

                with st.expander("🖼️ Ver versão visual resumida", expanded=False):
                    if guia_png.is_file():
                        st.image(
                            str(guia_png),
                            caption="Guia Visual resumido do App Conexões Sustentáveis",
                            use_container_width=True,
                        )
                    else:
                        st.info("A versão visual resumida ainda não está disponível neste ambiente.")

                if guia_pdf.is_file():
                    st.download_button(
                        "📄 Baixar guia em PDF",
                        data=guia_pdf.read_bytes(),
                        file_name="Guia_Visual_App_Conexoes_Sustentaveis.pdf",
                        mime="application/pdf",
                        use_container_width=False,
                    )
                else:
                    st.info("O PDF do guia ainda não está disponível neste ambiente.")

        with col_avaliacao_app:
            with st.popover("📝 Avaliação do app", use_container_width=True):
                st.write("Sua opinião ajuda a melhorar este aplicativo.")
                st.markdown("**Escolha seu perfil:**")
                st.link_button(
                    "👥 Sou Líder de Célula",
                    "https://forms.gle/SVBxwBspJj4osbhBA",
                    use_container_width=True,
                )
                st.link_button(
                    "🙋 Sou Membro de Célula",
                    "https://forms.gle/CDDAnigyCTzQ8qNP7",
                    use_container_width=True,
                )

    st.caption(
        "Conexões Sustentáveis • Extensão II • "
        "Conteúdo complementar sujeito a revisão humana."
    )
    st.stop()


if st.button("←  VOLTAR AO INÍCIO", key=f"voltar_{nav_mode}", use_container_width=True):
    st.session_state.nav_mobile_idosos = "inicio"
    st.rerun()

expandir_por_modo = {
    "avisos": "avisos",
    "mensagem": "mensagem",
    "carta": "carta",
    "estudo": None,
}

if nav_mode in expandir_por_modo:
    render_fonte_oficial_semana(
        estudo,
        carta_ok,
        transcricao_ok,
        mensagem_ok,
        expandir=expandir_por_modo[nav_mode],
        modo=nav_mode,
    )
    st.stop()

# nav_mode == "enriquecer": segue para o bloco complementar existente.







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



    st.caption("Conexões Sustentáveis • Extensão II • MVP 04D.4.2 • Conteúdo complementar sujeito a revisão humana.")



    st.stop()







st.divider()



st.subheader("🔎 Enriquecendo a discussão")
st.caption("Conteúdo complementar separado das fontes oficiais. Quando a Carta estiver pendente, o material é preliminar e deve ser conciliado depois.")
st.subheader("⭐ Recursos prioritários para este encontro")



tag("prioridade", "CURADORIA 04D.4.2")



for item in estudo.get("prioridades", []):



    if isinstance(item, dict):



        recurso = item.get("recurso") or "Recurso complementar"



        motivo = item.get("motivo") or ""



        st.markdown(f"**{recurso}**" + (f" — {motivo}" if motivo else ""))



    else:



        st.markdown(f"• {item}")







st.divider()



with st.expander("📖 Outros textos bíblicos", expanded=False):



    tag("biblico", "BÍBLICO")



    render_referencias(refs_comp(estudo.get("referencias_biblicas", []), estudo.get("texto_principal")), versao)







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

st.subheader("📝 Avaliação do app")

st.write(

    "Sua avaliação ajuda a verificar se os recursos utilizados contribuíram "

    "para a compreensão, participação e aplicação do tema."

)



with st.popover("📝 Responder avaliação", use_container_width=True):

    st.markdown("**Escolha seu perfil:**")



    st.link_button(

        "👥 Sou Líder de Célula",

        "https://forms.gle/SVBxwBspJj4osbhBA",

        use_container_width=True,

    )



    st.link_button(

        "🙋 Sou Membro de Célula",

        "https://forms.gle/CDDAnigyCTzQ8qNP7",

        use_container_width=True,

    )



st.divider()



st.caption("Conexões Sustentáveis • Extensão II • MVP 04D.4.2 • Conteúdo complementar sujeito a revisão humana.")



