import streamlit as st
import streamlit.components.v1 as components
import tempfile

from visualization.dashboard_charts import (
    show_benchmark_metrics,
    show_runtime_chart,
    show_csv_download
)

st.set_page_config(
    page_title="AlgoBench | Performance Lab",
    page_icon="💫",
    layout="wide",
    initial_sidebar_state="expanded"
)


import base64
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
LOGO_PATH = PROJECT_DIR / "Logo_Final.svg"
FONT_PATH = PROJECT_DIR / "assets" / "NetflixSans-Regular.ttf"

# Encode the existing SVG so the browser can display it without a separate URL.
LOGO_DATA_URI = (
    "data:image/svg+xml;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    if LOGO_PATH.is_file() else None
)

if not FONT_PATH.exists():
    st.error("Netflix Sans font file not found in assets/NetflixSans-Regular.ttf")
    st.stop()

FONT_BASE64 = base64.b64encode(
    FONT_PATH.read_bytes()
).decode("utf-8")


# Intro animation component. The HTML file is generated locally from this app.py,
# so no extra frontend build step is needed.
LANDING_COMPONENT_DIR = Path(tempfile.gettempdir()) / "algobench_landing_component"
LANDING_COMPONENT_DIR.mkdir(exist_ok=True)
LANDING_COMPONENT_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@font-face {
    font-family: "Netflix Sans";
    src: url(data:font/ttf;base64,LANDING_FONT_DATA) format("truetype");
    font-style: normal;
    font-weight: 100 900;
    font-display: swap;
}
:root {
    --intro-bg: #111315;
    --intro-panel: #1C1F22;
    --intro-text: #F0F1F2;
    --intro-muted: #A8AFB3;
    --intro-accent: #B7BEC2;
    --intro-glow: rgba(174,183,188,.15);
}
* { box-sizing: border-box; }
html, body {
    margin: 0;
    width: 100%;
    min-height: 100%;
    background: var(--intro-bg);
    color: var(--intro-text);
    font-family: "Netflix Sans", Arial, sans-serif;
    overflow: hidden;
}
.landing {
    width: 100%;
    min-height: 790px;
    height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    isolation: isolate;
    background:
        radial-gradient(ellipse at 50% 42%, var(--intro-glow) 0%, transparent 42%),
        linear-gradient(145deg, var(--intro-bg), var(--intro-bg));
}
.ambient {
    position: absolute;
    width: min(900px, 95vw);
    height: min(900px, 95vw);
    border-radius: 50%;
    background: radial-gradient(circle, var(--intro-glow), transparent 67%);
    filter: blur(24px);
    opacity: .8;
    pointer-events: none;
}
.landing-content {
    width: 100%;
    max-width: 1100px;
    min-height: 790px;
    height: 100%;
    padding: 0 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 2;
    text-align: center;
}
.topline {
    position: absolute;
    top: 34px;
    left: 28px;
    right: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--intro-muted);
    font-size: 10px;
    letter-spacing: 2.3px;
    text-transform: uppercase;
}
.topline .status { display: flex; align-items: center; gap: 8px; }
.status-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--intro-accent);
    box-shadow: 0 0 12px var(--intro-accent);
}
.brand-kicker {
    font-size: 11px;
    color: var(--intro-muted);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 18px;
    opacity: .95;
}
.mark-stage {
    width: min(470px, 74vw);
    height: min(470px, 74vw);
    min-width: 280px;
    min-height: 280px;
    position: relative;
    display: grid;
    place-items: center;
    margin: 0 0 14px;
}
.ring {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    transform-origin: center;
}
.ring-primary {
    inset: 3%;
    border: 1px solid color-mix(in srgb, var(--intro-accent) 74%, transparent);
    box-shadow: 0 0 34px var(--intro-glow), inset 0 0 28px var(--intro-glow);
    animation: idle-clockwise 32s linear infinite;
}
.ring-primary::before {
    content: "";
    position: absolute;
    inset: -12px;
    border-radius: 50%;
    border: 1px dashed color-mix(in srgb, var(--intro-accent) 55%, transparent);
}
.ring-primary::after {
    content: "";
    position: absolute;
    left: 50%; top: -5px;
    width: 9px; height: 9px;
    transform: translateX(-50%);
    border-radius: 50%;
    background: var(--intro-accent);
    box-shadow: 0 0 20px var(--intro-accent);
}
.ring-secondary {
    inset: 13%;
    border: 1px solid color-mix(in srgb, var(--intro-accent) 40%, transparent);
    animation: idle-counter 42s linear infinite;
}
.ring-secondary::before, .ring-secondary::after {
    content: "";
    position: absolute;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--intro-accent);
    opacity: .8;
}
.ring-secondary::before { left: 13%; top: 20%; }
.ring-secondary::after { right: 10%; bottom: 19%; }
.ring-tertiary {
    inset: 23%;
    border: 1px solid color-mix(in srgb, var(--intro-accent) 24%, transparent);
}
.mark-button {
    position: relative;
    z-index: 3;
    border: 0;
    padding: 0;
    width: 76%;
    height: 76%;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: transparent;
    cursor: pointer;
    outline: none;
    -webkit-tap-highlight-color: transparent;
}
.mark-button:focus-visible {
    outline: 1px solid var(--intro-accent);
    outline-offset: 12px;
}
.mark-button img {
    display: block;
    width: 100%;
    max-width: 370px;
    max-height: 370px;
    object-fit: contain;
    position: relative;
    left: clamp(18px, 2.5vw, 42px);
    filter: drop-shadow(0 12px 28px var(--intro-glow));
    transition: transform .35s ease, filter .35s ease;
}
.mark-button:hover img {
    /* Keep the logo anchored; hover only changes its shadow. */
    filter: drop-shadow(0 14px 34px var(--intro-glow));
}
.fallback-mark {
    color: var(--intro-text);
    font-size: clamp(120px, 20vw, 190px);
    line-height: 1;
    font-weight: 700;
    letter-spacing: -12px;
}
.wordmark {
    color: var(--intro-text);
    font-size: clamp(26px, 4vw, 38px);
    font-weight: 650;
    letter-spacing: -.8px;
    margin-top: 4px;
}
.wordmark span { color: var(--intro-accent); }
.tagline {
    margin-top: 9px;
    color: var(--intro-muted);
    font-size: 10px;
    letter-spacing: 3.2px;
    text-transform: uppercase;
}
.enter-hint {
    margin-top: 34px;
    display: flex;
    align-items: center;
    gap: 11px;
    color: var(--intro-muted);
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    transition: opacity .25s ease, transform .25s ease;
}
.enter-hint .line {
    width: 36px; height: 1px; background: var(--intro-accent); opacity: .7;
}
.bottomline {
    position: absolute;
    bottom: 29px;
    color: var(--intro-muted);
    font-size: 9px;
    letter-spacing: 2px;
    opacity: .72;
    text-transform: uppercase;
}
@keyframes idle-clockwise { to { transform: rotate(360deg); } }
@keyframes idle-counter { to { transform: rotate(-360deg); } }
@keyframes reverse-primary {
    0% { transform: rotate(0deg) scale(1); opacity: 1; }
    68% { transform: rotate(-510deg) scale(.86); opacity: .58; }
    100% { transform: rotate(-760deg) scale(.38); opacity: 0; }
}
@keyframes reverse-secondary {
    0% { transform: rotate(0deg) scale(1); opacity: .8; }
    100% { transform: rotate(620deg) scale(.55); opacity: 0; }
}
@keyframes ring-disappear {
    to { opacity: 0; transform: scale(.72); }
}
@keyframes mark-launch {
    0% { opacity: 1; transform: translate3d(0,0,0) scale(1); }
    24% { opacity: 1; transform: translate3d(0,-12px,0) scale(1.04); }
    100% { opacity: 0; transform: translate3d(0,-115vh,0) scale(.58); }
}
@keyframes text-dissolve {
    to { opacity: 0; transform: translateY(12px); }
}
.landing.launching .ring-primary { animation: reverse-primary 1.12s cubic-bezier(.65,0,.35,1) forwards; }
.landing.launching .ring-secondary { animation: reverse-secondary .92s ease-in forwards; }
.landing.launching .ring-tertiary { animation: ring-disappear .62s ease-in forwards; }
.landing.launching .mark-button { animation: mark-launch .76s cubic-bezier(.7,0,.84,.22) 1.15s forwards; }
.landing.launching .brand-kicker,
.landing.launching .wordmark,
.landing.launching .tagline,
.landing.launching .enter-hint,
.landing.launching .topline,
.landing.launching .bottomline { animation: text-dissolve .38s ease forwards; }
.landing.launching .brand-kicker { animation-delay: .08s; }
.landing.launching .enter-hint { animation-delay: .12s; }
@media (max-width: 650px) {
    .landing, .landing-content { min-height: 690px; }
    .mark-stage { width: 86vw; height: 86vw; }
    .mark-button { width: 78%; height: 78%; }
    .mark-button img {
        max-width: 300px;
        max-height: 300px;
        left: 16px;
    }
    .mark-button:hover img {
        /* No translation or scaling on hover on small screens either. */
        filter: drop-shadow(0 14px 34px var(--intro-glow));
    }
    .bottomline { bottom: 18px; font-size: 8px; }
}
@media (prefers-reduced-motion: reduce) {
    .ring-primary, .ring-secondary { animation: none; }
    .mark-button, .ring { transition: none; }
}
</style>
</head>
<body>
<main class="landing" id="landing">
    <div class="ambient"></div>
    <div class="landing-content">
        <div class="mark-stage">
            <div class="ring ring-primary"></div>
            <div class="ring ring-secondary"></div>
            <div class="ring ring-tertiary"></div>
            <button class="mark-button" id="launch" aria-label="Enter AlgoBench">
                <img id="logo" alt="AlgoBench A logo" style="display:none">
                <span class="fallback-mark" id="fallback">A</span>
            </button>
        </div>
        <div class="wordmark">Algo<span>Bench</span></div>
        <div class="tagline">Algorithm Benchmarking &amp; Profiling Suite</div>
        <div class="enter-hint"><span class="line"></span>Click the mark to enter<span class="line"></span></div>
        <div class="bottomline">Measure accurately · Understand deeply · Optimize intelligently</div>
    </div>
