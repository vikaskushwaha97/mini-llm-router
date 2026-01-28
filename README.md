# Mini LLM Routing Engine (CLI-Based)

A cost-aware, rule-based LLM routing engine that decides when and how an LLM request should be made to reduce token usage and overall cost.

This project was built as part of a trial-period internship task focused on LLM cost optimization, routing, and explainability, especially in RAG-style systems

# key Features

# Request Classification

Empty / Garbage

Simple

Complex

Extremely Long prompts

# Model Selection Logic

Cheap model for simple requests

Strong model for complex/long requests

Logs when and why a model was selected or changed

# In-Memory Caching

MD5-hash based prompt caching

Tracks cache hits, misses, tokens saved, and cost saved

# Daily Budget Enforcement

Prevents LLM calls when budget is exceeded

Rejects requests safely with clear logs

# Token & Cost Estimation

Heuristic token estimation

Per-request cost calculation

Remaining budget tracking

# Structured, Color-Coded Logs

Human-readable CLI logs

Optional JSON output for automation

# Edge Case Handling

Empty input

Garbage input

Extremely long prompts

Over-budget scenarios

# Project Structure
mini_llm_router/
│
├── cli.py                  # CLI entry point
│
├── mini_router/
│   ├── __init__.py
│   ├── decision.py         # Core decision engine
│   ├── model_router.py     # Model selection logic
│   ├── cache.py            # In-memory cache manager
│   ├── budget.py           # Budget tracking & enforcement
│   ├── logger.py           # Structured CLI logging
│   └── config.py           # Constants & configuration
│
└── README.md

# How It Works (High Level Flow)

User Input (CLI)
   ↓
Request Classification
   ↓
Cache Check
   ↓
Token Estimation
   ↓
Budget Validation
   ↓
Model Selection
   ↓
LLM Call / Reject / Cache Serve
   ↓
Structured Logs + Stats

# TO RUN CLONE THE REPO AND RUN python cli.py --interactive ON TERMINAL 

This project was designed with reference to academic and industry research on LLM routing and cost-aware model selection available publicly.

Key ideas such as:

request classification,

selective model invocation,

budget-aware decision making,

and caching for token-cost reduction

are inspired by concepts discussed in recent LLM routing and optimization research papers.
