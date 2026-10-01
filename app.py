"""Professional Streamlit portfolio for Avaneesh Singh."""

from __future__ import annotations

import base64
import os
import re
import smtplib
from email.message import EmailMessage
from html import escape
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(
    page_title="Avaneesh Singh | Python Developer",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Public portfolio configuration. Keep credentials in .streamlit/secrets.toml.
# -----------------------------------------------------------------------------
PROFILE_NAME = "Avaneesh Singh"
LINKEDIN_URL = "https://www.linkedin.com/in/avaneeshsingh3/"
GITHUB_URL = ""
EMAIL = ""

INTELLAIR_LIVE_URL = "https://intelliaiprolive-bja4wx5haxitsvvpb4hvuc.streamlit.app/"
INTELLAIR_GITHUB_URL = ""

PROFILE_IMAGE = "assets/profile.jpg"
RESUME_PATH = "assets/resume.pdf"
INTELLAIR_IMAGE = "images/intelliair-pro.png"

NAV_PAGES = (
    "Home",
    "About",
    "Skills",
    "Projects",
    "Education",
    "Certifications",
    "Resume",
    "Contact",
)
NAVIGATION_KEY = "page"
ROOT = Path(__file__).resolve().parent
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

NAV_ICONS = {
    "Home": "home",
    "About": "user",
    "Skills": "code",
    "Projects": "layers",
    "Education": "graduation-cap",
    "Certifications": "certificate",
    "Resume": "file-text",
    "Contact": "mail",
}

NAV_BUTTON_LABELS = {
    "Home": ":material/home: Home",
    "About": ":material/person: About",
    "Skills": ":material/code: Skills",
    "Projects": ":material/layers: Projects",
    "Education": ":material/school: Education",
    "Certifications": ":material/workspace_premium: Certifications",
    "Resume": ":material/description: Resume",
    "Contact": ":material/mail: Contact",
}

SVG_PATHS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1Z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "code": '<path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    "graduation-cap": '<path d="m2 9 10-5 10 5-10 5Z"/><path d="M6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
    "certificate": '<path d="M7 3h10l4 4v14H7Z"/><path d="M17 3v5h4M10 13h6M10 17h4"/><circle cx="16.5" cy="17.5" r="2.5"/>',
    "lightbulb": '<path d="M9 18h6M10 22h4M8 14c-1.5-1.3-2.5-3.2-2.5-5.3a6.5 6.5 0 0 1 13 0c0 2.1-1 4-2.5 5.3-.9.8-1.5 1.6-1.5 3H9.5c0-1.4-.6-2.2-1.5-3Z"/>',
    "file-text": '<path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v5h4M9 13h6M9 17h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>',
    "linkedin": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 10v6M8 7.5v.01M12 16v-3.4a2.6 2.6 0 0 1 5.2 0V16M12 10v6"/>',
    "github": '<path fill="currentColor" stroke="none" d="M12 2C6.48 2 2 6.58 2 12.23c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.49 0-.24-.01-1.05-.01-1.9-2.78.62-3.37-1.21-3.37-1.21-.46-1.19-1.11-1.5-1.11-1.5-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.86.09-.67.35-1.12.64-1.38-2.22-.26-4.56-1.15-4.56-5.09 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.73 0 0 .84-.27 2.75 1.05A9.3 9.3 0 0 1 12 6.82c.85 0 1.71.12 2.51.34 1.91-1.32 2.75-1.05 2.75-1.05.55 1.42.2 2.47.1 2.73.64.72 1.03 1.63 1.03 2.75 0 3.95-2.34 4.82-4.57 5.08.36.32.68.94.68 1.89 0 1.37-.01 2.47-.01 2.81 0 .27.18.59.69.49A10.23 10.23 0 0 0 22 12.23C22 6.58 17.52 2 12 2Z"/>',
}


def asset_path(relative_path: str) -> Path:
    """Return a project-rooted path for a configured public asset."""
    return ROOT / relative_path


def read_binary(relative_path: str) -> bytes | None:
    """Safely read an optional asset without crashing the application."""
    try:
        return asset_path(relative_path).read_bytes()
    except OSError:
        return None


def image_data_uri(relative_path: str) -> str | None:
    """Return a local image data URI for the custom profile frame."""
    image = read_binary(relative_path)
    if not image:
        return None

    extension = asset_path(relative_path).suffix.lower()
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(extension, "image/jpeg")
    return f"data:{mime_type};base64,{base64.b64encode(image).decode('ascii')}"


def render_icon(name: str, label: str = "") -> str:
    """Return a small, reusable outline SVG icon for navigation and links."""
    paths = SVG_PATHS.get(name, SVG_PATHS["code"])
    accessible_name = f'<title>{escape(label)}</title>' if label else ""
    aria_hidden = "false" if label else "true"
    return (
        f'<svg class="ui-icon ui-icon-{escape(name)}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="{aria_hidden}">'
        f"{accessible_name}{paths}</svg>"
    )