</main>
<script>
(function () {
    let hasStarted = false;
    let args = {};

    function applyArgs(nextArgs) {
        args = nextArgs || {};
        const root = document.documentElement;
        root.style.setProperty('--intro-bg', args.bg || '#111315');
        root.style.setProperty('--intro-panel', args.panel || '#1C1F22');
        root.style.setProperty('--intro-text', args.text || '#F0F1F2');
        root.style.setProperty('--intro-muted', args.muted || '#A8AFB3');
        root.style.setProperty('--intro-accent', args.accent || '#B7BEC2');
        root.style.setProperty('--intro-glow', args.glow || 'rgba(174,183,188,.15)');
        if (args.font) {
            const fontStyle = document.createElement('style');
            fontStyle.textContent = '@font-face{font-family:"Netflix Sans";src:url(data:font/ttf;base64,' + args.font + ') format("truetype");font-display:swap;}';
            document.head.appendChild(fontStyle);
        }
        const logo = document.getElementById('logo');
        const fallback = document.getElementById('fallback');
        if (args.logo) {
            logo.src = args.logo;
            logo.style.display = 'block';
            fallback.style.display = 'none';
        }
        sendHeight();
    }

    function sendHeight() {
        window.parent.postMessage({isStreamlitMessage:true, type:'streamlit:setFrameHeight', height:790}, '*');
    }

    function completeIntro() {
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setComponentValue',
            value: true,
            dataType: 'json'
        }, '*');
    }

    document.getElementById('launch').addEventListener('click', function () {
        if (hasStarted) return;
        hasStarted = true;
        document.getElementById('landing').classList.add('launching');
        this.disabled = true;
        window.setTimeout(completeIntro, 1950);
    });

    window.addEventListener('message', function (event) {
        if (event.data && event.data.type === 'streamlit:render') {
            applyArgs(event.data.args || {});
        }
    });

    window.parent.postMessage({
        isStreamlitMessage: true,
        type: 'streamlit:componentReady',
        apiVersion: 1
    }, '*');
    sendHeight();
})();
</script>
</body>
</html>
"""
LANDING_COMPONENT_HTML = LANDING_COMPONENT_HTML.replace("LANDING_FONT_DATA", FONT_BASE64)
(LANDING_COMPONENT_DIR / "index.html").write_text(LANDING_COMPONENT_HTML, encoding="utf-8")
landing_component = components.declare_component(
    "algobench_intro_screen",
    path=str(LANDING_COMPONENT_DIR)
)


# Compact animated brand component used in the dashboard sidebar.
SIDEBAR_BRAND_DIR = Path(tempfile.gettempdir()) / "algobench_sidebar_brand"
SIDEBAR_BRAND_DIR.mkdir(exist_ok=True)
SIDEBAR_BRAND_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: transparent;
}
.brand-wrap {
    width: 88px;
    height: 88px;
    display: grid;
    place-items: center;
    overflow: visible;
}
.brand-trigger {
    position: relative;
    width: 84px;
    height: 84px;
    padding: 0;
    margin: 0;
    border: 0;
    border-radius: 50%;
    background: transparent;
    display: grid;
    place-items: center;
    cursor: pointer;
    outline: none;
    -webkit-tap-highlight-color: transparent;
}
.brand-trigger:focus-visible {
    outline: 1px solid var(--brand-accent);
    outline-offset: 2px;
}
.brand-ring, .brand-orbit {
    position: absolute;
    inset: 5px;
    border: 1px solid var(--brand-ring);
    border-radius: 50%;
    pointer-events: none;
}
.brand-ring-inner {
    position: absolute;
    inset: 13px;
    border: 1px solid var(--brand-ring-inner);
    border-radius: 50%;
}
.brand-orbit {
    inset: 0;
    border: 1px dashed var(--brand-ring-dashed);
    animation: brand-orbit 9s linear infinite;
}
.brand-orbit::before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 6px;
    height: 6px;
    transform: translate(-50%, -1px);
    border-radius: 50%;
    background: var(--brand-accent);
    box-shadow: 0 0 9px var(--brand-glow);
}
.brand-logo {
    position: relative;
    z-index: 2;
    display: block;
    width: 61px;
    height: 61px;
    object-fit: contain;
    transform: translateY(0);
    filter: var(--brand-logo-filter) drop-shadow(0 2px 5px var(--brand-glow));
    transition: filter .22s ease;
    pointer-events: none;
}
.brand-trigger:hover .brand-logo {
    filter: var(--brand-logo-filter) drop-shadow(0 3px 9px var(--brand-glow));
}
.brand-fallback {
    color: var(--brand-accent);
    font: 700 42px/1 Georgia, serif;
}
@keyframes brand-orbit { to { transform: rotate(360deg); } }
@keyframes brand-ring-reverse {
    0% { transform: rotate(0deg) scale(1); opacity: 1; }
    100% { transform: rotate(-430deg) scale(.5); opacity: 0; }
}
@keyframes brand-ring-fade {
    to { transform: scale(.7); opacity: 0; }
}
@keyframes brand-mark-rise {
    0% { transform: translateY(0) scale(1); opacity: 1; }
    35% { transform: translateY(-7px) scale(1.04); opacity: 1; }
    100% { transform: translateY(-115px) scale(.7); opacity: 0; }
}
.brand-trigger.switching .brand-orbit { animation: brand-ring-reverse .62s ease-in forwards; }
.brand-trigger.switching .brand-ring { animation: brand-ring-fade .48s ease-in forwards; }
.brand-trigger.switching .brand-logo,
.brand-trigger.switching .brand-fallback { animation: brand-mark-rise .58s cubic-bezier(.65,0,.8,.25) forwards; }
@media (prefers-reduced-motion: reduce) {
    .brand-orbit { animation: none; }
    .brand-trigger.switching .brand-orbit,
    .brand-trigger.switching .brand-ring,
    .brand-trigger.switching .brand-logo { animation-duration: .12s; }
}
</style>
</head>
<body>
<div class="brand-wrap">
    <button id="brandToggle" class="brand-trigger" aria-label="Switch AlgoBench theme" title="Click to switch theme">
        <span class="brand-ring"><span class="brand-ring-inner"></span></span>
        <span class="brand-orbit"></span>
        <img id="brandLogo" class="brand-logo" alt="AlgoBench logo" style="display:none">
        <span id="brandFallback" class="brand-fallback">A</span>
    </button>
</div>
<script>
(function () {
    let args = {};
    let fired = false;
    const button = document.getElementById('brandToggle');
    const logo = document.getElementById('brandLogo');
    const fallback = document.getElementById('brandFallback');

    function applyArgs(next) {
        args = next || {};
        const root = document.documentElement;
        root.style.setProperty('--brand-accent', args.accent || '#B7BEC2');
        root.style.setProperty('--brand-glow', args.glow || 'rgba(174,183,188,.18)');
        root.style.setProperty('--brand-ring', args.ring || 'rgba(174,183,188,.48)');
        root.style.setProperty('--brand-ring-inner', args.ringInner || 'rgba(174,183,188,.25)');
        root.style.setProperty('--brand-ring-dashed', args.ringDashed || 'rgba(174,183,188,.30)');
        root.style.setProperty('--brand-logo-filter', args.logoFilter || 'none');
        if (args.logo) {
            logo.src = args.logo;
            logo.style.display = 'block';
            fallback.style.display = 'none';
        }
    }

    function sendThemeSwitch() {
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setComponentValue',
            value: true,
            dataType: 'json'
        }, '*');
    }

    button.addEventListener('click', function () {
        if (fired) return;
        fired = true;
        button.disabled = true;
        button.classList.add('switching');
        window.setTimeout(sendThemeSwitch, 640);
    });

    window.addEventListener('message', function (event) {
        if (event.data && event.data.type === 'streamlit:render') {
            applyArgs(event.data.args || {});
        }
    });

    window.parent.postMessage({
        isStreamlitMessage: true,
        type: 'streamlit:componentReady',
        apiVersion: 1
    }, '*');
})();
</script>
</body>
</html>
"""
(SIDEBAR_BRAND_DIR / "index.html").write_text(SIDEBAR_BRAND_HTML, encoding="utf-8")
sidebar_brand_component = components.declare_component(
    "algobench_sidebar_brand",
    path=str(SIDEBAR_BRAND_DIR)
)


