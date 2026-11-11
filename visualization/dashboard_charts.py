"""Streamlit visualizations for AlgoBench benchmark results."""
from __future__ import annotations

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from benchmarking.benchmark_engine import CSV_FIELDS


def _results_frame(results):
    if not results:
        return pd.DataFrame()
    df = pd.DataFrame(results)
    # Keep dashboard tables focused on comparable, serializable measurements.
    return df


def show_benchmark_metrics(results):
    """Show summary metrics and the structured measurement table."""
    df = _results_frame(results)
    if df.empty:
        st.info("No benchmark results available.")
        return

    if "average_time" not in df.columns:
        st.error("Benchmark results are missing the 'average_time' field.")
        return

    run_count = len(df)
    if "trial_count" in df.columns:
        total_trials = int(pd.to_numeric(df["trial_count"], errors="coerce").fillna(0).sum())
    elif "trials" in df.columns:
        total_trials = int(pd.to_numeric(df["trials"], errors="coerce").fillna(0).sum())
    else:
        total_trials = "N/A"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Benchmark Runs", run_count)
    col2.metric("Total Timed Trials", total_trials)
    col3.metric("Mean Runtime", f"{pd.to_numeric(df['average_time']).mean():.6f} s")

    if "memory_measurement" in df.columns:
        memory = pd.to_numeric(df["memory_measurement"], errors="coerce").dropna()
        col4.metric("Mean Peak Memory", f"{memory.mean():.2f} KiB" if not memory.empty else "N/A")
    else:
        col4.metric("Mean Peak Memory", "N/A")

    display_cols = [c for c in CSV_FIELDS if c in df.columns]
    if display_cols:
        st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


def show_runtime_chart(results):
    """Use a scaling line chart for multiple sizes, otherwise a bar comparison."""
    df = _results_frame(results)
    required = {"algorithm", "average_time"}
    if df.empty:
        st.info("Run a benchmark to generate performance charts.")
        return
    if not required.issubset(df.columns):
        st.warning("Runtime chart requires 'algorithm' and 'average_time' fields.")
        return

    df["average_time"] = pd.to_numeric(df["average_time"], errors="coerce")
    df = df.dropna(subset=["average_time"])
    if df.empty:
        st.info("No valid runtime measurements are available.")
        return

    st.subheader("Runtime Comparison")
    fig, ax = plt.subplots(figsize=(9, 4.8))

    has_multiple_sizes = "input_size" in df.columns and df["input_size"].nunique() > 1
    if has_multiple_sizes:
        df["input_size"] = pd.to_numeric(df["input_size"], errors="coerce")
        for algorithm, group in df.groupby("algorithm"):
            group = group.sort_values("input_size")
            ax.plot(
                group["input_size"],
                group["average_time"],
                marker="o",
                linewidth=2,
                label=algorithm,
            )
        ax.set_xlabel("Input size")
        ax.set_ylabel("Average runtime (seconds)")
        ax.set_title("Runtime Scaling by Input Size")
        ax.legend()
        ax.grid(True, alpha=0.25)
    else:
        labels = df["algorithm"].astype(str)
        ax.bar(labels, df["average_time"])
        ax.set_title("Average Runtime by Algorithm")
        ax.set_ylabel("Average runtime (seconds)")
        ax.set_xlabel("Algorithm")
        ax.tick_params(axis="x", labelrotation=18)
        ax.grid(axis="y", alpha=0.25)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def show_csv_download(results):
    """Download only the agreed benchmark schema, excluding transient profile data."""
    if not results:
        return

    df = pd.DataFrame(results)
    columns = [column for column in CSV_FIELDS if column in df.columns]
    if columns:
        df = df[columns]

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="algobench_results.csv",
        mime="text/csv",
    )
