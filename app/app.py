import re
import sys
import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analyzer import analyze_contract


st.set_page_config(
    page_title="AI Contract Risk Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #f4f7fb;
        --surface: #ffffff;
        --surface-2: #f8fbff;
        --surface-3: #eef7f8;
        --ink: #132238;
        --muted: #53657a;
        --line: #d8e1eb;
        --brand: #135d66;
        --brand-2: #0f3d56;
        --brand-soft: #e7f6f7;
        --accent: #b86a1f;
        --accent-soft: #fff2e2;
        --success: #116149;
        --success-soft: #e8f6ef;
        --warning: #8a5a00;
        --warning-soft: #fff4d9;
        --danger: #a12b2b;
        --danger-soft: #fdecec;
        --shadow: 0 20px 50px rgba(17, 37, 62, 0.08);
        --shadow-strong: 0 24px 60px rgba(12, 39, 60, 0.14);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(19, 93, 102, 0.08), transparent 22%),
            radial-gradient(circle at top right, rgba(184, 106, 31, 0.08), transparent 18%),
            linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        color: var(--ink);
    }

    h1, h2, h3 {
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        color: var(--ink);
        letter-spacing: -0.03em;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: #fbfdff;
        border-right: 1px solid var(--line);
    }

    .landing-shell {
        padding-top: 0.5rem;
    }

    .hero {
        background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%);
        border-radius: 30px;
        padding: 2.2rem;
        box-shadow: var(--shadow);
        color: #ffffff;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.12);
        animation: riseIn 0.85s cubic-bezier(.22,1,.36,1) both;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        right: -70px;
        top: -90px;
        background: radial-gradient(circle, rgba(255,255,255,0.17), transparent 65%);
    }

    .hero::before {
        content: "";
        position: absolute;
        inset: auto 0 -45% auto;
        width: 360px;
        height: 360px;
        background: radial-gradient(circle, rgba(255,255,255,0.16), transparent 62%);
        animation: pulseGlow 9s ease-in-out infinite;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.88fr);
        gap: 1.2rem;
        align-items: stretch;
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        display: inline-block;
        font-size: 0.8rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.82);
        margin-bottom: 0.8rem;
    }

    .hero-copy {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 3rem;
        line-height: 1.02;
        margin: 0 0 0.85rem 0;
        max-width: 700px;
    }

    .hero p {
        color: rgba(255,255,255,0.92);
        font-size: 1.04rem;
        line-height: 1.7;
        max-width: 720px;
        margin-bottom: 0;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        margin-top: 1.2rem;
    }

    .hero-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.65rem 0.92rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.14);
        color: rgba(255,255,255,0.95);
        font-size: 0.92rem;
    }

    .hero-preview {
        border-radius: 24px;
        padding: 1rem;
        background: linear-gradient(180deg, rgba(255,255,255,0.13), rgba(255,255,255,0.08));
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        animation: floatCard 8s ease-in-out infinite;
    }

    .preview-window {
        border-radius: 20px;
        padding: 1rem;
        background: rgba(8, 25, 41, 0.42);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .preview-dots {
        display: flex;
        gap: 0.45rem;
        margin-bottom: 0.9rem;
    }

    .preview-dots span {
        width: 0.65rem;
        height: 0.65rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.35);
    }

    .preview-dots span:nth-child(1) { background: #ffd166; }
    .preview-dots span:nth-child(2) { background: #7bd389; }
    .preview-dots span:nth-child(3) { background: #7ec8ff; }

    .preview-score {
        display: flex;
        align-items: end;
        gap: 0.65rem;
        margin-bottom: 0.95rem;
    }

    .preview-score strong {
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        font-size: 2.8rem;
        line-height: 1;
    }

    .preview-score span {
        color: rgba(255,255,255,0.78);
        font-size: 0.92rem;
        padding-bottom: 0.28rem;
    }

    .scan-line {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        padding: 0.72rem 0.9rem;
        border-radius: 16px;
        margin-bottom: 0.65rem;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .scan-line:last-child {
        margin-bottom: 0;
    }

    .scan-line label {
        display: block;
        color: rgba(255,255,255,0.88);
        font-size: 0.92rem;
        font-weight: 700;
    }

    .scan-track {
        width: 42%;
        min-width: 110px;
        height: 0.5rem;
        border-radius: 999px;
        overflow: hidden;
        background: rgba(255,255,255,0.12);
    }

    .scan-track span {
        display: block;
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, #f5d76e, #ffffff);
        animation: loadingBar 3.6s ease-in-out infinite;
        transform-origin: left center;
    }

    .surface-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.25rem;
        box-shadow: var(--shadow);
        animation: riseIn 0.9s cubic-bezier(.22,1,.36,1) both;
    }

    .surface-card:hover,
    .stat-card:hover,
    .soft-card:hover,
    .timeline-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-strong);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .soft-card {
        background: linear-gradient(180deg, #fcfdff 0%, var(--surface-2) 100%);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 1rem;
        position: relative;
        overflow: hidden;
    }

    .soft-card::after {
        content: "";
        position: absolute;
        inset: auto -10% -70% auto;
        width: 180px;
        height: 180px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(19, 93, 102, 0.08), transparent 62%);
    }

    .feature-title {
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.25rem;
    }

    .feature-copy {
        color: var(--muted);
        line-height: 1.55;
        font-size: 0.95rem;
    }

    .stat-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: var(--shadow);
        min-height: 138px;
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .stat-label {
        color: var(--muted);
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .stat-value {
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        font-size: 2rem;
        line-height: 1;
        color: var(--ink);
        margin-bottom: 0.45rem;
    }

    .stat-copy {
        color: var(--muted);
        line-height: 1.45;
        font-size: 0.94rem;
    }

    .pill {
        display: inline-block;
        margin: 0.22rem 0.35rem 0 0;
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        border: 1px solid var(--line);
        background: var(--surface-2);
        color: #23445a;
        font-size: 0.9rem;
    }

    .trust-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 1rem;
    }

    .timeline-card {
        background: linear-gradient(180deg, #fcfefe 0%, var(--surface-3) 100%);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: var(--shadow);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .timeline-step {
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-family: "Trebuchet MS", "Segoe UI", sans-serif;
        font-size: 0.95rem;
        background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%);
        color: #fff;
        box-shadow: 0 10px 24px rgba(19, 93, 102, 0.24);
        margin-bottom: 0.8rem;
    }

    .timeline-title {
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.28rem;
    }

    .timeline-copy {
        color: var(--muted);
        line-height: 1.55;
        font-size: 0.95rem;
    }

    .risk-badge {
        display: inline-block;
        border-radius: 999px;
        padding: 0.35rem 0.72rem;
        font-size: 0.78rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.45rem;
    }

    .risk-low {
        background: var(--success-soft);
        color: var(--success);
    }

    .risk-medium {
        background: var(--warning-soft);
        color: var(--warning);
    }

    .risk-high {
        background: var(--danger-soft);
        color: var(--danger);
    }

    .info-card {
        background: var(--surface-2);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.8rem;
    }

    .info-title {
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.28rem;
    }

    .info-copy {
        color: var(--muted);
        line-height: 1.55;
        font-size: 0.95rem;
    }

    .section-heading {
        color: #0f2f4a !important;
    }

    .section-body {
        color: #21384f !important;
    }

    .section-label {
        color: #12324d !important;
        font-weight: 800;
    }

    .table-heading {
        color: #0f2f4a !important;
        margin-bottom: 0.35rem;
    }

    .auth-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 26px;
        padding: 1.3rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        animation: riseIn 1s cubic-bezier(.22,1,.36,1) both;
    }

    .auth-card::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -90px;
        bottom: -90px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(19, 93, 102, 0.08), transparent 68%);
    }

    .auth-lead {
        color: var(--muted);
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .auth-note {
        background: var(--brand-soft);
        border: 1px solid #c8e6e7;
        color: #1d5560;
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 1rem;
    }

    div[data-testid="stFileUploader"] {
        background: #fbfdff;
        border: 1px dashed #abc4d4;
        border-radius: 18px;
        padding: 0.85rem;
        transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: var(--brand);
        box-shadow: 0 12px 28px rgba(19, 93, 102, 0.08);
        transform: translateY(-2px);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.35rem;
        background: #edf4f7;
        padding: 0.3rem;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: var(--ink);
        font-weight: 700;
        padding-left: 1rem;
        padding-right: 1rem;
        transition: background 160ms ease, color 160ms ease, transform 160ms ease;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        box-shadow: 0 8px 18px rgba(17, 37, 62, 0.08);
    }

    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-1px);
    }

    .stTextInput label, .stSelectbox label {
        color: var(--ink);
        font-weight: 700;
    }

    .stTextInput input {
        color: var(--ink) !important;
        background: #ffffff !important;
        border-radius: 12px !important;
    }

    .stTextInput input:focus {
        border-color: var(--brand) !important;
        box-shadow: 0 0 0 0.18rem rgba(19, 93, 102, 0.16) !important;
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 14px !important;
        border: 0 !important;
        min-height: 2.9rem;
        font-weight: 800 !important;
        background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 14px 30px rgba(19, 93, 102, 0.24);
        transition: transform 180ms ease, box-shadow 180ms ease, filter 180ms ease;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        filter: saturate(1.08);
        box-shadow: 0 18px 38px rgba(19, 93, 102, 0.28);
    }

    .stDataFrame, div[data-testid="stExpander"] {
        background: var(--surface);
        border-radius: 18px;
    }

    @keyframes riseIn {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); opacity: 0.75; }
        50% { transform: scale(1.08); opacity: 1; }
    }

    @keyframes loadingBar {
        0% { width: 30%; opacity: 0.7; }
        50% { width: 82%; opacity: 1; }
        100% { width: 48%; opacity: 0.82; }
    }

    @media (max-width: 980px) {
        .hero-grid,
        .trust-row {
            grid-template-columns: 1fr;
        }

        .hero h1 {
            font-size: 2.4rem;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation: none !important;
            transition: none !important;
            scroll-behavior: auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_session() -> None:
    defaults = {
        "page": "landing",
        "current_section": "Upload",
        "analysis_result": None,
        "uploaded_file_key": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def valid_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value.strip()))


def valid_phone(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    return 10 <= len(digits) <= 15


def valid_password(value: str) -> bool:
    return len(value.strip()) >= 6


def risk_badge(severity: str) -> str:
    icons = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴",
    }
    level = severity.lower()
    icon = icons.get(level, "⚪")
    return f'<span class="risk-badge risk-{level}">{icon} {level.upper()} Risk</span>'


def clause_expander_label(clause: dict) -> str:
    severity = clause["severity"].lower()
    icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(severity, "⚪")
    return f'{icon} Clause {clause["clause_number"]} | {severity.upper()} | Score {clause["score"]}'


def navigate(page: str, section: str | None = None) -> None:
    st.session_state.page = page
    if section is not None:
        st.session_state.current_section = section
    st.rerun()


def file_key(uploaded_file) -> str:
    content = uploaded_file.getvalue()
    digest = hashlib.md5(content).hexdigest()
    return f"{uploaded_file.name}:{digest}"


def show_landing_page() -> None:
    st.markdown('<div class="landing-shell">', unsafe_allow_html=True)

    top_left, top_right = st.columns([1.25, 0.95], gap="large")

    with top_left:
        st.markdown(
            """
            <div class="hero">
                <div class="hero-grid">
                    <div class="hero-copy">
                        <div class="eyebrow">Contract Intelligence Platform</div>
                        <h1>AI-powered contract risk analysis for startups, freelancers, and fast-moving teams.</h1>
                        <p>
                            Contracts hide renewal traps, vague obligations, payment exposure, and one-sided terms.
                            This app gives teams a fast first-pass review so they can spot risk earlier, understand
                            what the AI found, and walk into legal review with better context.
                        </p>
                        <div class="hero-actions">
                            <span class="hero-chip">Clause risk detection</span>
                            <span class="hero-chip">AI clause summaries</span>
                            <span class="hero-chip">Pitch-ready workflow</span>
                        </div>
                    </div>
                    <div class="hero-preview">
                        <div class="preview-window">
                            <div class="preview-dots"><span></span><span></span><span></span></div>
                            <div class="preview-score">
                                <strong>72</strong>
                                <span>overall risk score detected</span>
                            </div>
                            <div class="scan-line">
                                <label>Termination clause</label>
                                <div class="scan-track"><span></span></div>
                            </div>
                            <div class="scan-line">
                                <label>Payment obligations</label>
                                <div class="scan-track"><span style="animation-delay:-1.1s;"></span></div>
                            </div>
                            <div class="scan-line">
                                <label>Auto-renewal language</label>
                                <div class="scan-track"><span style="animation-delay:-2.1s;"></span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="surface-card" style="margin-top:1rem;">
                <h3 style="margin-top:0;">Why this matters</h3>
                <div class="soft-card" style="margin-bottom:0.8rem;">
                    <div class="feature-title">What problem are we solving?</div>
                    <div class="feature-copy">Manual contract review is slow, inconsistent, and easy to miss under time pressure, especially for founders, freelancers, and small teams.</div>
                </div>
                <div class="soft-card" style="margin-bottom:0.8rem;">
                    <div class="feature-title">How does AI help?</div>
                    <div class="feature-copy">The analyzer extracts clauses, scores risk, flags suspicious language, and summarizes obligations so users can review smarter instead of reading everything from scratch.</div>
                </div>
                <div class="soft-card">
                    <div class="feature-title">Why should users trust it?</div>
                    <div class="feature-copy">The product shows the exact clauses behind each flag, keeps extracted entities visible, and presents AI output as a transparent first-pass assistant rather than a black-box legal replacement.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="trust-row">
                <div class="timeline-card">
                    <div class="timeline-step">1</div>
                    <div class="timeline-title">Landing page</div>
                    <div class="timeline-copy">Users learn what the product does, why AI is useful here, and why the workflow is trustworthy.</div>
                </div>
                <div class="timeline-card">
                    <div class="timeline-step">2</div>
                    <div class="timeline-title">Try now</div>
                    <div class="timeline-copy">A clear call-to-action moves them straight into the analyzer without unnecessary signup friction.</div>
                </div>
                <div class="timeline-card">
                    <div class="timeline-step">3</div>
                    <div class="timeline-title">Results and report</div>
                    <div class="timeline-copy">They upload a contract, review flagged clauses, and leave with a report that feels like a real product journey.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_right:
        st.markdown(
            """
            <div class="auth-card">
                <h2 style="margin-top:0;">Analyze Your Contract Now</h2>
                <div class="auth-lead">
                    Upload a PDF, let the AI identify risky clauses and obligations, then review a clean summary and clause-by-clause report.
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="info-card">
                <div class="info-title">What you get</div>
                <div class="info-copy">Risk score, clause analysis, obligation highlights, entity extraction, and a report-style review screen.</div>
            </div>
            <div class="info-card">
                <div class="info-title">Best for</div>
                <div class="info-copy">Hackathon demos, internship projects, startup validation, and internal contract triage workflows.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Analyze Your Contract Now", use_container_width=True):
            navigate("analyzer", "Upload")
        if st.button("See Results Flow", use_container_width=True):
            section = "Report" if st.session_state.analysis_result else "Upload"
            navigate("analyzer", section)

        st.markdown(
            """
            <div class="auth-note">
                Trust note: the AI acts as a first-pass reviewer. It explains flagged clauses and helps prioritize legal attention, but it does not replace legal counsel.
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    stats = st.columns(3)
    items = [
        ("Problem solved", "Faster review", "Teams can move from long PDFs to the clauses that matter without reading line by line first."),
        ("AI advantage", "Clearer analysis", "Clause scoring, extraction, and summaries reduce guesswork and create a more guided review flow."),
        ("Pitch value", "More credible", "A landing page plus analyzer journey makes the project feel closer to a startup product than a raw demo."),
    ]

    for col, (label, value, copy) in zip(stats, items):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def show_main_app() -> None:
    with st.sidebar:
        st.subheader("Workspace")
        st.caption("Upload a contract and move through analysis to report.")
        st.divider()
        if st.button("Back to Landing Page", use_container_width=True):
            navigate("landing")
        if st.button("Go to Upload", use_container_width=True):
            navigate("analyzer", "Upload")
        st.divider()
        current_section = st.radio(
            "Go to",
            ["Upload", "Analysis", "Report"],
            index=["Upload", "Analysis", "Report"].index(st.session_state.current_section),
            label_visibility="collapsed",
            key="current_section",
        )
        st.divider()
        st.subheader("Product Flow")
        st.write("1. Landing page explains value.")
        st.write("2. Try Now opens the analyzer.")
        st.write("3. Upload starts AI analysis.")
        st.write("4. Results become a shareable report view.")

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Upload and Analysis Page</div>
            <h1>AI Contract Risk Analyzer</h1>
            <p>
                Upload a contract PDF to detect obligations, analyze clauses, and generate a results workflow that feels ready for demos, pitches, and product reviews.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader("Upload contract PDF", type=["pdf"])

    if uploaded_file is None:
        if current_section == "Upload":
            left, right = st.columns([1.25, 1], gap="large")
            with left:
                st.markdown(
                    """
                    <div class="surface-card">
                        <h3 style="margin-top:0;">What the model will prepare</h3>
                        <span class="pill">Clause-level scoring</span>
                        <span class="pill">Entity extraction</span>
                        <span class="pill">Obligation review</span>
                        <span class="pill">High-risk clause list</span>
                        <span class="pill">Readable summary</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with right:
                st.markdown(
                    """
                    <div class="surface-card">
                        <h3 style="margin-top:0;">Suggested use</h3>
                        <div class="info-card">
                            <div class="info-title">First-pass triage</div>
                            <div class="info-copy">Use the analyzer to narrow attention before a deeper legal review.</div>
                        </div>
                        <div class="info-card" style="margin-bottom:0;">
                            <div class="info-title">Business alignment</div>
                            <div class="info-copy">Validate renewal, termination, confidentiality, and payment terms quickly.</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        elif current_section == "Analysis":
            st.info("Upload a contract first to unlock the Analysis view.")
        else:
            st.info("Upload a contract first to generate the Report view.")
        return

    current_file_key = file_key(uploaded_file)
    if st.session_state.uploaded_file_key != current_file_key or st.session_state.analysis_result is None:
        progress_text = st.empty()
        progress_bar = st.progress(0)
        progress_steps = [
            (10, "Uploading contract..."),
            (28, "Extracting text and clauses..."),
            (52, "Scoring clause risk..."),
            (76, "Detecting entities and obligations..."),
            (92, "Preparing analysis report..."),
        ]
        for value, message in progress_steps:
            progress_text.caption(message)
            progress_bar.progress(value)

        with st.spinner("Analyzing contract..."):
            st.session_state.analysis_result = analyze_contract(uploaded_file)

        st.session_state.uploaded_file_key = current_file_key
        progress_text.caption("Analysis complete.")
        progress_bar.progress(100)

    result = st.session_state.analysis_result

    risk_report = result["risk_report"]
    high_count = len(result["high_risk_clauses"])
    medium_count = sum(1 for clause in risk_report["clauses"] if clause["severity"] == "medium")
    low_count = sum(1 for clause in risk_report["clauses"] if clause["severity"] == "low")
    entities = result["entities"]

    stat_cols = st.columns(3)
    stat_payload = [
        ("Overall Risk Score", str(risk_report["overall_score"]), "Average risk intensity across extracted clauses."),
        ("Immediate Review", str(high_count), "High-risk clauses that should be checked first."),
        ("Clause Coverage", str(result["clause_count"]), f"{medium_count} medium-risk clauses also need review."),
    ]

    for col, (label, value, copy) in zip(stat_cols, stat_payload):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-copy">{copy}</div>
                    {" " if label != "Immediate Review" else risk_badge(risk_report["overall_severity"])}
                </div>
                """,
                unsafe_allow_html=True,
            )

    if current_section == "Upload":
        st.success("Contract uploaded successfully. Switch to Analysis or Report in the sidebar when you’re ready.")
        return

    if current_section == "Analysis":
        summary_col, checklist_col = st.columns([1.55, 1], gap="large")

        with summary_col:
            st.markdown('<div class="surface-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-heading">Executive Summary</h3>', unsafe_allow_html=True)
            st.markdown(f'<div class="section-body">{result["summary"]}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with checklist_col:
            st.markdown(
                f"""
                <div class="surface-card">
                    <h3 style="margin-top:0;">Review Checklist</h3>
                    <div class="info-card">
                        <div class="info-title">🔴 Check high-risk clauses first</div>
                        <div class="info-copy">{high_count} clauses are currently flagged at high severity.</div>
                    </div>
                    <div class="info-card">
                        <div class="info-title">🟡 Confirm commercial exposure</div>
                        <div class="info-copy">Review payment language, automatic renewal, termination rights, and confidentiality duties.</div>
                    </div>
                    <div class="info-card" style="margin-bottom:0;">
                        <div class="info-title">🟢 Validate obligations</div>
                        <div class="info-copy">Look for mandatory terms created by shall, must, and similar language.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        legend_cols = st.columns(3)
        legend_items = [
            ("🟢 Low Risk", str(low_count), "Routine clauses with limited immediate concern."),
            ("🟡 Medium Risk", str(medium_count), "Clauses that deserve business or legal review."),
            ("🔴 High Risk", str(high_count), "Clauses that should be prioritized first."),
        ]
        for col, (label, value, copy) in zip(legend_cols, legend_items):
            with col:
                st.markdown(
                    f"""
                    <div class="stat-card">
                        <div class="stat-label">{label}</div>
                        <div class="stat-value">{value}</div>
                        <div class="stat-copy">{copy}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        entity_col, obligation_col = st.columns(2, gap="large")

        with entity_col:
            st.markdown('<div class="surface-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-heading">Detected Entities</h3>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Parties</div>', unsafe_allow_html=True)
            if entities["parties"]:
                st.markdown("".join(f'<span class="pill">{party}</span>' for party in entities["parties"]), unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-body">None detected</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:0.8rem;">Dates</div>', unsafe_allow_html=True)
            if entities["dates"]:
                st.markdown("".join(f'<span class="pill">{date}</span>' for date in entities["dates"][:10]), unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-body">None detected</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label" style="margin-top:0.8rem;">Amounts</div>', unsafe_allow_html=True)
            if entities["amounts"]:
                st.markdown("".join(f'<span class="pill">{amount}</span>' for amount in entities["amounts"][:10]), unsafe_allow_html=True)
            else:
                st.markdown('<div class="section-body">None detected</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with obligation_col:
            st.markdown('<div class="surface-card">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-heading">Key Obligations</h3>', unsafe_allow_html=True)
            obligations = entities["obligations"][:8]
            if obligations:
                for obligation in obligations:
                    st.markdown(
                        f"""
                        <div class="info-card">
                            <div class="info-title">Obligation detected</div>
                            <div class="info-copy">{obligation}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div class="section-body">No strong obligation statements were detected.</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Expandable Clause Review")
        for clause in risk_report["clauses"]:
            with st.expander(clause_expander_label(clause), expanded=clause["severity"] == "high"):
                st.markdown(risk_badge(clause["severity"]), unsafe_allow_html=True)
                st.write(clause["text"])
                if clause["flags"]:
                    for flag in clause["flags"]:
                        st.markdown(
                            f"""
                            <div class="info-card">
                                <div class="info-title">{flag['label']}</div>
                                <div class="info-copy">{flag['reason']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.caption("No specific risk flags were attached to this clause.")
        return

    st.markdown('<h3 class="table-heading">Clause Risk Table</h3>', unsafe_allow_html=True)
    clause_rows = [
        {
            "Clause #": clause["clause_number"],
            "Severity": f'{"🟢" if clause["severity"] == "low" else "🟡" if clause["severity"] == "medium" else "🔴"} {clause["severity"].upper()}',
            "Score": clause["score"],
            "Flags": ", ".join(flag["label"] for flag in clause["flags"]) or "None",
            "Preview": clause["text"][:140] + ("..." if len(clause["text"]) > 140 else ""),
        }
        for clause in risk_report["clauses"]
    ]
    table_df = pd.DataFrame(clause_rows).sort_values(by=["Score", "Clause #"], ascending=[False, True])
    st.dataframe(table_df, use_container_width=True, hide_index=True)

    st.subheader("Risk Summary Report")
    report_left, report_right = st.columns([1.2, 1], gap="large")

    with report_left:
        st.markdown('<div class="surface-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-heading">Executive Summary</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-body">{result["summary"]}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with report_right:
        st.markdown(
            f"""
            <div class="surface-card">
                <h3 style="margin-top:0;">Risk Breakdown</h3>
                <div class="info-card">
                    <div class="info-title">🔴 High Risk</div>
                    <div class="info-copy">{high_count} clauses need immediate attention.</div>
                </div>
                <div class="info-card">
                    <div class="info-title">🟡 Medium Risk</div>
                    <div class="info-copy">{medium_count} clauses may affect commercial terms.</div>
                </div>
                <div class="info-card" style="margin-bottom:0;">
                    <div class="info-title">🟢 Low Risk</div>
                    <div class="info-copy">{low_count} clauses appear routine under current rules.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Expandable Clause Report")
    for clause in risk_report["clauses"]:
        with st.expander(clause_expander_label(clause), expanded=clause["severity"] == "high"):
            st.markdown(risk_badge(clause["severity"]), unsafe_allow_html=True)
            st.write(clause["text"])
            if clause["flags"]:
                for flag in clause["flags"]:
                    st.markdown(
                        f"""
                        <div class="info-card">
                            <div class="info-title">{flag['label']}</div>
                            <div class="info-copy">{flag['reason']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No specific risk flags were attached to this clause.")

    with st.expander("Extracted Contract Text"):
        st.text(result["text"][:10000] or "No text extracted from the PDF.")


init_session()

try:
    if st.session_state.page == "analyzer":
        show_main_app()
    else:
        show_landing_page()
except Exception as exc:
    st.error("The app hit a rendering error. A safer fallback view is shown below.")
    st.exception(exc)
    st.markdown("## AI Contract Risk Analyzer")
    st.write("Please refresh the page after this fix. If the issue returns, the error details above will stay visible instead of a blank page.")