# Rolling-text navigation component used in the sidebar (TextRoll effect).
# Each letter slides up and is replaced by the same letter coming from below,
# staggered outwards from the centre of the word.
SIDEBAR_NAV_DIR = Path(tempfile.gettempdir()) / "algobench_sidebar_nav"
SIDEBAR_NAV_DIR.mkdir(exist_ok=True)
SIDEBAR_NAV_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@font-face {
    font-family: "Netflix Sans";
    src: url(data:font/ttf;base64,NAV_FONT_DATA) format("truetype");
    font-style: normal;
    font-weight: 100 900;
    font-display: swap;
}
:root {
    --nav-text: #202319;
    --nav-muted: #6D735F;
    --nav-accent: #68764B;
    --fs: 30px;
}
* { box-sizing: border-box; }
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    background: transparent;
    overflow: hidden;
    font-family: "Netflix Sans", Arial, sans-serif;
}
#wrap { width: 100%; padding: 4px 0 6px; }
ul#navList {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
}
li {
    position: relative;
    cursor: pointer;
    outline: none;
    -webkit-tap-highlight-color: transparent;
}
.roll {
    position: relative;
    display: block;
    overflow: hidden;
    font-size: var(--fs);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.03em;
    line-height: 1.0;
    padding: 0.05em 0.02em;
    white-space: pre;
    /* faux-bold so the single Regular weight of the font reads heavy */
    -webkit-text-stroke: 0.045em currentColor;
}
.layer { display: block; white-space: pre; }
.layer.bottom { position: absolute; left: 0; right: 0; top: 0.05em; text-align: center; }
.ch {
    display: inline-block;
    transition: transform .38s ease-in-out;
    will-change: transform;
}
.layer.top { color: var(--nav-muted); }
.layer.bottom { color: var(--nav-text); }
.layer.top .ch { transform: translateY(0); }
.layer.bottom .ch { transform: translateY(105%); }
li:hover .layer.top .ch,
li:focus-visible .layer.top .ch { transform: translateY(-105%); }
li:hover .layer.bottom .ch,
li:focus-visible .layer.bottom .ch { transform: translateY(0); }

/* Currently selected page */
li.active .layer.top,
li.active .layer.bottom { color: var(--nav-accent); }
li.active .layer.top { color: var(--nav-accent); }

