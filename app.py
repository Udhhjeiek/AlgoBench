
import streamlit as st

from visualization.dashboard_charts import (
    show_benchmark_metrics,
    show_runtime_chart,
    show_csv_download
)

st.set_page_config(
    page_title="AlgoBench | Performance Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


import base64
from pathlib import Path

FONT_PATH = Path(__file__).parent / "assets" / "NetflixSans-Regular.ttf"

if not FONT_PATH.exists():
    st.error("Netflix Sans font file not found in assets/NetflixSans-Regular.ttf")
    st.stop()

FONT_BASE64 = base64.b64encode(
    FONT_PATH.read_bytes()
).decode("utf-8")

if "bright_theme" not in st.session_state:
    st.session_state.bright_theme = True


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
        "button_glow": "rgba(104, 118, 75, .20)"
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
        "button_glow": "rgba(190, 198, 202, .16)"
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
html, body, [class*="css"], .stApp, h1, h2, h3, h4, p, label, span, div, button, input {
    font-family: "Netflix Sans", Arial, sans-serif !important;
}
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
.ab-icon { font-size: 25px; margin-bottom: 14px; }
.ab-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 650;
    margin-bottom: 8px;
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
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 78% 22%, __HERO_GLOW__, transparent 33%),
        linear-gradient(120deg, var(--panel-raised), var(--panel));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 42px;
    margin: 15px 0 28px 0;
    box-shadow: var(--shadow);
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
footer, #MainMenu { visibility: hidden; }
</style>
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
    "__BUTTON_GLOW__": theme["button_glow"]
}
for key, value in values.items():
    css = css.replace(key, value)

st.markdown(f"""<style>{css}</style>""", unsafe_allow_html=True)



# SIDEBAR

with st.sidebar:

    st.markdown(f"""
    <div style="padding:0 0 24px 4px">
        <div style="font-size:30px;font-weight:800;color:{theme["text"]}">
            ⚡ Algo<span style="color:{theme["text"]}">Bench</span>
        </div>
        <div style="font-size:9px;letter-spacing:2px;color:{theme["muted"]};margin-top:5px">
            NEXUS PERFORMANCE LAB
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ab-divider"></div>', unsafe_allow_html=True)

    st.toggle("Bright theme", key="bright_theme")

    st.markdown('<div class="ab-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="ab-label">WORKSPACE</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Run Benchmark",
            "Compare Results",
            "Profiler",
            "Algorithm Library",
            "History"
        ],
        label_visibility="collapsed"
    )

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


# TOP BAR

left, right = st.columns([5, 1])

with left:
    st.markdown(
        '<div class="ab-label">ALGORITHM INTELLIGENCE / PERFORMANCE ANALYTICS</div>',
        unsafe_allow_html=True
    )

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

    st.markdown("### Platform Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Algorithm Categories","05")
    c2.metric("Algorithm Implementations","15+")
    c3.metric("Analysis Tools","03")
    c4.metric("Benchmark Engine","Pending")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Explore Algorithm Domains")
    st.caption("Select a domain to configure and analyze its algorithms.")

    categories = [
        ("01","↕️","Sorting","Quick, Merge, Heap and Insertion Sort",
         "O(n log n)"),
        ("02","⌕","Searching","Linear, Binary and Hash Table Lookup",
         "O(log n)"),
        ("03","◈","Graph Algorithms","Dijkstra, Bellman-Ford and BFS",
         "O(V + E)"),
        ("04","▦","Dynamic Programming","LCS and 0/1 Knapsack",
         "DP"),
        ("05","▧","Matrix Algorithms","Standard and Strassen Multiplication",
         "O(n³)")
    ]

    cols = st.columns(3)

    for i, (number,icon,title,desc,complexity) in enumerate(categories):

        with cols[i % 3]:
            st.markdown(f"""
            <div class="ab-card">
                <div class="ab-label">DOMAIN {number}</div>
                <div class="ab-icon">{icon}</div>
                <div class="ab-title">{title}</div>
                <div class="ab-description">{desc}</div>
                <br>
                <div class="ab-mono">{complexity}</div>
            </div>
            """, unsafe_allow_html=True)

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
        "⚡ Prepare Benchmark Configuration",
        use_container_width=True
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
