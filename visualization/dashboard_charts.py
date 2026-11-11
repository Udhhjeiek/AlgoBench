
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def show_benchmark_metrics(results):

    if not results:
        st.info("No benchmark results available.")
        return

    df = pd.DataFrame(results)

    if "average_time" not in df.columns:
        st.error("Benchmark results are missing average_time.")
        return

    if df.empty:
        st.info("No benchmark results available.")
        return

    st.subheader("Benchmark Performance")

    cols = st.columns(3)

    cols[0].metric(
        "Algorithms Tested",
        len(df)
    )

    cols[1].metric(
        "Total Experiments",
        int(df["trials"].sum())
        if "trials" in df.columns else "N/A"
    )

    cols[2].metric(
        "Average Runtime",
        f"{df['average_time'].mean():.6f} s"
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def show_runtime_chart(results):

    if not results:
        st.info("Run a benchmark to generate performance charts.")
        return

    df = pd.DataFrame(results)

    required = {"algorithm", "average_time"}

    if not required.issubset(df.columns):
        st.warning("Runtime chart requires algorithm and average_time.")
        return

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.bar(
        df["algorithm"],
        df["average_time"]
    )

    ax.set_title("Algorithm Runtime Comparison")
    ax.set_ylabel("Average Runtime (seconds)")
    ax.set_xlabel("Algorithm")

    plt.xticks(rotation=20)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


def show_csv_download(results):

    if not results:
        return

    df = pd.DataFrame(results)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="algobench_results.csv",
        mime="text/csv"
    )