@media (prefers-reduced-motion: reduce) {
    .ch { transition-duration: .01s; }
}
</style>
</head>
<body>
<div id="wrap"><ul id="navList" role="navigation"></ul></div>
<script>
(function () {
    const STAGGER = 0.035;
    const list = document.getElementById('navList');
    const wrap = document.getElementById('wrap');
    let items = [];
    let active = '';
    let builtKey = '';

    function makeLayer(cls, text) {
        const layer = document.createElement('span');
        layer.className = 'layer ' + cls;
        const chars = Array.from(text);
        const mid = (chars.length - 1) / 2;
        chars.forEach(function (ch, i) {
            const s = document.createElement('span');
            s.className = 'ch';
            s.style.transitionDelay = (STAGGER * Math.abs(i - mid)).toFixed(3) + 's';
            s.textContent = ch === ' ' ? '\u00a0' : ch;
            layer.appendChild(s);
        });
        return layer;
    }

    function choose(name) {
        if (!name || name === active) return;

        // Send the page selection immediately. Streamlit handles the rerun;
        // the new page receives a short CSS fade-in from the Python side.
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setComponentValue',
            value: name,
            dataType: 'json'
        }, '*');
    }

    function build() {
        list.innerHTML = '';
        items.forEach(function (name) {
            const li = document.createElement('li');
            li.dataset.name = name;
            li.tabIndex = 0;
            li.setAttribute('role', 'button');
            li.setAttribute('aria-label', name);

            const roll = document.createElement('span');
            roll.className = 'roll';
            roll.appendChild(makeLayer('top', name));
            roll.appendChild(makeLayer('bottom', name));
            li.appendChild(roll);

            li.addEventListener('click', function () { choose(name); });
            li.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    choose(name);
                }
            });
            list.appendChild(li);
        });
    }

    function markActive() {
        list.querySelectorAll('li').forEach(function (li) {
            li.classList.toggle('active', li.dataset.name === active);
        });
    }

    // Shrink the type just enough that the longest label fits the sidebar.
    function fit() {
        const avail = wrap.clientWidth - 8;
        let size = 30;
        document.documentElement.style.setProperty('--fs', size + 'px');
        let widest = 0;
        list.querySelectorAll('.roll').forEach(function (r) {
            widest = Math.max(widest, r.scrollWidth);
        });
        if (widest > avail && avail > 0) {
            size = Math.max(16, Math.floor((size * avail / widest) * 10) / 10);
            document.documentElement.style.setProperty('--fs', size + 'px');
        }
        sendHeight();
    }

    function sendHeight() {
        const h = Math.ceil(wrap.getBoundingClientRect().height) + 4;
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: 'streamlit:setFrameHeight',
            height: h
        }, '*');
    }

    function applyArgs(args) {
        args = args || {};
        const root = document.documentElement;
        root.style.setProperty('--nav-text', args.text || '#202319');
        root.style.setProperty('--nav-muted', args.muted || '#6D735F');
        root.style.setProperty('--nav-accent', args.accent || '#68764B');

        items = args.items || [];
        active = args.active || '';

        const key = items.join('|');
        if (key !== builtKey) {
            builtKey = key;
            build();
        }
        markActive();
        fit();
    }

    window.addEventListener('message', function (event) {
        if (event.data && event.data.type === 'streamlit:render') {
            applyArgs(event.data.args || {});
        }
    });
    window.addEventListener('resize', fit);
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(fit);
    }

    window.parent.postMessage({
        isStreamlitMessage: true,
        type: 'streamlit:componentReady',
        apiVersion: 1
    }, '*');
})();
</script>
</body>
</html>
"""
SIDEBAR_NAV_HTML = SIDEBAR_NAV_HTML.replace("NAV_FONT_DATA", FONT_BASE64)
(SIDEBAR_NAV_DIR / "index.html").write_text(SIDEBAR_NAV_HTML, encoding="utf-8")
sidebar_nav_component = components.declare_component(
    "algobench_sidebar_nav",
    path=str(SIDEBAR_NAV_DIR)
)

NAV_ITEMS = [
    "Overview",
    "Run Benchmark",
    "Compare Results",
    "Profiler",
    "Algorithm Library",
    "History"
]

if "bright_theme" not in st.session_state:
    st.session_state.bright_theme = True

if "current_page" not in st.session_state:
    st.session_state.current_page = NAV_ITEMS[0]


# Theme palette
if st.session_state.bright_theme:
    theme = {
        "bg": "#F3F4ED",
        "sidebar": "#E9EBDD",
        "panel": "#FFFFFF",
        "panel_raised": "#F7F8F2",
        "border": "#D8DDCA",
        "text": "#202319",
        "muted": "#6D735F",
        "accent": "#68764B",
        "accent_soft": "#EEF1E5",
        "input": "#FFFFFF",
        "header": "#F3F4ED",
        "glow": "rgba(112, 132, 72, .17)",
        "hero_glow": "rgba(112, 132, 72, .21)",
        "grid_glow": "rgba(112, 132, 72, .13)",
        "shadow": "0 8px 26px rgba(50, 60, 35, .07)",
        "button_end": "#879568",
        "button_text": "#FFFFFF",
        "button_glow": "rgba(104, 118, 75, .20)",
        "arrow_color": "#000000",
        "logo_filter": "hue-rotate(-78deg) saturate(.78) brightness(.82)",
        "logo_ring": "rgba(104, 118, 75, .52)",
        "logo_ring_inner": "rgba(104, 118, 75, .27)",
        "logo_ring_dashed": "rgba(104, 118, 75, .32)"
    }
else:
    theme = {
        "bg": "#111315",
        "sidebar": "#17191B",
        "panel": "#1C1F22",
        "panel_raised": "#24282B",
        "border": "#3A4044",
        "text": "#F0F1F2",
        "muted": "#A8AFB3",
        "accent": "#B7BEC2",
        "accent_soft": "#292E32",
        "input": "#202427",
        "header": "#111315",
        "glow": "rgba(174, 183, 188, .15)",
        "hero_glow": "rgba(174, 183, 188, .19)",
        "grid_glow": "rgba(190, 198, 202, .10)",
        "shadow": "0 10px 32px rgba(0, 0, 0, .24)",
        "button_end": "#858D92",
        "button_text": "#111315",
        "button_glow": "rgba(190, 198, 202, .16)",
        "arrow_color": "#D0D5D8",
        "logo_filter": "none",
        "logo_ring": "rgba(183, 190, 194, .50)",
        "logo_ring_inner": "rgba(183, 190, 194, .26)",
        "logo_ring_dashed": "rgba(183, 190, 194, .31)"
    }

css = r'''
@font-face {
    font-family: "Netflix Sans";
    src: url(data:font/ttf;base64,__FONT__) format("truetype");
    font-style: normal;
    font-weight: 100 900;
    font-display: swap;
}
:root {
    --bg: __BG__;
    --sidebar: __SIDEBAR__;
    --panel: __PANEL__;
    --panel-raised: __PANEL_RAISED__;
    --border: __BORDER__;
    --text: __TEXT__;
    --muted: __MUTED__;
    --accent: __ACCENT__;
    --accent-soft: __ACCENT_SOFT__;
    --input: __INPUT__;
    --header: __HEADER__;
    --shadow: __SHADOW__;
}
/* Apply the custom font to ordinary UI text, not icon glyphs. */
html, body, .stApp, h1, h2, h3, h4, p, label, input, textarea,
[data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    font-family: "Netflix Sans", Arial, sans-serif !important;
}
/* Streamlit uses Material Symbols for its sidebar expand/collapse arrows.
   Do not let the Netflix Sans override turn their glyph names into text. */
.material-icons, .material-symbols-rounded, .material-symbols-outlined,
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap;
    -webkit-font-feature-settings: "liga";
    font-feature-settings: "liga";
}

/* High-contrast collapse arrow INSIDE the open sidebar (both themes). */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button {
    color: var(--accent) !important;
    opacity: 1 !important;
    background: var(--accent-soft) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    box-shadow: var(--shadow) !important;
}

[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
    color: var(--accent) !important;
    fill: currentColor !important;
    opacity: 1 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    filter: none !important;
}

[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    background: var(--panel-raised) !important;
    border-color: var(--accent) !important;
}

[data-testid="stSidebarCollapseButton"] button:focus-visible {
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px !important;
}
.ab-brand-name { color:var(--text); font-size:30px; font-weight:800; line-height:1.1; white-space:nowrap; }
.ab-brand-tagline { color:var(--muted); font-size:9px; letter-spacing:2px; margin-top:6px; white-space:nowrap; }
.ab-brand-hint { color:var(--muted); font-size:8px; letter-spacing:1.4px; margin-top:7px; opacity:.8; }
.stApp {
    background:
        radial-gradient(ellipse at 52% -8%, __GLOW__ 0%, transparent 43%),
        linear-gradient(145deg, var(--bg), var(--bg));
    color: var(--text);
}
[data-testid="stHeader"] {
    background: var(--header);
}
[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.8rem;
}
/* Keep the rolling-text navigation iframe transparent on the sidebar. */
[data-testid="stSidebar"] iframe {
    background: transparent !important;
    color-scheme: normal;
}
.block-container {
    max-width: 1500px;
    padding-top: 2.1rem;
    padding-bottom: 4rem;
}
h1, h2, h3, h4 {
    color: var(--text) !important;
    letter-spacing: -0.55px;
}
h1 { font-weight: 700 !important; }
h2, h3 { font-weight: 650 !important; }
p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }

[data-testid="stMetric"] {
    background: linear-gradient(145deg, var(--panel-raised), var(--panel));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 19px 20px;
    box-shadow: var(--shadow);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 700;
}
[data-testid="stMetricDelta"] { font-size: 12px; }

.ab-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, var(--panel-raised), var(--panel));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 14px;
    box-shadow: var(--shadow);
    transition: transform .2s ease, border-color .2s ease;
}
.ab-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
}
.ab-icon {
    font-size: 25px;
    margin-bottom: 14px;
    color: var(--accent);
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ab-icon svg {
    width: 34px;
    height: 34px;
    display: block;
}
.ab-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 650;
    margin-bottom: 8px;
}

/* Click-triggered PointerHighlight treatment for the five domain headings. */
.ab-domain-trigger {
    position: relative;
    display: inline-flex;
    align-items: center;
    max-width: 100%;
    padding: 4px 9px 5px 0;
    margin: -4px 0 4px -1px;
    border: 0;
    border-radius: 5px;
    background: transparent;
    color: var(--text);
    font: inherit;
    font-size: 18px;
    font-weight: 650;
    line-height: 1.3;
    text-align: left;
    cursor: pointer;
    isolation: isolate;
    -webkit-tap-highlight-color: transparent;
}

.ab-domain-trigger::before {
    content: "";
    position: absolute;
    inset: -3px -8px;
    z-index: -1;
    border: 1.35px solid var(--accent);
    border-radius: 6px;
    background: color-mix(in srgb, var(--accent) 8%, transparent);
    clip-path: inset(0 100% 0 0 round 6px);
    opacity: 0;
    pointer-events: none;
}

.ab-domain-trigger.is-pointer-active::before {
    opacity: 1;
    animation: ab-pointer-outline-draw .62s cubic-bezier(.16, 1, .3, 1) forwards;
}

.ab-domain-cursor {
    position: absolute;
    z-index: 2;
    left: 0;
    top: 50%;
    width: 19px;
    height: 24px;
    opacity: 0;
    transform: translate(-48%, -12%) rotate(-9deg);
    transform-origin: 15% 10%;
    pointer-events: none;
    filter: drop-shadow(0 2px 3px rgba(0, 0, 0, .24));
}

.ab-domain-trigger.is-pointer-active .ab-domain-cursor {
    animation: ab-pointer-cursor-sweep .78s cubic-bezier(.22, .78, .25, 1) forwards;
}

.ab-domain-trigger:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 5px;
}

@keyframes ab-pointer-outline-draw {
    0% {
        clip-path: inset(0 100% 0 0 round 6px);
        opacity: .35;
    }
    70% {
        clip-path: inset(0 0 0 0 round 6px);
        opacity: 1;
    }
    100% {
        clip-path: inset(0 0 0 0 round 6px);
        opacity: 1;
    }
}

@keyframes ab-pointer-cursor-sweep {
    0% {
        left: 0;
        opacity: 0;
        transform: translate(-48%, -12%) rotate(-9deg) scale(.82);
    }
    12% { opacity: 1; }
    76% {
        opacity: 1;
        transform: translate(-48%, -12%) rotate(-9deg) scale(1);
    }
    100% {
        left: calc(100% - 2px);
        opacity: 0;
        transform: translate(-48%, -12%) rotate(-9deg) scale(.94);
    }
}

@media (prefers-reduced-motion: reduce) {
    .ab-domain-trigger.is-pointer-active::before {
        animation: none;
        clip-path: inset(0 0 0 0 round 6px);
    }
    .ab-domain-trigger.is-pointer-active .ab-domain-cursor {
        animation: none;
        opacity: 0;
    }
}
.ab-description {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
}
.ab-label {
    color: var(--accent);
    font-size: 10px;
    letter-spacing: 1.8px;
    font-weight: 700;
}
.ab-hero {
    --tilt-x: 0deg;
    --tilt-y: 0deg;
    --lift-y: 0px;
    --card-scale: 1;
    --pointer-x: 50%;
    --pointer-y: 50%;
    position: relative;
    overflow: hidden;
    transform:
        perspective(1250px)
        rotateX(var(--tilt-y))
        rotateY(var(--tilt-x))
        translateY(var(--lift-y))
        scale(var(--card-scale));
    transform-style: preserve-3d;
    transform-origin: center center;
    background:
        radial-gradient(circle at 78% 22%, __HERO_GLOW__, transparent 33%),
        linear-gradient(120deg, var(--panel-raised), var(--panel));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 42px;
    margin: 15px 0 28px 0;
    box-shadow: var(--shadow);
    transition:
        transform 520ms cubic-bezier(.2,.75,.25,1),
        box-shadow 420ms cubic-bezier(.2,.75,.25,1),
        border-color 300ms ease;
    will-change: transform;
    backface-visibility: hidden;
}

/* A soft light sheen follows the pointer across the card surface. */
.ab-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 1;
    border-radius: inherit;
    pointer-events: none;
    opacity: 0;
    background:
        radial-gradient(
            420px circle at var(--pointer-x) var(--pointer-y),
            rgba(255,255,255,.19),
            rgba(255,255,255,.07) 28%,
            transparent 68%
        );
    transition: opacity 220ms ease;
}

/* During pointer movement, the tilt follows the cursor with minimal lag. */
.ab-hero.is-tilting {
    transition:
        transform 80ms linear,
        box-shadow 120ms ease,
        border-color 180ms ease;
    border-color: var(--accent);
}

.ab-hero.is-tilting::before {
    opacity: 1;
}

/* Keep the existing subtle technical grid above the sheen. */
.ab-hero::after {
    z-index: 2;
}

/* Lift the hero's text and badge slightly forward to create layered depth. */
.ab-hero > * {
    position: relative;
    z-index: 3;
    transform: translateZ(24px);
}

@media (prefers-reduced-motion: reduce) {
    .ab-hero,
    .ab-hero.is-tilting {
        transition: none;
        transform: none;
    }
    .ab-hero::before {
        display: none;
    }
}
.ab-hero:after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: .16;
    background-image:
        linear-gradient(__GRID_GLOW__ 1px, transparent 1px),
        linear-gradient(90deg, __GRID_GLOW__ 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: linear-gradient(90deg, transparent, black);
}
.ab-hero-title {
    position: relative;
    z-index: 1;
    color: var(--text);
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 750;
    letter-spacing: -2px;
    line-height: 1.08;
}
.ab-hero-sub {
    position: relative;
    z-index: 1;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.8;
    max-width: 660px;
}
.ab-divider {
    height: 1px;
    background: var(--border);
    margin: 21px 0;
}
.ab-status {
    display: inline-block;
    padding: 6px 11px;
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 650;
}
.ab-mono { color: var(--accent); font-size: 12px; }

div.stButton > button {
    background: linear-gradient(100deg, var(--accent), __BUTTON_END__);
    color: __BUTTON_TEXT__;
    border: 1px solid transparent;
    border-radius: 8px;
    font-weight: 700;
    min-height: 43px;
    transition: .2s ease;
}
div.stButton > button:hover {
    filter: brightness(1.08);
    border-color: var(--accent);
    color: __BUTTON_TEXT__;
    box-shadow: 0 5px 22px __BUTTON_GLOW__;
}

/* Run Benchmark: keep this button label black in both bright and dark themes. */
.st-key-prepare_benchmark_configuration button,
.st-key-prepare_benchmark_configuration button p,
.st-key-prepare_benchmark_configuration button:hover,
.st-key-prepare_benchmark_configuration button:hover p {
    color: #000000 !important;
}
div[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: var(--input);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
}
.stTextInput input, .stNumberInput input {
    background: var(--input);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
}
[data-baseweb="popover"], [data-baseweb="menu"] {
    background: var(--panel-raised);
}
div[role="radiogroup"] { gap: 8px; }
[data-testid="stRadio"] label { color: var(--text); }
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 9px; }
[data-testid="stToggle"] label { color: var(--text) !important; }

/* ------------------------------------------------------------------
   Sidebar EXPAND arrow (shown when the sidebar is closed).
   Works with both Streamlit naming schemes:
     - [data-testid="stSidebarCollapsedControl"] (wrapper) > button
     - [data-testid="stExpandSidebarButton"]
   The native icon is hidden and a single high-contrast "»" is drawn
   on ONE element only, so it can never be doubled or invisible.
------------------------------------------------------------------- */

/* 1) The fixed, boxed container pinned to the top-left corner. */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"]:not([data-testid="stSidebarCollapsedControl"] *) {
    position: fixed !important;
    top: 14px !important;
    left: 14px !important;
    z-index: 999999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px !important;
    min-height: 44px !important;
    padding: 0 !important;
    margin: 0 !important;
    background: var(--accent-soft) !important;
    border: 2px solid __ARROW_COLOR__ !important;
    border-radius: 10px !important;
    opacity: 1 !important;
    visibility: visible !important;
    box-shadow: var(--shadow) !important;
}

/* 2) The clickable button itself (transparent, fills the box). */
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stExpandSidebarButton"],
button[data-testid="stSidebarCollapsedControl"] {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    height: 100% !important;
    min-width: 40px !important;
    min-height: 40px !important;
    padding: 0 !important;
    margin: 0 !important;
    color: __ARROW_COLOR__ !important;
    background: transparent;
    border: 0;
    border-radius: 9px !important;
    opacity: 1 !important;
    visibility: visible !important;
    box-shadow: none;
    cursor: pointer !important;
    font-size: 0 !important;
    line-height: 0 !important;
}

/* 3) Hide Streamlit's native icon so only our arrow is drawn. */
[data-testid="stSidebarCollapsedControl"] button *,
[data-testid="stExpandSidebarButton"] *,
button[data-testid="stSidebarCollapsedControl"] * {
    display: none !important;
}

/* 4) Draw ONE clearly visible double arrow. */
[data-testid="stSidebarCollapsedControl"] button::after,
[data-testid="stExpandSidebarButton"]::after,
button[data-testid="stSidebarCollapsedControl"]::after {
    content: "\00BB" !important;
    position: absolute !important;
    inset: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 3px 4px 0 !important;
    color: __ARROW_COLOR__ !important;
    font-family: Arial, Helvetica, sans-serif !important;
    font-size: 30px !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    letter-spacing: -4px !important;
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: none !important;
    z-index: 10 !important;
}

[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="stExpandSidebarButton"]:hover {
    background: var(--panel-raised) !important;
    transform: none !important;
}

[data-testid="stSidebarCollapsedControl"] button:focus-visible,
[data-testid="stExpandSidebarButton"]:focus-visible {
    outline: 2px solid __ARROW_COLOR__ !important;
    outline-offset: 2px !important;
}


/* Gentle page-entry transition: fast navigation with a soft visual settle. */
@keyframes algobench-page-enter {
    0% {
        opacity: .18;
        transform: translate3d(0, 7px, 0);
    }
    65% {
        opacity: .88;
        transform: translate3d(0, 1px, 0);
    }
    100% {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stAppViewContainer"] > .main {
        animation: none !important;
    }
}

footer, #MainMenu { visibility: hidden; }
'''

values = {
    "__FONT__": FONT_BASE64,
    "__BG__": theme["bg"],
    "__SIDEBAR__": theme["sidebar"],
    "__PANEL__": theme["panel"],
    "__PANEL_RAISED__": theme["panel_raised"],
    "__BORDER__": theme["border"],
    "__TEXT__": theme["text"],
    "__MUTED__": theme["muted"],
    "__ACCENT__": theme["accent"],
    "__ACCENT_SOFT__": theme["accent_soft"],
    "__INPUT__": theme["input"],
    "__HEADER__": theme["header"],
    "__GLOW__": theme["glow"],
    "__HERO_GLOW__": theme["hero_glow"],
    "__GRID_GLOW__": theme["grid_glow"],
    "__SHADOW__": theme["shadow"],
    "__BUTTON_END__": theme["button_end"],
    "__BUTTON_TEXT__": theme["button_text"],
    "__BUTTON_GLOW__": theme["button_glow"],
    "__ARROW_COLOR__": theme["arrow_color"]
}
for key, value in values.items():
    css = css.replace(key, value)

st.markdown(f"""<style>{css}</style>""", unsafe_allow_html=True)


# First-visit cinematic logo landing page.
if "entered_dashboard" not in st.session_state:
    st.session_state.entered_dashboard = False

if not st.session_state.entered_dashboard:
    st.markdown("""
    <style>
    /* Make the Streamlit host page match the dark intro canvas. */
    html, body, #root, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stAppViewBlockContainer"] {
        background: #111315 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Remove Streamlit's reserved top bar and its layout gap. */
    header, [data-testid="stHeader"], .stAppHeader,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"],
    .block-container {
        background: #111315 !important;
        max-width: none !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    iframe {
        display: block !important;
        border: 0 !important;
        width: 100% !important;
        margin: 0 !important;
        vertical-align: top !important;
    }
    </style>
    """, unsafe_allow_html=True)

    intro_finished = landing_component(
        logo=LOGO_DATA_URI or "",
        bg="#111315",
        panel="#1C1F22",
        text="#F0F1F2",
        muted="#A8AFB3",
        accent="#B7BEC2",
        glow="rgba(174,183,188,.15)",
        key="algobench_intro",
        default=False,
        height=790,
        scrolling=False
    )

    if intro_finished:
        st.session_state.entered_dashboard = True
        st.session_state.animate_dashboard_reveal = True
        st.session_state.force_sidebar_expand = True
        st.rerun()

    st.stop()

if st.session_state.pop("animate_dashboard_reveal", False):
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        animation: dashboard-arrive .72s cubic-bezier(.2,.7,.2,1) both;
    }
    @keyframes dashboard-arrive {
        from { opacity: 0; transform: translateY(18px) scale(.992); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

    # Streamlit can retain a previously collapsed sidebar across reruns.
    # Expand it once when arriving from the cinematic landing screen.
    
# SIDEBAR

with st.sidebar:

    if LOGO_DATA_URI is None:
        st.warning("Logo_Final.svg was not found in the AlgoBench project folder.")

    brand_left, brand_right = st.columns([1.25, 3.8], vertical_alignment="center", gap="small")
    with brand_left:
        theme_clicked = sidebar_brand_component(
            logo=LOGO_DATA_URI or "",
            accent=theme["accent"],
            glow=theme["button_glow"],
            ring=theme["logo_ring"],
            ringInner=theme["logo_ring_inner"],
            ringDashed=theme["logo_ring_dashed"],
            logoFilter=theme["logo_filter"],
            key=f"sidebar_theme_mark_{'bright' if st.session_state.bright_theme else 'dark'}",
            default=False,
            height=90,
            scrolling=False
        )

    with brand_right:
        st.markdown(f"""
        <div style="padding:0 0 4px 0">
            <div class="ab-brand-name">AlgoBench</div>
            <div class="ab-brand-tagline">NEXUS PERFORMANCE LAB</div>
            <div class="ab-brand-hint">CLICK THE MARK TO SWITCH THEME</div>
        </div>
        """, unsafe_allow_html=True)

    if theme_clicked:
        st.session_state.bright_theme = not st.session_state.bright_theme
        st.session_state.page_transition_enter = True
        st.rerun()

    st.markdown('<div class="ab-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="ab-label">WORKSPACE</div>', unsafe_allow_html=True)

    # Rolling-text navigation (replaces the old st.radio).
    nav_choice = sidebar_nav_component(
        items=NAV_ITEMS,
        active=st.session_state.current_page,
        text=theme["text"],
        muted=theme["muted"],
        accent=theme["accent"],
        key="sidebar_nav_roll",
        default=None,
        scrolling=False
    )

    if (
        nav_choice
        and nav_choice in NAV_ITEMS
        and nav_choice != st.session_state.current_page
    ):
        st.session_state.current_page = nav_choice
        st.session_state.page_transition_enter = True
        st.rerun()

    page = st.session_state.current_page

    st.markdown('<div class="ab-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ab-card">
        <div class="ab-label">SYSTEM STATUS</div>
        <br>
        <span class="ab-status">● INTERFACE ONLINE</span>
        <br><br>
        <div class="ab-description">
            Benchmark engine integration is under development.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="padding:10px 5px;color:{theme["muted"]};font-size:11px">
        ALGOBENCH NEXUS<br>
        VERSION 1.0.0
    </div>
    """, unsafe_allow_html=True)


