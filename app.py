
import streamlit as st

from visualization.dashboard_charts import (
    show_benchmark_metrics,
    show_runtime_chart,
    show_csv_download
)

st.set_page_config(
    page_title="AlgoBench | Nexus",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080D18;
    --panel: #101A2B;
    --panel2: #131F33;
    --border: #24334A;
    --cyan: #22D3EE;
    --purple: #A78BFA;
    --text: #E8F0FC;
    --muted: #8DA1BC;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, rgba(34,211,238,.09), transparent 35%),
        radial-gradient(ellipse at 10% 20%, rgba(139,92,246,.08), transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8,13,24,.85);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0D1728,#09111F);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

h1,h2,h3,h4,p,label {
    font-family: 'Inter', sans-serif !important;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -1.5px;
}

h2,h3 {
    font-weight: 700 !important;
    letter-spacing: -.5px;
}

p, label {
    color: var(--muted);
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg,#142239,#101A2B);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
}

[data-testid="stMetricValue"] {
    color: var(--cyan);
    font-weight: 800;
}

[data-testid="stMetricDelta"] {
    font-size: 12px;
}

.ab-card {
    background: linear-gradient(145deg,rgba(19,31,51,.96),rgba(12,22,38,.96));
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 14px;
    transition: .2s ease;
}

.ab-card:hover {
    border-color: rgba(34,211,238,.55);
    transform: translateY(-2px);
}

.ab-icon {
    font-size: 25px;
    margin-bottom: 14px;
}

.ab-title {
    color: #F1F5F9;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 8px;
}

.ab-description {
    color: #91A4BE;
    font-size: 13px;
    line-height: 1.6;
}

.ab-label {
    color: var(--cyan);
    font-family: 'DM Mono',monospace;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 500;
}

.ab-hero {
    background:
        linear-gradient(110deg,rgba(19,34,57,.98),rgba(15,24,43,.88)),
        radial-gradient(circle at 90% 30%,rgba(34,211,238,.2),transparent 35%);
    border: 1px solid #2B405D;
    border-radius: 22px;
    padding: 34px;
    margin: 15px 0 28px 0;
}

.ab-hero-title {
    color: #F8FAFC;
    font-size: clamp(30px,4vw,48px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.15;
}

.ab-hero-sub {
    color: #A4B6CE;
    font-size: 14px;
    line-height: 1.8;
    max-width: 650px;
}

.ab-divider {
    height: 1px;
    background: linear-gradient(90deg,#22D3EE55,#A78BFA22,transparent);
    margin: 22px 0;
}

.ab-status {
    display: inline-block;
    padding: 6px 11px;
    background: #12352F;
    color: #5EEAD4;
    border: 1px solid #1D6254;
    border-radius: 30px;
    font-size: 11px;
    font-family: 'DM Mono',monospace;
}

.ab-mono {
    font-family: 'DM Mono',monospace;
    color: var(--cyan);
    font-size: 12px;
}

div.stButton > button {
    background: linear-gradient(100deg,#0891B2,#6366F1);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 43px;
    transition: .2s;
}

div.stButton > button:hover {
    border: 1px solid #67E8F9;
    color: white;
    box-shadow: 0 0 22px #22D3EE33;
}

div[data-baseweb="select"] > div {
    background: #111D30;
    border: 1px solid #30435E;
    border-radius: 9px;
}

.stTextInput input, .stNumberInput input {
    background: #111D30;
    color: #E8F0FC;
    border: 1px solid #30435E;
    border-radius: 9px;
}

div[role="radiogroup"] {
    gap: 8px;
}

[data-testid="stRadio"] label {
    color: #C8D5E7;
}

[data-testid="stCaptionContainer"] {
    color: #8298B4;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR

with st.sidebar:

    st.markdown("""
    <div style="padding:0 0 24px 4px">
        <div style="font-size:30px;font-weight:800;color:#F1F5F9">
            ⚡ Algo<span style="color:#22D3EE">Bench</span>
        </div>
        <div style="font-size:9px;letter-spacing:2px;color:#8298B4;margin-top:5px">
            NEXUS PERFORMANCE LAB
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div style="padding:10px 5px;color:#61748F;font-size:11px">
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
            <span style="color:#22D3EE">Optimize.</span>
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
    st.caption("Compare algorithm execution metrics and scalability.")

    st.markdown("""
    <div class="ab-card">
        <div class="ab-label">ANALYTICS MODULE</div>
        <div class="ab-title">Performance Intelligence</div>
        <div class="ab-description">
            Compare algorithms using measured benchmark results.
            Charts will populate after benchmark execution.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("No benchmark results available yet. Run an experiment first.")


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
st.markdown("""
<div style="border-top:1px solid #24334A;padding-top:18px;
text-align:center;color:#60748F;font-size:11px;letter-spacing:1px">
    ALGOBENCH NEXUS · BUILT FOR PERFORMANCE ENGINEERING
</div>
""", unsafe_allow_html=True)
