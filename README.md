# Consensus Gap

**Expert vs Public Belief Tracker** — built on [TrueForge](https://github.com/truefoundry/trueforge) for the Agent Harness Hackathon.

## What it does

Consensus Gap is an agent that takes any topic and shows you two things side by side, with evidence:

- **What experts actually say** — pulled from academic, institutional, and scientific sources
- **What the public actually believes** — pulled from forums, social sentiment, and survey data

It then scores the gap between the two and generates a comparison report — but never publishes anything without your explicit approval.

## Why

There's no simple tool that systematically shows "what experts say vs. what people believe" side by side, with sources. Nutrition myths, economic beliefs, health practices — this space is largely empty. Consensus Gap fills it.

## How it works

1. **You give it a topic** (e.g. "Does sugar cause hyperactivity in kids?")
2. **Two subagents run in parallel**:
   - `expert-researcher` — searches academic and institutional sources for the expert consensus
   - `public-belief-researcher` — searches forums, social platforms, and survey data for public sentiment
3. **Sandbox execution** — a Python script (run in a Daytona sandbox) scores the agreement gap and generates a comparison chart
4. **Human approval gate** — before anything is saved or published, the agent stops and asks for explicit approval. Nothing is written or committed without a yes.

This uses TrueForge's core harness capabilities: MCP-connected web search, dynamic sub-agents for parallel research, sandboxed code execution, and a human-in-the-loop approval step before any irreversible action.

## Setup

**Requirements:** Node.js 22+

```bash
npx @truefoundry/trueforge
```

Open `http://localhost:8790`.

1. **Settings → Models** — add a model provider and API key
2. **Settings → Connectors** — connect a web search tool (e.g. `exa`)
3. **Settings → Sandbox providers** — connect Daytona with your API key
4. Compose the agent: enable **Dynamic sub-agents** and the sandbox capability, then save with the instructions below

### Agent instructions

```
You are Consensus Gap, an agent that researches a topic and compares expert
consensus vs public belief. When given a topic: spawn two subagents — one
searches academic/institutional/expert sources, one searches forums/social/
survey data for public sentiment. Collect 3-5 sourced claims from each. Then
use the sandbox to run a Python script that scores the agreement gap and
generates a comparison chart. Draft a short report. Before saving/publishing
the report, STOP and ask the user for explicit approval — do not write any
file or make any commit without approval.
```

## Usage

Once the agent is saved, start a new session and give it a topic:

```
Does sugar cause hyperactivity in children?
```

The agent will research both sides, generate a gap score and chart, and pause for your approval before writing anything.

## Qodo Code Review Evidence

_Link to a reviewed, merged PR goes here._

## Team

Built by Team [name] for the [Agent Harness Hackathon](https://www.wemakedevs.org/hackathons/trueforge) by WeMakeDevs, TrueFoundry, and Qodo.