# A lightweight 220 ms fade-in on page/theme changes.
# No JavaScript timers or hidden-state manipulation: navigation stays immediate.
if st.session_state.pop("page_transition_enter", False):
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] > .main {
            animation: algobench-page-enter 300ms cubic-bezier(.22, 1, .36, 1) both !important;
            will-change: opacity, transform;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# TOP BAR

_, right = st.columns([5, 1])

with right:
    st.markdown(
        '<div style="text-align:right"><span class="ab-status">● READY</span></div>',
        unsafe_allow_html=True
    )


# OVERVIEW PAGE

if page == "Overview":

    st.markdown("""
    <div class="ab-hero">
        <div class="ab-label">WELCOME TO THE PERFORMANCE LAB</div>
        <br>
        <div class="ab-hero-title">
            Measure. Analyze.<br>
            Optimize.
        </div>
        <br>
        <div class="ab-hero-sub">
            An integrated environment for algorithm benchmarking,
            computational profiling and performance analysis.
            Discover how algorithms behave as input complexity grows.
        </div>
        <br>
        <span class="ab-status">● PLATFORM INITIALIZED</span>
    </div>
    """, unsafe_allow_html=True)

    # Cursor-tracking 3D effect for the Overview hero only.
    # This small bridge attaches pointer listeners to the rendered .ab-hero
    # element in the Streamlit page; no other cards or dashboard sections change.
    components.html(
        """
        <script>
        (() => {
            let attempts = 0;
            const maxAttempts = 30;

            function attachCometInteraction() {
                let hostDocument;

                try {
                    hostDocument = window.parent.document;
                } catch (error) {
                    return;
                }

                const card = hostDocument.querySelector(".ab-hero");

                if (!card) {
                    attempts += 1;
                    if (attempts < maxAttempts) {
                        window.setTimeout(attachCometInteraction, 120);
                    }
                    return;
                }

                if (card.dataset.cometPointerReady === "true") return;
                card.dataset.cometPointerReady = "true";

                const hostWindow = window.parent;
                const reducedMotion = hostWindow.matchMedia(
                    "(prefers-reduced-motion: reduce)"
                ).matches;
                const finePointer = hostWindow.matchMedia(
                    "(hover: hover) and (pointer: fine)"
                ).matches;

                if (reducedMotion || !finePointer) return;

                function handlePointerMove(event) {
                    const rect = card.getBoundingClientRect();
                    if (!rect.width || !rect.height) return;

                    const localX = Math.max(
                        0, Math.min(rect.width, event.clientX - rect.left)
                    );
                    const localY = Math.max(
                        0, Math.min(rect.height, event.clientY - rect.top)
                    );

                    const normalizedX = (localX / rect.width - 0.5) * 2;
                    const normalizedY = (localY / rect.height - 0.5) * 2;

                    // The face turns toward the pointer, with restrained angles.
                    const rotateY = normalizedX * 10;
                    const rotateX = normalizedY * -8;

                    card.style.setProperty("--tilt-x", rotateY.toFixed(2) + "deg");
                    card.style.setProperty("--tilt-y", rotateX.toFixed(2) + "deg");
                    card.style.setProperty("--lift-y", "-7px");
                    card.style.setProperty("--card-scale", "1.008");
                    card.style.setProperty(
                        "--pointer-x",
                        (localX / rect.width * 100).toFixed(2) + "%"
                    );
                    card.style.setProperty(
                        "--pointer-y",
                        (localY / rect.height * 100).toFixed(2) + "%"
                    );

                    // Offset the shadow opposite the cursor to strengthen depth.
                    const shadowX = (-normalizedX * 19).toFixed(1);
                    const shadowY = (23 - normalizedY * 13).toFixed(1);
                    card.style.boxShadow =
                        shadowX + "px " + shadowY +
                        "px 48px rgba(0,0,0,.19), var(--shadow)";

                    card.classList.add("is-tilting");
                }

                function resetCard() {
                    card.classList.remove("is-tilting");
                    card.style.setProperty("--tilt-x", "0deg");
                    card.style.setProperty("--tilt-y", "0deg");
                    card.style.setProperty("--lift-y", "0px");
                    card.style.setProperty("--card-scale", "1");
                    card.style.setProperty("--pointer-x", "50%");
                    card.style.setProperty("--pointer-y", "50%");
                    card.style.boxShadow = "";
                }

                card.addEventListener("pointermove", handlePointerMove, {
                    passive: true
                });
                card.addEventListener("pointerleave", resetCard, {
                    passive: true
                });
                card.addEventListener("pointercancel", resetCard, {
                    passive: true
                });
            }

            // Give Streamlit time to finish inserting the hero markup.
            window.setTimeout(attachCometInteraction, 80);
        })();
        </script>
        """,
        height=0,
        scrolling=False
    )

    st.markdown("### Platform Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Algorithm Categories","05")
    c2.metric("Algorithm Implementations","15+")
    c3.metric("Analysis Tools","03")
    c4.metric("Benchmark Engine","Pending")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Explore Algorithm Domains")
    st.caption("Select a domain to configure and analyze its algorithms.")

    
    sorting_svg = """
    <svg xmlns="http://www.w3.org/2000/svg"
        width="34" height="34" viewBox="0 0 40 40"
        fill="none" stroke="currentColor"
        stroke-width="2.2" stroke-linecap="round"
        stroke-linejoin="round">
        <path d="M5 34H36"/>
        <rect x="8" y="23" width="6" height="11" rx="1.5"/>
        <rect x="18" y="16" width="6" height="18" rx="1.5"/>
        <rect x="28" y="8" width="6" height="26" rx="1.5"/>
        <path d="M8 15L17 10L24 12L34 4"/>
        <path d="M27 4H34V11"/>
    </svg>
    """

    categories = [
        ("01", sorting_svg, "Sorting",
        "Quick, Merge, Heap and Insertion Sort", "O(n log n)"),
        ("02", "⌕", "Searching",
        "Linear, Binary and Hash Table Lookup", "O(log n)"),
        ("03", "◈", "Graph Algorithms",
        "Dijkstra, Bellman-Ford and BFS", "O(V + E)"),
        ("04", "▦", "Dynamic Programming",
        "LCS and 0/1 Knapsack", "DP"),
        ("05", "▧", "Matrix Algorithms",
        "Standard and Strassen Multiplication", "O(n³)")
    ]

    cols = st.columns(3)

    for i, (number,icon,title,desc,complexity) in enumerate(categories):

        with cols[i % 3]:
            st.markdown(f"""
            <div class="ab-card">
                <div class="ab-label">DOMAIN {number}</div>
                <div class="ab-icon">{icon}</div>
                <div class="ab-title">
                    <button type="button"
                            class="ab-domain-trigger"
                            aria-label="Highlight {title} domain"
                            title="Click to highlight {title}">
                        <span>{title}</span>
                        <svg class="ab-domain-cursor"
                             viewBox="0 0 24 30"
                             aria-hidden="true"
                             xmlns="http://www.w3.org/2000/svg">
                            <path d="M2 1.5L2.5 24L8.1 18.3L12.4 27.8L16.2 26L11.8 16.8L20.3 16.1Z"
                                  fill="var(--accent)"
                                  stroke="var(--panel)"
                                  stroke-width="1.25"
                                  stroke-linejoin="round"/>
                        </svg>
                    </button>
                </div>
                <div class="ab-description">{desc}</div>
                <br>
                <div class="ab-mono">{complexity}</div>
            </div>
            """, unsafe_allow_html=True)

    # Attach the click-to-highlight animation to the five domain headings.
    # Only the clicked heading is highlighted; clicking another moves the
    # selection to that heading. The script is safe across Streamlit reruns.
    components.html(
        """
        <script>
        (() => {
            let attempts = 0;
            const maxAttempts = 30;

            function attachPointerHighlights() {
                let hostDocument;

                try {
                    hostDocument = window.parent.document;
                } catch (error) {
                    return;
                }

                const headings = Array.from(
                    hostDocument.querySelectorAll(".ab-domain-trigger")
                );

                if (!headings.length) {
                    attempts += 1;
                    if (attempts < maxAttempts) {
                        window.setTimeout(attachPointerHighlights, 120);
                    }
                    return;
                }

                headings.forEach((heading) => {
                    if (heading.dataset.pointerHighlightReady === "true") return;
                    heading.dataset.pointerHighlightReady = "true";

                    heading.addEventListener("click", () => {
                        headings.forEach((item) => {
                            item.classList.remove("is-pointer-active");
                        });

                        // Force a fresh animation even when the same heading
                        // is clicked repeatedly.
                        void heading.offsetWidth;
                        heading.classList.add("is-pointer-active");
                    });
                });
            }

            attachPointerHighlights();
        })();
        </script>
        """,
        height=0,
        scrolling=False
    )

    st.markdown("### Analysis Pipeline")

    p1,p2,p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="ab-card">
            <div class="ab-label">01 / EXECUTION</div>
            <div class="ab-title">Benchmark</div>
            <div class="ab-description">
                Generate datasets and execute algorithms
                across different input sizes.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="ab-card">
            <div class="ab-label">02 / INVESTIGATION</div>
            <div class="ab-title">Profile</div>
            <div class="ab-description">
                Inspect execution time, memory allocation
                and computational bottlenecks.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="ab-card">
            <div class="ab-label">03 / INTELLIGENCE</div>
            <div class="ab-title">Visualize</div>
            <div class="ab-description">
                Compare performance trends and
                analyze algorithmic efficiency.
            </div>
        </div>
        """, unsafe_allow_html=True)


# RUN BENCHMARK PAGE

elif page == "Run Benchmark":

    st.title("Benchmark Configuration")
    st.caption("Design and configure your algorithm performance experiment.")

    st.markdown("""
    <div class="ab-card">
        <div class="ab-label">EXPERIMENT CONTROL CENTER</div>
        <div class="ab-title">Configure your workload</div>
        <div class="ab-description">
            Select algorithms, define dataset characteristics and
            configure execution parameters before benchmarking.
        </div>
    </div>
    """, unsafe_allow_html=True)

    algorithm_options = {
        "Sorting": [
            "Quick Sort",
            "Merge Sort",
            "Heap Sort",
            "Insertion Sort"
        ],
        "Searching": [
            "Linear Search",
            "Binary Search",
            "Hash Table Lookup"
        ],
        "Graph": [
            "Dijkstra",
            "Bellman-Ford",
            "BFS"
        ],
        "Dynamic Programming": [
            "LCS - Memoization",
            "LCS - Tabulation",
            "Knapsack - Memoization",
            "Knapsack - Tabulation"
        ],
        "Matrix": [
            "Standard Multiplication",
            "Strassen Multiplication"
        ]
    }

    input_options = {
        "Sorting": [
            "Random",
            "Sorted",
            "Reverse Sorted",
            "Nearly Sorted"
        ],
        "Searching": [
            "Random",
            "Sorted",
            "Reverse Sorted"
        ],
        "Graph": [
            "Sparse",
            "Dense"
        ],
        "Dynamic Programming": [
            "Random"
        ],
        "Matrix": [
            "Random"
        ]
    }

    st.markdown("### 01 / Algorithm Selection")

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Algorithm Category",
            list(algorithm_options.keys()),
            key="benchmark_category"
        )

    with col2:
        algorithms = st.multiselect(
            "Select Algorithms",
            algorithm_options[category],
            default=algorithm_options[category][:1],
            key="benchmark_algorithms"
        )

    st.markdown('<div class="ab-divider"></div>',
                unsafe_allow_html=True)

    st.markdown("### 02 / Dataset Configuration")

    col1, col2 = st.columns(2)

    with col1:
        input_size = st.selectbox(
            "Dataset Size",
            [100, 500, 1000, 5000, 10000, 50000],
            index=2
        )

    with col2:
        input_type = st.selectbox(
            "Input Distribution",
            input_options[category]
        )

    if category == "Sorting":
        st.caption(
            "Dataset size represents the number of array elements."
        )

    elif category == "Searching":
        st.caption(
            "Dataset size represents the number of elements "
            "in the search collection."
        )

    elif category == "Graph":
        st.caption(
            "Dataset size represents the number of graph vertices. "
            "The generator will determine the number of edges "
            "based on graph density."
        )

    elif category == "Dynamic Programming":
        st.caption(
            "Dataset size represents the input length or number "
            "of items, depending on the selected algorithm."
        )

    elif category == "Matrix":
        st.caption(
            "Dataset size represents the dimension of square matrices."
        )

    if category == "Searching":
        search_mode = st.radio(
            "Search Query Type",
            ["Successful Search", "Unsuccessful Search"],
            horizontal=True
        )
    else:
        search_mode = None

    st.markdown('<div class="ab-divider"></div>',
                unsafe_allow_html=True)

    st.markdown("### 03 / Execution Parameters")

    col1, col2 = st.columns(2)

    with col1:
        trials = st.number_input(
            "Number of Trials",
            min_value=1,
            max_value=50,
            value=5,
            step=1
        )

    with col2:
        random_seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=999999,
            value=42,
            step=1
        )

    st.caption(
        "Using the same random seed helps reproduce generated datasets."
    )

    st.markdown('<div class="ab-divider"></div>',
                unsafe_allow_html=True)

    st.markdown("### 04 / Experiment Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Algorithms Selected", len(algorithms))
    col2.metric("Dataset Size", f"{input_size:,}")
    col3.metric("Total Trials", len(algorithms) * trials)

    if category == "Searching" and "Binary Search" in algorithms:
        if input_type != "Sorted":
            st.warning(
                "Binary Search requires sorted input. "
                "The dataset generator must sort the data before searching."
            )

    if st.button(
        "Prepare Benchmark Configuration",
        use_container_width=True,
        key="prepare_benchmark_configuration"
    ):

        if not algorithms:
            st.error("Please select at least one algorithm.")

        else:
            config = {
                "category": category,
                "algorithms": algorithms,
                "input_size": input_size,
                "input_type": input_type,
                "trials": int(trials),
                "random_seed": int(random_seed),
                "search_mode": search_mode
            }

            st.session_state["benchmark_config"] = config

            st.success(
                "Benchmark configuration prepared successfully!"
            )

    if "benchmark_config" in st.session_state:

        st.markdown("### Prepared Experiment")

        st.json(st.session_state["benchmark_config"])

        st.info(
            "Configuration is ready. Actual execution will be enabled "
            "after integration with the benchmarking engine."
        )


# COMPARE RESULTS

elif page == "Compare Results":

    st.title("Performance Comparison")
    st.caption("Analyze actual algorithm benchmarking results.")

    results = st.session_state.get("benchmark_results", [])

    if results:
        show_benchmark_metrics(results)

        st.markdown("---")

        show_runtime_chart(results)

        st.markdown("---")

        show_csv_download(results)

    else:
        st.info(
            "No benchmark results available yet. "
            "Run an experiment to see performance comparisons."
        )
# PROFILER

elif page == "Profiler":

    st.title("Execution Profiler")
    st.caption("Investigate runtime behaviour and computational bottlenecks.")

    c1,c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="ab-card">
            <div class="ab-label">RUNTIME ANALYSIS</div>
            <div class="ab-title">cProfile / pstats</div>
            <div class="ab-description">
                Identify expensive functions, call counts
                and cumulative execution time.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="ab-card">
            <div class="ab-label">MEMORY ANALYSIS</div>
            <div class="ab-title">tracemalloc</div>
            <div class="ab-description">
                Inspect Python memory allocations
                and identify memory-intensive operations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.info("Profiler integration will be added with the benchmarking engine.")


# ALGORITHM LIBRARY

elif page == "Algorithm Library":

    st.title("Algorithm Library")
    st.caption("Explore supported algorithms and their theoretical complexity.")

    data = {
        "Category": [
            "Sorting","Sorting","Sorting","Sorting",
            "Searching","Searching","Searching",
            "Graph","Graph","Graph",
            "Dynamic Programming","Dynamic Programming",
            "Matrix","Matrix"
        ],
        "Algorithm": [
            "Quick Sort","Merge Sort","Heap Sort","Insertion Sort",
            "Linear Search","Binary Search","Hash Table Lookup",
            "Dijkstra","Bellman-Ford","BFS",
            "LCS","0/1 Knapsack",
            "Standard Multiplication","Strassen"
        ],
        "Time Complexity": [
            "O(n log n) avg","O(n log n)","O(n log n)","O(n²)",
            "O(n)","O(log n)","O(1) average",
            "O((V+E) log V)","O(VE)","O(V+E)",
            "O(mn)","O(nW)",
            "O(n³)","O(n^2.807)"
        ]
    }

    st.dataframe(data, use_container_width=True, hide_index=True)


# HISTORY

elif page == "History":

    st.title("Experiment History")
    st.caption("Access previous benchmark executions.")

    st.info(
        "Your benchmark history will appear here after "
        "the result storage module is integrated."
    )


# FOOTER

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="border-top:1px solid {theme["border"]};padding-top:18px;
text-align:center;color:{theme["muted"]};font-size:11px;letter-spacing:1px">
    ALGOBENCH NEXUS · BUILT FOR PERFORMANCE ENGINEERING
</div>
""", unsafe_allow_html=True)


