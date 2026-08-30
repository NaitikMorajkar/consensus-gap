"""
gap_score.py

Runs inside the Daytona sandbox. Takes the expert-consensus claims and the
public-belief claims collected by the two research subagents, scores the
agreement gap, and generates a comparison chart.

Expected input: a JSON object with two lists of claims, each claim scored
0-100 for how strongly it supports the position being asked about.

Usage (the agent fills this in with real findings before running):
    python gap_score.py
"""

import json
import matplotlib
matplotlib.use("Agg")  # no display in the sandbox
import matplotlib.pyplot as plt


def compute_gap(expert_claims, public_claims):
    """
    expert_claims / public_claims: list of dicts like
        {"claim": str, "source": str, "agreement_score": int}  # 0-100

    Returns a summary dict with each side's average agreement and the gap.
    """
    expert_avg = sum(c["agreement_score"] for c in expert_claims) / len(expert_claims)
    public_avg = sum(c["agreement_score"] for c in public_claims) / len(public_claims)
    gap = round(abs(expert_avg - public_avg), 1)

    return {
        "expert_agreement": round(expert_avg, 1),
        "public_agreement": round(public_avg, 1),
        "gap_points": gap,
        "direction": "public overestimates" if public_avg > expert_avg else "public underestimates",
    }


def make_chart(summary, topic, out_path="gap_chart.png"):
    labels = ["Expert Consensus", "Public Belief"]
    values = [summary["expert_agreement"], summary["public_agreement"]]
    colors = ["#2f5d50", "#a3572e"]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=colors, width=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 2, f"{val}%",
                 ha="center", fontsize=11, fontweight="bold")

    ax.set_ylim(0, 100)
    ax.set_ylabel("Agreement with claim (%)")
    ax.set_title(f"Consensus Gap: {topic}\nGap = {summary['gap_points']} points", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def build_report(topic, expert_claims, public_claims, summary, chart_path):
    lines = [
        f"# Consensus Gap Report: {topic}\n",
        f"**Expert agreement:** {summary['expert_agreement']}%",
        f"**Public agreement:** {summary['public_agreement']}%",
        f"**Gap:** {summary['gap_points']} points ({summary['direction']})\n",
        f"![gap chart]({chart_path})\n",
        "## Expert Consensus\n",
    ]
    for c in expert_claims:
        lines.append(f"- {c['claim']} — *{c['source']}*")

    lines.append("\n## Public Belief\n")
    for c in public_claims:
        lines.append(f"- {c['claim']} — *{c['source']}*")

    return "\n".join(lines)


if __name__ == "__main__":
    # The agent replaces this block with the real findings from the two
    # subagents before executing the script in the sandbox.
    topic = "Does sugar cause hyperactivity in children?"

    expert_claims = [
        {"claim": "No controlled trial has shown a reliable causal link between sugar and hyperactivity.",
         "source": "meta-analysis, J. Pediatrics", "agreement_score": 10},
        {"claim": "Reported effects are largely attributed to observer expectation bias.",
         "source": "NIH review, 2019", "agreement_score": 15},
        {"claim": "Any diet-behavior link is small and confounded by other factors.",
         "source": "AAP clinical guidance", "agreement_score": 12},
    ]

    public_claims = [
        {"claim": "\"Sugar rush\" is treated as common-sense fact by most parents.",
         "source": "parenting forum survey, n=1240", "agreement_score": 82},
        {"claim": "Party/school anecdotes are cited as first-hand confirmation.",
         "source": "social sentiment sample", "agreement_score": 78},
        {"claim": "Belief holds steady across regions and education levels.",
         "source": "YouGov panel", "agreement_score": 77},
    ]

    summary = compute_gap(expert_claims, public_claims)
    chart_path = make_chart(summary, topic)
    report = build_report(topic, expert_claims, public_claims, summary, chart_path)

    print(json.dumps(summary, indent=2))
    print("\n--- DRAFT REPORT (not saved — awaiting approval) ---\n")
    print(report)