def render_logo() -> str:
    """Render the portfolio brand with a custom SVG A mark."""
    return """
        <div class="portfolio-brand" aria-label="Avaneesh portfolio">
            <span class="brand-mark" aria-hidden="true">
                <svg viewBox="0 0 44 44" fill="none">
                    <path d="M8 34 20.4 8h3.3L36 34" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M14.5 23.5h15" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
                    <path d="M30.5 10.5 36 22" stroke="#b68cff" stroke-width="4" stroke-linecap="round"/>
                </svg>
            </span>
            <span class="brand-copy"><strong>AVANEESH</strong><span>/ PORTFOLIO</span></span>
        </div>
    """


def configured_public_email() -> str:
    """Use a deliberately public email first, then an existing email receiver secret."""
    if EMAIL:
        return EMAIL.strip()
    try:
        return str(st.secrets["email"]["receiver"]).strip()
    except (KeyError, FileNotFoundError, TypeError):
        return ""


def render_social_button(name: str, label: str, url: str) -> str:
    """Render one compact social control without creating a Streamlit widget."""
    icon_markup = render_icon(name)
    label_markup = f'<span class="sr-only">{escape(label)}</span>'
    if url:
        target = ' target="_blank" rel="noopener noreferrer"' if not url.startswith("mailto:") else ""
        return f'<a class="social-button" href="{escape(url, quote=True)}"{target} aria-label="{escape(label)}">{icon_markup}{label_markup}</a>'
    return f'<span class="social-button is-disabled" aria-label="{escape(label)} unavailable" title="{escape(label)} unavailable">{icon_markup}{label_markup}</span>'


def icon(name: str) -> str:
    """Render a Font Awesome icon in custom HTML components."""
    return f'<i class="fa-solid {name}" aria-hidden="true"></i>'


def tags(values: list[str]) -> str:
    return "".join(f'<span class="tag">{value}</span>' for value in values)