# Open the sidebar automatically right after the landing screen.
if st.session_state.pop("force_sidebar_expand", False):

    components.html("""
    <script>
    (() => {
        let attempts = 0;
        const maxAttempts = 50;

        // Different Streamlit versions use different test ids for the
        // "open sidebar" control, so try all of them.
        const selectors = [
            '[data-testid="stExpandSidebarButton"]',
            '[data-testid="stSidebarCollapsedControl"] button',
            '[data-testid="stSidebarCollapsedControl"]'
        ];

        function findControl(doc) {
            for (const selector of selectors) {
                const el = doc.querySelector(selector);
                if (el) return el;
            }
            return null;
        }

        function expandSidebar() {
            attempts++;
            try {
                const doc = window.parent.document;
                const control = findControl(doc);

                if (control) {
                    const button = control.tagName === "BUTTON"
                        ? control
                        : (control.querySelector("button") || control);
                    button.click();
                } else {
                    // No "open" control: stop only if the sidebar is really open.
                    const sidebar = doc.querySelector('[data-testid="stSidebar"]');
                    if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
                        return;
                    }
                }
            } catch (error) {
                // Retry while Streamlit completes the dashboard render.
            }

            if (attempts < maxAttempts) {
                window.setTimeout(expandSidebar, 400);
            }
        }

        window.setTimeout(expandSidebar, 250);
    })();
    </script>
    """, height=1)