def load_css() -> None:
    """Load the dark glassmorphism visual system used on every page."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
        <style>
            :root { --bg:#080b12; --card:#111827; --primary:#38bdf8; --secondary:#818cf8; --text:#f8fafc; --muted:#94a3b8; }
            html, body { background:var(--bg); }
            [data-testid="stAppViewContainer"], .stApp {
                background:radial-gradient(circle at 8% 8%,rgba(56,189,248,.14),transparent 23rem),
                           radial-gradient(circle at 90% 14%,rgba(99,102,241,.15),transparent 25rem),var(--bg);
                color:var(--text); font-family:"Manrope",sans-serif;
            }
            #MainMenu, header, footer { visibility:hidden; }
            .block-container { max-width:1240px; padding:1.55rem 2rem 3.5rem; }
            .st-key-navbar { position:relative; max-width:1180px; margin:0 auto 2.8rem; padding:.6rem .72rem .6rem 1rem; overflow:hidden; border:1px solid transparent; border-radius:22px; background:linear-gradient(135deg,rgba(13,22,38,.9),rgba(10,14,27,.84)) padding-box,linear-gradient(105deg,rgba(49,214,255,.82),rgba(139,92,246,.52) 50%,rgba(205,123,255,.85)) border-box; box-shadow:-18px 0 42px rgba(35,205,255,.17),18px 0 45px rgba(169,91,255,.16),inset 0 1px 0 rgba(255,255,255,.05); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); }
            .st-key-navbar::before { content:""; position:absolute; inset:0; pointer-events:none; background:linear-gradient(95deg,rgba(61,219,255,.09),transparent 26%,transparent 70%,rgba(180,99,255,.1)); }
            .st-key-navbar > div { position:relative; z-index:1; }
            .portfolio-brand { position:relative; z-index:1; }
            .portfolio-brand { display:inline-flex; flex:0 0 auto; align-items:center; gap:.65rem; color:var(--text); text-decoration:none; }
            .brand-mark { display:grid; place-items:center; width:2.42rem; height:2.42rem; border:1px solid rgba(85,220,255,.58); border-radius:11px; color:#59ddff; background:linear-gradient(145deg,rgba(53,211,255,.18),rgba(131,74,235,.12)); box-shadow:0 0 20px rgba(47,210,255,.24),inset 0 0 13px rgba(109,206,255,.1); }
            .brand-mark svg { width:1.65rem; height:1.65rem; }
            .brand-copy { display:flex; align-items:baseline; gap:.36rem; font:600 .72rem "DM Mono",monospace; letter-spacing:.105em; white-space:nowrap; }
            .brand-copy strong { color:#effbff; font-weight:500; }
            .brand-copy span { color:#aab8ca; }
            .st-key-navbar [class*="st-key-nav_"] { min-width:0; }
            .st-key-navbar [class*="st-key-nav_"] button { display:flex; align-items:center; justify-content:center; gap:.32rem; width:100%; min-height:2.15rem; padding:.5rem .42rem; border:1px solid transparent; border-radius:10px; color:#9caabd !important; background:transparent; font-family:"Manrope",sans-serif; font-size:.635rem; font-weight:800; line-height:1; letter-spacing:.015em; white-space:nowrap; transition:color .2s ease,background .2s ease,border-color .2s ease,box-shadow .2s ease,transform .2s ease; }
            .st-key-navbar [class*="st-key-nav_"] button:hover { color:#83e9ff !important; border-color:rgba(77,218,255,.25); background:rgba(55,206,255,.08); box-shadow:0 0 18px rgba(49,212,255,.12); transform:translateY(-1px); }
            .st-key-navbar [class*="st-key-nav_"] button span[data-testid="stIconMaterial"] { font-size:.94rem; }
            .ui-icon { display:block; flex:0 0 auto; }
            .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
            .page-eyebrow { margin:0 0 .75rem; color:var(--primary); font:500 .74rem "DM Mono",monospace; letter-spacing:.15em; text-transform:uppercase; }
            .page-title { max-width:900px; margin:0; color:var(--text); font-size:clamp(2.25rem,5vw,4.2rem); line-height:1.04; letter-spacing:-.065em; font-weight:800; }
            .page-title span { background:linear-gradient(100deg,var(--primary),#a5b4fc); -webkit-background-clip:text; background-clip:text; color:transparent; }
            .page-copy { max-width:710px; margin:1.2rem 0 0; color:var(--muted); font-size:1rem; line-height:1.85; }
            .hero { padding:0 0 1rem; }
            .hero-title { margin:0; color:var(--text); font-size:clamp(3.25rem,7vw,6.25rem); line-height:.95; letter-spacing:-.08em; font-weight:800; }
            .hero-title span { background:linear-gradient(100deg,var(--primary),#a5b4fc); -webkit-background-clip:text; background-clip:text; color:transparent; }
            .hero-role { margin:1.5rem 0 .8rem; color:#d9e6f1; font-size:clamp(1rem,2vw,1.22rem); font-weight:700; }
            .availability { display:inline-flex; align-items:center; gap:.5rem; margin-top:1.35rem; padding:.5rem .75rem; border:1px solid rgba(56,189,248,.27); border-radius:999px; color:#baecfd; background:rgba(56,189,248,.07); font:500 .7rem "DM Mono",monospace; letter-spacing:.06em; }
            .status-dot { width:.45rem; height:.45rem; border-radius:50%; background:#5eead4; box-shadow:0 0 0 .25rem rgba(94,234,212,.1); }
            .profile-shell { position:relative; width:min(100%,330px); aspect-ratio:1; margin:0 auto; padding:7px; overflow:hidden; border-radius:35px; background:linear-gradient(135deg,rgba(56,189,248,.95),rgba(99,102,241,.95),rgba(56,189,248,.25)); box-shadow:0 28px 80px rgba(0,0,0,.38); }
            .profile-shell::after { content:""; position:absolute; inset:0; pointer-events:none; background:linear-gradient(140deg,transparent 45%,rgba(255,255,255,.14)); }
            .profile-image { width:100%; height:100%; border-radius:29px; object-fit:cover; background:#101928; }
            .profile-placeholder { display:grid; place-items:center; width:100%; height:100%; border-radius:29px; color:#c8edfc; background:linear-gradient(145deg,#111827,#172554); font-size:4.1rem; font-weight:800; }
            .social-row { display:flex; align-items:center; gap:.68rem; margin-top:1.65rem; }
            .social-button { display:grid; place-items:center; width:2.7rem; height:2.7rem; box-sizing:border-box; border:1px solid rgba(65,208,255,.44); border-radius:11px; color:#e8faff !important; background:linear-gradient(145deg,rgba(20,36,57,.84),rgba(13,18,33,.9)); box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 0 16px rgba(46,202,255,.1); text-decoration:none; transition:transform .2s ease,border-color .2s ease,color .2s ease,box-shadow .2s ease,background .2s ease; }
            .social-button .ui-icon { width:1.18rem; height:1.18rem; }
            .social-button:hover { border-color:#67e5ff; color:#74e9ff !important; background:rgba(31,77,108,.76); box-shadow:0 0 23px rgba(43,214,255,.3),0 0 26px rgba(161,96,255,.12); transform:translateY(-2px); }
            .social-button.is-disabled { cursor:not-allowed; opacity:.4; }
            .button-row { display:flex; flex-wrap:wrap; gap:.75rem; margin-top:1.65rem; }
            .button-link { display:inline-flex; align-items:center; justify-content:center; min-height:2.9rem; box-sizing:border-box; padding:.7rem 1rem; border:1px solid rgba(56,189,248,.45); border-radius:10px; color:#07111a !important; background:linear-gradient(110deg,#67d5fa,#8aa1ff); font-size:.84rem; font-weight:800; text-decoration:none; transition:transform .18s ease,box-shadow .18s ease; }
            .button-link.ghost { color:#dff5ff !important; background:rgba(17,24,39,.68); border-color:rgba(148,163,184,.22); }
            .button-link:hover { transform:translateY(-2px); box-shadow:0 13px 30px rgba(56,189,248,.18); }
            div.stButton > button, div.stDownloadButton > button, div.stFormSubmitButton > button { min-height:2.9rem; border:1px solid rgba(56,189,248,.42); border-radius:10px; color:#dff7ff; background:rgba(17,24,39,.7); font-family:"Manrope",sans-serif; font-size:.84rem; font-weight:800; transition:transform .18s ease,background .18s ease; }
            div.stButton > button:hover, div.stDownloadButton > button:hover, div.stFormSubmitButton > button:hover { color:#061019; border-color:var(--primary); background:var(--primary); transform:translateY(-2px); }
            .section-space { height:2.15rem; }
            .content-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1.125rem; align-items:stretch; }
            .skills-grid, .project-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1.125rem; align-items:stretch; }
            .cert-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1.125rem; align-items:stretch; }
            .glass-card, .feature-panel, .cert-card, .education-card, .project-card { position:relative; display:flex; flex-direction:column; height:100%; min-height:200px; box-sizing:border-box; padding:1.35rem; overflow:hidden; border:1px solid rgba(80,180,255,.18); border-radius:16px; background:rgba(12,22,40,.75); box-shadow:0 8px 30px rgba(0,0,0,.20); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease; }
            .glass-card::before, .cert-card::before, .project-card::before { content:""; position:absolute; inset:0; pointer-events:none; background:linear-gradient(135deg,rgba(75,210,255,.08),transparent 35%,transparent 72%,rgba(139,92,246,.07)); }
            .glass-card:hover, .feature-panel:hover, .cert-card:hover, .education-card:hover, .project-card:hover { transform:translateY(-3px); border-color:rgba(78,205,255,.43); box-shadow:0 15px 35px rgba(0,0,0,.25),0 0 24px rgba(71,192,255,.10); }
            .card-icon { position:relative; z-index:1; display:grid; place-items:center; width:2.45rem; height:2.45rem; margin-bottom:1rem; border:1px solid rgba(82,209,255,.15); border-radius:10px; color:#69dcff; background:rgba(56,189,248,.08); font-size:.95rem; }
            .card-title { position:relative; z-index:1; margin:0 0 .6rem; color:var(--text); font-size:1rem; font-weight:800; }
            .card-text { position:relative; z-index:1; margin:0; color:var(--muted); font-size:.89rem; line-height:1.75; }
            .card-corner { position:relative; z-index:1; display:grid; place-items:center; width:1.8rem; height:1.8rem; margin-top:auto; margin-left:auto; border:1px solid rgba(108,219,255,.15); border-radius:8px; color:#8ce9ff; background:rgba(56,189,248,.06); font-size:.7rem; }
            .tag { position:relative; z-index:1; display:inline-block; margin:0 .32rem .42rem 0; padding:.38rem .6rem; border:1px solid rgba(80,190,255,.2); border-radius:999px; color:#c9effd; background:rgba(56,189,248,.065); font:400 .7rem "DM Mono",monospace; }
            .skills-card { min-height:196px; }
            .skills-card .card-icon { margin-bottom:.85rem; }
            .featured-project { display:grid; grid-template-columns:minmax(0,1.03fr) minmax(0,.97fr); overflow:hidden; border:1px solid rgba(85,195,255,.24); border-radius:18px; background:rgba(12,22,40,.77); box-shadow:0 12px 35px rgba(0,0,0,.23); }
            .featured-visual { position:relative; min-height:410px; overflow:hidden; background:radial-gradient(circle at 25% 20%,rgba(47,193,255,.18),transparent 42%),#0c1727; }
            .featured-visual::after { content:""; position:absolute; inset:0; pointer-events:none; background:linear-gradient(135deg,rgba(19,229,255,.10),transparent 42%,rgba(151,89,245,.10)); }
            .featured-visual img { display:block; width:100%; height:100%; object-fit:cover; }
            .project-placeholder { display:grid; place-items:center; height:100%; min-height:410px; padding:2rem; box-sizing:border-box; color:var(--muted); text-align:center; }
            .project-placeholder i { display:block; margin-bottom:.85rem; color:var(--primary); font-size:3rem; }
            .feature-panel { min-height:410px; border:0; border-radius:0; background:transparent; box-shadow:none; }
            .feature-panel:hover { transform:none; border-color:transparent; box-shadow:none; }
            .feature-badge { position:relative; z-index:1; display:inline-block; align-self:flex-start; margin-bottom:1rem; padding:.35rem .58rem; border:1px solid rgba(76,211,255,.22); border-radius:6px; color:#76e0ff; background:rgba(56,189,248,.09); font:500 .66rem "DM Mono",monospace; letter-spacing:.1em; }
            .feature-title { position:relative; z-index:1; margin:0 0 .8rem; color:var(--text); font-size:clamp(1.9rem,3vw,2.55rem); letter-spacing:-.05em; }
            .feature-list { position:relative; z-index:1; display:grid; grid-template-columns:1fr 1fr; gap:.62rem .9rem; margin:1.25rem 0; padding:0; list-style:none; color:#cbd8e5; font-size:.83rem; }
            .feature-list li::before { content:"→"; margin-right:.45rem; color:var(--primary); }
            .feature-panel .button-link { position:relative; z-index:1; align-self:flex-start; margin-top:auto; }
            .project-card { min-height:205px; }
            .timeline { position:relative; display:grid; gap:1rem; max-width:940px; margin:0; padding:0; border:0; }
            .timeline-item { position:relative; min-height:102px; padding:1.15rem 1.25rem 1.15rem 4.1rem; border:1px solid rgba(80,180,255,.18); border-radius:16px; background:rgba(12,22,40,.75); box-shadow:0 8px 30px rgba(0,0,0,.20); }
            .timeline-item::before { content:""; position:absolute; top:1.2rem; left:1.25rem; width:.78rem; height:.78rem; border:4px solid rgba(11,22,38,.95); border-radius:50%; background:linear-gradient(135deg,#55ddff,#a78bfa); box-shadow:0 0 18px rgba(56,189,248,.5); }
            .timeline-item:not(:last-child)::after { content:""; position:absolute; top:2.3rem; bottom:-1.25rem; left:1.61rem; width:1px; background:linear-gradient(#57dfff,rgba(147,99,255,.32)); }
            .timeline-degree { color:var(--text); font-size:1.06rem; font-weight:800; }
            .timeline-place { margin-top:.32rem; color:#70dcff; font-size:.9rem; font-weight:700; }
            .cert-card { min-height:185px; margin:0; }
            .cert-org { position:relative; z-index:1; margin:0; color:#73dcff; font-size:.83rem; }
            .cert-indicator { position:relative; z-index:1; display:flex; align-items:center; gap:.38rem; margin-top:auto; padding-top:1rem; color:#a8c2d8; font:500 .65rem "DM Mono",monospace; letter-spacing:.06em; text-transform:uppercase; }
            .cert-indicator i { color:#8ce9ff; }
            .resume-panel { padding:1.8rem; border:1px solid rgba(56,189,248,.2); border-radius:18px; background:linear-gradient(120deg,rgba(18,37,58,.85),rgba(17,24,39,.85)); }
            .contact-item { display:flex; align-items:center; gap:.7rem; padding:.75rem; margin-top:.75rem; border:1px solid rgba(148,163,184,.1); border-radius:10px; color:#cbd8e5; text-decoration:none; font-size:.85rem; }
            .contact-item i { color:var(--primary); }
            [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { border:1px solid rgba(148,163,184,.2); border-radius:9px; color:var(--text); background:rgba(8,11,18,.55); }
            [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus { border-color:var(--primary); box-shadow:0 0 0 1px var(--primary); }
            label, [data-testid="stWidgetLabel"] p { color:#c8d6e5 !important; font-size:.85rem !important; }
            .site-footer { margin-top:5rem; padding-top:1.8rem; border-top:1px solid rgba(148,163,184,.12); color:#71839a; text-align:center; font-size:.8rem; line-height:1.8; }
            .site-footer strong { color:#cbd9e8; }
            @media (max-width: 760px) {
                .block-container { padding:1.25rem 1.25rem 3rem; }
                .st-key-navbar { margin-bottom:2.35rem; padding:.75rem; border-radius:18px; }
                .st-key-navbar [class*="st-key-nav_"] button { min-height:2.1rem; padding:.46rem .42rem; font-size:.62rem; }
                .hero { padding-top:0; }
                .profile-shell { width:240px; margin-top:1.8rem; }
                .feature-list { grid-template-columns:1fr; }
                .button-row { gap:.55rem; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_heading(eyebrow: str, title: str, accent: str, copy: str) -> None:
    st.markdown(
        f"""
        <p class="page-eyebrow">{eyebrow}</p>
        <h1 class="page-title">{title} <span>{accent}</span></h1>
        <p class="page-copy">{copy}</p>
        """,
        unsafe_allow_html=True,
    )


def select_page(page: str) -> None:
    """Set the current internal portfolio page without navigating away."""
    st.session_state.page = page


def render_active_nav_style(page: str) -> None:
    """Apply the existing glowing active treatment to the selected nav button."""
    nav_key = f"nav_{page.lower()}"
    st.markdown(
        f"""
        <style>
            .st-key-navbar .st-key-{nav_key} button {{
                position:relative;
                color:#effcff !important;
                border-color:rgba(82,218,255,.58) !important;
                background:linear-gradient(110deg,rgba(42,198,255,.18),rgba(130,90,241,.18)) !important;
                box-shadow:inset 0 0 14px rgba(71,214,255,.12),0 0 19px rgba(72,208,255,.14) !important;
            }}
            .st-key-navbar .st-key-{nav_key} button::after {{
                content:"";
                position:absolute;
                right:.55rem;
                bottom:.18rem;
                left:.55rem;
                height:1.5px;
                border-radius:999px;
                background:linear-gradient(90deg,#54e4ff,#b991ff);
                box-shadow:0 0 9px #54e4ff;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def navbar_container():
    """Create the styled navbar container, including older Streamlit fallback."""
    try:
        return st.container(key="navbar")
    except TypeError:
        return st.container()


def navbar_columns():
    """Create compact nav columns with a safe fallback for older Streamlit APIs."""
    try:
        return st.columns(len(NAV_PAGES), gap=None)
    except TypeError:
        return st.columns(len(NAV_PAGES), gap="small")


def render_navbar() -> str:
    """Render same-tab Streamlit navigation and keep its selected page in state."""
    if NAVIGATION_KEY not in st.session_state:
        st.session_state.page = "Home"

    selected_page = st.session_state.page
    render_active_nav_style(selected_page)

    with navbar_container():
        brand_column, navigation_column = st.columns([1.35, 5.65], gap="small")
        with brand_column:
            st.markdown(render_logo(), unsafe_allow_html=True)
        with navigation_column:
            nav_columns = navbar_columns()
            for column, page in zip(nav_columns, NAV_PAGES):
                with column:
                    st.button(
                        NAV_BUTTON_LABELS[page],
                        key=f"nav_{page.lower()}",
                        on_click=select_page,
                        args=(page,),
                        use_container_width=True,
                    )
    return selected_page


def resume_download(label: str, key: str, container_width: bool = False) -> None:
    """Display a uniquely keyed resume download or a graceful unavailable state."""
    resume = read_binary(RESUME_PATH)
    if resume:
        st.download_button(
            label,
            data=resume,
            file_name="Avaneesh_Singh_Resume.pdf",
            mime="application/pdf",
            key=key,
            use_container_width=container_width,
        )
    else:
        st.button(
            "Resume unavailable",
            disabled=True,
            key=f"{key}_unavailable",
            use_container_width=container_width,
        )


def home_section() -> None:
    """Render the landing hero and compact contact controls."""
    text_column, image_column = st.columns([1.25, .75], gap="large")
    with text_column:
        st.markdown(
            """
            <section class="hero">
                <p class="page-eyebrow">Hi, I'm</p>
                <h1 class="hero-title">AVANEESH<br><span>SINGH</span></h1>
                <p class="hero-role">Python Developer | Software Developer | MCA Graduate</p>
                <p class="page-copy">I build practical software applications using Python, databases, APIs and modern development technologies.</p>
                <div class="availability"><span class="status-dot"></span> OPEN TO OPPORTUNITIES</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        public_email = configured_public_email()
        email_url = f"mailto:{quote(public_email, safe='@+._-')}" if public_email else ""
        st.markdown(
            '<div class="social-row">'
            f'{render_social_button("linkedin", "LinkedIn", LINKEDIN_URL)}'
            f'{render_social_button("github", "GitHub", GITHUB_URL)}'
            f'{render_social_button("mail", "Gmail", email_url)}'
            "</div>",
            unsafe_allow_html=True,
        )
    with image_column:
        profile_data = image_data_uri(PROFILE_IMAGE)
        if profile_data:
            st.markdown(
                f'<div class="profile-shell"><img class="profile-image" src="{profile_data}" alt="{PROFILE_NAME} profile photograph"></div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("Profile image is unavailable. Add assets/profile.jpg to show it here.")
            st.markdown('<div class="profile-shell"><div class="profile-placeholder">AS</div></div>', unsafe_allow_html=True)


def about_section() -> None:
    page_heading(
        "About me",
        "A practical",
        "developer mindset.",
        "I am an MCA graduate interested in building useful software while continuously strengthening my foundations in programming, databases and modern web technologies.",
    )
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    cards = [
        ("fa-graduation-cap", "MCA Background", "MCA graduate with an academic foundation in computing and modern development technologies."),
        ("fa-book-open", "BCA Background", "BCA background from the University of Allahabad."),
        ("fa-code", "Python & Software Development", "Interested in practical Python applications, problem solving and software development."),
        ("fa-database", "Databases & APIs", "Developing with databases, API integration and data-focused application workflows."),
        ("fa-arrow-trend-up", "Continuous Learning", "Growing technical skills through structured learning, certifications and hands-on projects."),
    ]
    for start in range(0, len(cards), 3):
        columns = st.columns(3, gap="medium")
        for column, (symbol, title, description) in zip(columns, cards[start:start + 3]):
            with column:
                st.markdown(f'<article class="glass-card"><div class="card-icon">{icon(symbol)}</div><h2 class="card-title">{title}</h2><p class="card-text">{description}</p></article>', unsafe_allow_html=True)


def skills_section() -> None:
    page_heading("Technical toolkit", "Skills built for", "practical delivery.", "A focused collection of programming, tooling, data and security interests that supports hands-on software development.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    groups = [
        ("Programming", ["Python", "SQL", "HTML", "CSS", "JavaScript"]),
        ("Frameworks & Tools", ["Streamlit", "Git", "GitHub", "VS Code"]),
        ("Databases", ["MongoDB", "MySQL"]),
        ("Other", ["REST APIs", "API Integration", "Data Processing", "Data Visualization", "Data Science", "Machine Learning", "Cybersecurity"]),
    ]
    for start in range(0, len(groups), 2):
        columns = st.columns(2, gap="medium")
        for column, (title, values) in zip(columns, groups[start:start + 2]):
            with column:
                st.markdown(f'<article class="glass-card"><div class="card-icon">{icon("fa-layer-group")}</div><h2 class="card-title">{title}</h2><div>{tags(values)}</div></article>', unsafe_allow_html=True)
        if start + 2 < len(groups):
            st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)


def projects_section() -> None:
    page_heading("Selected work", "Projects with", "purpose.", "A collection of practical Python work, led by an interactive weather and environmental insights application.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    image_column, content_column = st.columns([1, 1], gap="large")
    with image_column:
        if asset_path(INTELLAIR_IMAGE).is_file():
            st.image(str(asset_path(INTELLAIR_IMAGE)), use_container_width=True)
        else:
            st.warning("Project image is unavailable. Add images/intelliair-pro.png to show it here.")
            st.markdown(f'<div class="project-placeholder"><div>{icon("fa-cloud-sun")}<strong>IntelliAir Pro</strong><br><span>Add images/intelliair-pro.png to display the project visual.</span></div></div>', unsafe_allow_html=True)
    with content_column:
        st.markdown(
            f"""
            <article class="feature-panel">
                <span class="feature-badge">FEATURED PROJECT</span>
                <h2 class="feature-title">IntelliAir Pro</h2>
                <p class="card-text">IntelliAir Pro is a Python and Streamlit-based application designed to provide interactive weather and environmental insights through a user-friendly dashboard.</p>
                <div style="margin-top:1.15rem">{tags(["Python", "Streamlit", "MongoDB", "APIs", "Data Visualization"])}</div>
                <ul class="feature-list"><li>Interactive dashboard</li><li>Weather information</li><li>Environmental insights</li><li>API integration</li><li>Data visualization</li><li>MongoDB integration</li></ul>
                <a class="button-link" href="{INTELLAIR_LIVE_URL}" target="_blank" rel="noopener noreferrer">{icon("fa-arrow-up-right-from-square")} Live Demo</a>
            </article>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('<div style="height:1.25rem"></div>', unsafe_allow_html=True)
    columns = st.columns(2, gap="medium")
    projects = [
        ("fa-hospital", "Hospital Management System", "A CLI-based hospital management application designed to manage hospital-related records and operations.", ["CLI-based", "Python"]),
        ("fa-terminal", "Python Applications", "Python-based academic and personal applications focused on practical programming and problem solving.", ["Python"]),
    ]
    for column, (symbol, title, description, project_tags) in zip(columns, projects):
        with column:
            st.markdown(f'<article class="glass-card"><div class="card-icon">{icon(symbol)}</div><h2 class="card-title">{title}</h2><p class="card-text">{description}</p><div style="margin-top:1rem">{tags(project_tags)}</div></article>', unsafe_allow_html=True)


def education_section() -> None:
    page_heading("Academic journey", "Education that grounds", "my work.", "A computing-focused academic path that supports my interest in software development and technology.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    education = [
        ("MCA", "ABES Engineering College"),
        ("BCA", "University of Allahabad"),
        ("12th", "Air Force School Bamrauli"),
        ("10th", "Air Force School Bamrauli"),
    ]
    timeline = []
    for qualification, institution in education:
        timeline.append(
            f'<div class="timeline-item"><div class="timeline-degree">{qualification}</div>'
            f'<div class="timeline-place">{institution}</div></div>'
        )
    st.markdown(f'<div class="timeline">{"".join(timeline)}</div>', unsafe_allow_html=True)


def certifications_section() -> None:
    page_heading("Credentials", "Certifications and", "learning.", "Professional learning credentials across Python, data, SQL and cybersecurity.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    certifications = [
        ("fa-database", "SQL Basic", "HackerRank"),
        ("fa-shield-halved", "Introduction to Cybersecurity", "Cisco Networking Academy"),
        ("fa-python", "Python Essentials 1", "Cisco Networking Academy"),
        ("fa-python", "Python Essentials 2", "Cisco Networking Academy"),
        ("fa-chart-line", "Data Science with Python", "Simplilearn"),
        ("fa-server", "SQL Intermediate", "SoloLearn"),
    ]
    columns = st.columns(3, gap="medium")
    for index, (symbol, certification, organization) in enumerate(certifications):
        with columns[index % 3]:
            st.markdown(f'<article class="cert-card"><div class="card-icon">{icon(symbol)}</div><h2 class="card-title">{certification}</h2><p class="cert-org">{organization}</p></article>', unsafe_allow_html=True)


def innovation_section() -> None:
    """Highlight the practical, problem-solving approach behind the portfolio."""
    page_heading(
        "Innovation",
        "Turning learning into",
        "useful ideas.",
        "I explore technology by connecting Python, data, APIs and clear interfaces into practical software experiences.",
    )
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    ideas = [
        (
            "fa-cloud-sun",
            "Environmental insights",
            "IntelliAir Pro explores how weather and environmental information can be presented through an approachable interactive dashboard.",
        ),
        (
            "fa-code-branch",
            "Useful software",
            "I focus on applications that solve understandable problems through thoughtful Python development, data handling and integrations.",
        ),
        (
            "fa-lightbulb",
            "Continuous exploration",
            "Each project is an opportunity to strengthen fundamentals, test an idea and learn from building something real.",
        ),
    ]
    columns = st.columns(3, gap="medium")
    for column, (symbol, title, description) in zip(columns, ideas):
        with column:
            st.markdown(
                f'<article class="glass-card"><div class="card-icon">{icon(symbol)}</div>'
                f'<h2 class="card-title">{title}</h2><p class="card-text">{description}</p></article>',
                unsafe_allow_html=True,
            )


def resume_section() -> None:
    page_heading("Resume", "A closer look at", "my profile.", "Download my resume for an overview of education, technical skills, certifications and projects.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    st.markdown(f'<article class="resume-panel"><div class="card-icon">{icon("fa-file-arrow-down")}</div><h2 class="card-title">Avaneesh Singh — Resume</h2><p class="card-text">The document is available as a PDF download when assets/resume.pdf is present.</p></article>', unsafe_allow_html=True)
    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
    if read_binary(RESUME_PATH):
        resume_download("Download Resume", "resume_page_download")
    else:
        st.warning("Resume will be available soon. Add assets/resume.pdf to enable the download.")


def email_settings() -> tuple[str, str, str] | None:
    """Read Gmail settings from Streamlit secrets only, never source code."""
    try:
        sender = st.secrets["email"]["sender"]
        password = st.secrets["email"]["password"]
        receiver = st.secrets["email"]["receiver"]
    except (KeyError, FileNotFoundError, TypeError):
        sender = None
        password = None
        receiver = None

    if not sender or not password or not receiver:
        return None
    return (str(sender).strip(), str(password).strip(), str(receiver).strip())


def is_valid_email(address: str) -> bool:
    """Return whether an address has the basic structure required by the form."""
    return bool(EMAIL_PATTERN.fullmatch(address.strip()))


def send_contact_email(name: str, visitor_email: str, subject: str, message: str) -> None:
    """Send a contact-form message through a configured Gmail app password."""
    settings = email_settings()
    if not settings:
        raise RuntimeError("Email delivery is not configured yet. Please configure Streamlit secrets.")

    sender, password, receiver = settings
    email = EmailMessage()
    email["From"] = sender
    email["To"] = receiver
    email["Reply-To"] = visitor_email
    email["Subject"] = subject
    email.set_content(
        "Visitor Name: " + name + "\n"
        "Visitor Email: " + visitor_email + "\n"
        "Subject: " + subject + "\n\n"
        "Message:\n" + message
    )

    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        server.starttls()
        server.login(sender, password)
        server.send_message(email)
    finally:
        server.quit()


def contact_section() -> None:
    page_heading("Contact", "Let's start a", "conversation.", "I'm interested in software development, Python development and technology opportunities.")
    st.markdown('<div class="section-space"></div>', unsafe_allow_html=True)
    details_column, form_column = st.columns([.78, 1.22], gap="large")
    with details_column:
        st.markdown(
            f'<article class="glass-card"><div class="card-icon">{icon("fa-paper-plane")}</div><h2 class="card-title">Contact Information</h2><p class="card-text">The quickest way to connect is through LinkedIn.</p><a class="contact-item" href="{LINKEDIN_URL}" target="_blank" rel="noopener noreferrer">{icon("fa-linkedin-in")} LinkedIn</a></article>',
            unsafe_allow_html=True,
        )
    with form_column:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name", key="contact_name")
            visitor_email = st.text_input("Email", key="contact_email")
            subject = st.text_input("Subject", key="contact_subject")
            message = st.text_area("Message", height=155, key="contact_message")
            submitted = st.form_submit_button("Send Message", use_container_width=True, key="contact_send_message")

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            elif not visitor_email.strip():
                st.error("Please enter your email address.")
            elif not is_valid_email(visitor_email):
                st.error("Please enter a valid email address.")
            elif not message.strip():
                st.error("Please enter a message.")
            else:
                try:
                    send_contact_email(name.strip(), visitor_email.strip(), subject.strip(), message.strip())
                except RuntimeError as error:
                    st.error(str(error))
                except (OSError, ValueError, smtplib.SMTPException) as error:
                    detail = str(error).strip()
                    st.error(f"Message could not be sent: {detail}" if detail else "Message could not be sent right now. Please try again later.")
                else:
                    st.success("✅ Message sent successfully!")


def footer() -> None:
    st.markdown(
        """
        <div class="site-footer">
            <strong>Avaneesh Singh</strong><br>
            Python Developer | Software Developer<br>
            © 2026 Avaneesh Singh<br>
            Built with Python + Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page(page: str) -> None:
    """Render exactly one portfolio section for the active navigation page."""
    pages = {
        "Home": home_section,
        "About": about_section,
        "Skills": skills_section,
        "Projects": projects_section,
        "Education": education_section,
        "Certifications": certifications_section,
        "Resume": resume_section,
        "Contact": contact_section,
    }
    pages.get(page, home_section)()


def main() -> None:
    load_css()
    selected_page = render_navbar()
    render_page(selected_page)
    footer()


if __name__ == "__main__":
    main()
