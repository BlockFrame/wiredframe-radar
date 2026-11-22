#!/usr/bin/env python3
"""
Models Directory Audit & Sync Utility.

Maintains the public Models Directory (`web/data/models.json` and
`frontend/static/data/models.json`) by:
1. Pruning obsolete legacy models (2023 / early-2024 generations such as
   LLaMA 1/2, PaLM, Gemini 1.x, Gemma 1/2, Claude 1–3.5, GPT-4o, Mixtral 8x7B,
   Command Legacy, abab5/6, Grok 1/2, Qwen 2/2.5, DeepSeek V1/V2).
2. Curating current frontier and open-weight models across major labs and the
   open-weight ecosystem.
3. Synchronizing newly tracked releases from `config/model_releases.yaml` and
   `config/ecosystem_context.yaml` (which the daily pipeline auto-updates from
   AI News and OpenRouter), plus an optional live check (`--live`) against the
   OpenRouter `/api/v1/models` catalog.

Usage:
    # Check for missing or outdated models without modifying files
    python3 scripts/update_models_directory.py --check

    # Check including live OpenRouter API catalog
    python3 scripts/update_models_directory.py --check --live

    # Sync and write updated models.json to web/data and frontend/static/data
    python3 scripts/update_models_directory.py --sync
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parent.parent
WEB_MODELS_JSON = ROOT / "web" / "data" / "models.json"
STATIC_MODELS_JSON = ROOT / "frontend" / "static" / "data" / "models.json"
MODEL_RELEASES_YAML = ROOT / "config" / "model_releases.yaml"
ECOSYSTEM_CONTEXT_YAML = ROOT / "config" / "ecosystem_context.yaml"

# Legacy model names and subcategories to prune from the directory
OBSOLETE_SUBCATEGORIES = {
    "Claude (legacy 1-2.x)",
    "Claude (legacy 1–2.x)",
    "Command (Legacy)",
    "DeepSeek V1 / Legacy",
    "DeepSeek Coder",
    "DeepSeek-V2",
    "Gemini 1",
    "Gemini 2",
    "Gemma 1",
    "Gemma 2",
    "PaLM",
    "LLaMA 1",
    "Llama 2",
    "Code Llama",
    "Llama 3",
    "Llama 3.1",
    "Llama 3.2",
    "abab5",
    "abab6",
    "MiniMax M1",
    "MiniMax (Other)",
    "Mistral Base",
    "Mixtral",
    "Pixtral",
    "Moonshot v1",
    "GPT-4o",
    "Grok 1",
    "Grok 2",
    "Qwen 2",
    "Qwen 2.5",
}

OBSOLETE_MODEL_NAMES = {
    "claude 3 opus",
    "claude 3 sonnet",
    "claude 3 haiku",
    "claude 3.5 haiku",
    "claude 3.5 sonnet",
    "claude 3.5 sonnet (new)",
    "claude 3.7 sonnet",
    "claude sonnet 4",
    "claude opus 4",
    "claude opus 4.1",
    "claude mythos preview",
    "command r (03-2024)",
    "command r (08-2024)",
    "command r+ (04-2024)",
    "command r+ (08-2024)",
    "mistral medium (2023)",
    "mistral large (24.02)",
    "mistral large 2 (24.07)",
    "mistral large 2.1 (24.11)",
    "mistral small (24.09)",
    "codestral 22b (24.05)",
    "codestral mamba",
    "gpt-5",
    "gpt-5 pro",
    "gpt-5 mini",
    "gpt-5 nano",
    "gpt-5-codex",
    "gpt-5.1",
    "gpt-5.1 pro",
    "gpt-5.1 instant",
    "gpt-5.1-codex",
    "gpt-5.2",
    "gpt-5.2 pro",
    "gpt-5.2 instant",
    "gpt-5.2-codex",
}

# Authoritative curated catalog of current frontier and open-weight models
CURATED_NEW_MODELS: List[Dict[str, str]] = [
    # --- OpenAI ---
    {
        "name": "GPT-6.2 Astra",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "OpenAI's flagship frontier reasoning and multimodal model (Nov 2026), built for deep research, complex software engineering, and long-horizon autonomous tool use.",
    },
    {
        "name": "GPT-6.2 Sol",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "High-throughput frontier reasoning model in the GPT-6.2 family (Nov 2026), balancing low-latency inference with frontier coding and agentic execution.",
    },
    {
        "name": "GPT-6.1 Terra",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "Enterprise-tuned GPT-6.1 release (Oct 2026) optimized for grounded synthesis, structured outputs, and multi-step workflow orchestration.",
    },
    {
        "name": "GPT-6.1 Sol",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "General-purpose GPT-6.1 production model (Sep 2026) delivering upgraded tool-calling reliability and extended context reasoning over GPT-6 Sol.",
    },
    {
        "name": "GPT-6 Astra",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "First heavy-compute tier of the GPT-6 generation (Sep 2026), introducing unified adaptive reasoning and native multimodal tool execution.",
    },
    {
        "name": "GPT-6 Sol",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "Core GPT-6 flagship release (Sep 2026) combining fast conversational response with on-demand reasoning depth.",
    },
    {
        "name": "GPT-6 Luna",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "Compact, latency-optimized member of the GPT-6 family (Sep 2026) designed for real-time agents, decision benchmarks, and high-volume API workloads.",
    },
    {
        "name": "GPT-6 Cyber",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "Defensive cybersecurity and binary-analysis specialist in the GPT-6 lineup (Nov 2026) for vulnerability discovery, patching, and threat auditing.",
    },
    {
        "name": "Astra 6.2 & Astra (Autonomous Agent Swarm)",
        "category": "OpenAI",
        "subcategory": "GPT-6",
        "url": "https://openai.com/",
        "description": "OpenAI's autonomous multi-agent orchestration and long-horizon execution system (Aug–Nov 2026) powering coordinated agent swarms.",
    },
    {
        "name": "GPT-5.7 Sol & GPT-5.7 Terra",
        "category": "OpenAI",
        "subcategory": "GPT-5",
        "url": "https://openai.com/",
        "description": "Late-cycle GPT-5.7 production releases (Aug 2026) bridging the GPT-5.6 and GPT-6 architectures with high-reliability long-context retrieval and coding.",
    },
    {
        "name": "GPT-5.6 Sol Ultra",
        "category": "OpenAI",
        "subcategory": "GPT-5",
        "url": "https://openai.com/",
        "description": "Maximum-compute reasoning tier of the GPT-5.6 family (Jul 2026) for scientific research, theorem synthesis, and complex architecture planning.",
    },
    {
        "name": "GPT-5.6 (Base, Sol, Terra, Luna & Cyber)",
        "category": "OpenAI",
        "subcategory": "GPT-5",
        "url": "https://openai.com/",
        "description": "Full GPT-5.6 model generation (Jun–Aug 2026) introducing the Sol/Terra/Luna tiering across flagship, enterprise, compact, and cyberdefense workloads.",
    },
    {
        "name": "GPT-5.5 (Base, Instant & Cyber)",
        "category": "OpenAI",
        "subcategory": "GPT-5",
        "url": "https://openai.com/",
        "description": "Mid-2026 GPT-5.5 generation (Apr–Jun 2026) delivering lower-latency tool execution, instant chat response, and specialized cyber-auditing variants.",
    },
    {
        "name": "GPT-Live-1.1 & GPT-Live-1",
        "category": "OpenAI",
        "subcategory": "Multimodal & Specialized",
        "url": "https://openai.com/",
        "description": "Low-latency native full-duplex voice and live multimodal streaming models (Jul–Nov 2026) for real-time conversational agents.",
    },
    {
        "name": "ChatGPT Images 2.6 & 2.5",
        "category": "OpenAI",
        "subcategory": "Multimodal & Specialized",
        "url": "https://openai.com/",
        "description": "Native autoregressive image generation and editing models (Sep–Nov 2026) with high typography accuracy and multi-turn visual consistency.",
    },
    {
        "name": "GPT-Synopsys",
        "category": "OpenAI",
        "subcategory": "Multimodal & Specialized",
        "url": "https://openai.com/",
        "description": "Specialized chip-design and EDA co-pilot model (Oct 2026) developed for hardware verification, RTL synthesis, and silicon layout optimization.",
    },
    # --- Anthropic ---
    {
        "name": "Claude Fable 5.2",
        "category": "Anthropic",
        "subcategory": "Claude Fable / Mythos",
        "url": "https://www.anthropic.com/claude",
        "description": "Anthropic's frontier Mythos-class model (Nov 2026) with 1M context, always-on deep reasoning, and state-of-the-art autonomous coding and formal research performance.",
    },
    {
        "name": "Claude Mythos 5.2",
        "category": "Anthropic",
        "subcategory": "Claude Fable / Mythos",
        "url": "https://www.anthropic.com/claude",
        "description": "Partner-gated cyberdefense and critical-infrastructure edition of Fable 5.2 (Nov 2026) deployed under Project Glasswing.",
    },
    {
        "name": "Claude Fable 5.1",
        "category": "Anthropic",
        "subcategory": "Claude Fable / Mythos",
        "url": "https://www.anthropic.com/claude",
        "description": "Second-generation Mythos-class general release (Sep 2026), improving long-horizon agent stability and verification accuracy over Fable 5.",
    },
    {
        "name": "Claude Mythos 5.1",
        "category": "Anthropic",
        "subcategory": "Claude Fable / Mythos",
        "url": "https://www.anthropic.com/claude",
        "description": "Specialized cyberdefense counterpart to Claude Fable 5.1 (Sep 2026) for audited security research.",
    },
    {
        "name": "Claude Fable 5 & Claude Mythos 5",
        "category": "Anthropic",
        "subcategory": "Claude Fable / Mythos",
        "url": "https://www.anthropic.com/claude",
        "description": "First-generation Claude 5 Fable/Mythos deep-reasoning and cyberdefense models (Jun 2026), inaugurating Anthropic's ultra-compute frontier tier.",
    },
    {
        "name": "Claude Opus 5.5",
        "category": "Anthropic",
        "subcategory": "Claude Opus",
        "url": "https://www.anthropic.com/claude",
        "description": "Flagship Opus-tier model (Sep 2026) with 1M context and adaptive thinking, engineered for large-repository refactoring and complex enterprise workflows.",
    },
    {
        "name": "Claude Opus 5",
        "category": "Anthropic",
        "subcategory": "Claude Opus",
        "url": "https://www.anthropic.com/claude",
        "description": "First Claude 5 Opus release (Jul 2026) introducing next-generation adaptive thinking budgets and multi-agent software engineering.",
    },
    {
        "name": "Claude Opus 4.8",
        "category": "Anthropic",
        "subcategory": "Claude Opus",
        "url": "https://www.anthropic.com/claude",
        "description": "Final Claude 4-generation Opus release (May 2026) with upgraded long-horizon tool reliability and coding precision.",
    },
    {
        "name": "Claude Sonnet 5.5",
        "category": "Anthropic",
        "subcategory": "Claude Sonnet",
        "url": "https://www.anthropic.com/claude",
        "description": "High-efficiency frontier workhorse (Sep 2026) delivering near-Opus 5.5 coding, computer use, and agentic tool use at Sonnet latency and cost.",
    },
    {
        "name": "Claude Sonnet 5",
        "category": "Anthropic",
        "subcategory": "Claude Sonnet",
        "url": "https://www.anthropic.com/claude",
        "description": "Core Claude 5 Sonnet release (Jun 2026) advancing SWE-bench software engineering, interactive coding, and enterprise agent deployment.",
    },
    {
        "name": "Claude Haiku 5.5",
        "category": "Anthropic",
        "subcategory": "Claude Haiku",
        "url": "https://www.anthropic.com/claude",
        "description": "Fast, low-cost Claude 5.5 family model (Oct 2026) bringing hybrid reasoning, top Decision Index v2 accuracy, and sub-second latency to production pipelines.",
    },
    # --- Google ---
    {
        "name": "Gemini 4 Neon",
        "category": "Google",
        "subcategory": "Gemini 4",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "Google DeepMind's coding and agentic frontier release in the Gemini 4 series (Nov 2026), featuring 1M context and top-tier autonomous software engineering performance.",
    },
    {
        "name": "Gemini 4 Hydrogen",
        "category": "Google",
        "subcategory": "Gemini 4",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "Foundational multimodal reasoning model in the Gemini 4 family (Nov 2026) with native audio, video, code, and long-context synthesis.",
    },
    {
        "name": "Gemini 4 Carbon",
        "category": "Google",
        "subcategory": "Gemini 4",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "Enterprise and scientific reasoning model in the Gemini 4 lineup (Oct 2026), optimized for complex tool use and multi-document analysis.",
    },
    {
        "name": "Gemini 4 Argon",
        "category": "Google",
        "subcategory": "Gemini 4",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "First debut checkpoint of the Gemini 4 architecture (Sep 2026), introducing next-generation sparse MoE routing and deep thinking traces.",
    },
    {
        "name": "Gemini 3.8 Pro",
        "category": "Google",
        "subcategory": "Gemini 3",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "Mature Gemini 3.8 flagship (Sep 2026) with 2M context window and strong multimodal coding and analytical performance.",
    },
    {
        "name": "Gemini 3.8 Flash",
        "category": "Google",
        "subcategory": "Gemini 3",
        "url": "https://deepmind.google/technologies/gemini/",
        "description": "High-speed reasoning model (Sep 2026) pairing 1M+ context with low-cost thinking tokens for real-time agentic applications.",
    },
    {
        "name": "Gemini Decision 1",
        "category": "Google",
        "subcategory": "Science & Agents",
        "url": "https://deepmind.google/",
        "description": "Specialized decision-making and planning model (Nov 2026) trained for browser/OS computer-use and multi-agent coordination.",
    },
    {
        "name": "Gemini Omni 1.2 Flash",
        "category": "Google",
        "subcategory": "Science & Agents",
        "url": "https://deepmind.google/",
        "description": "Low-latency native speech-to-speech and live video interaction model (Nov 2026) for real-time multimodal assistants.",
    },
    {
        "name": "Genie 4",
        "category": "Google",
        "subcategory": "Science & Agents",
        "url": "https://deepmind.google/",
        "description": "Interactive foundation world model (Oct 2026) capable of generating playable, physics-consistent 3D environments in real time for embodied AI training.",
    },
    {
        "name": "AlphaGenome 2",
        "category": "Google",
        "subcategory": "Science & Agents",
        "url": "https://deepmind.google/",
        "description": "DeepMind's second-generation genomic regulatory foundation model (Nov 2026) predicting non-coding DNA variant effects across cell types.",
    },
    {
        "name": "AlphaProof Code",
        "category": "Google",
        "subcategory": "Science & Agents",
        "url": "https://deepmind.google/",
        "description": "Formal verification and mathematical theorem-proving model (Nov 2026) combining Lean 4 reinforcement learning with code synthesis.",
    },
    {
        "name": "EmbeddingGemma 2 (Open-Weight)",
        "category": "Google",
        "subcategory": "Gemma 4 & 3 (Open-Weight)",
        "url": "https://ai.google.dev/gemma",
        "description": "Compact open-weight multilingual retrieval and embedding model (Oct 2026) built on the Gemma 4 architecture for local RAG pipelines.",
    },
    # --- Alibaba (Qwen) [Open-Weight & Frontier] ---
    {
        "name": "Qwen4 Max",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://qwenlm.github.io/",
        "description": "Alibaba's flagship Qwen 4 frontier model (Nov 2026), advancing multilingual reasoning, agentic coding, and long-context synthesis.",
    },
    {
        "name": "Qwen3.8-2.4T-A95B (Open-Weight MoE)",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://huggingface.co/Qwen",
        "description": "Ultra-scale 2.4-trillion-parameter open-weight Mixture-of-Experts model (95B active per token, Aug 2026) matching top proprietary frontier models.",
    },
    {
        "name": "Qwen3.8-27B (Open-Weight)",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://huggingface.co/Qwen",
        "description": "Dense 27B open-weight model (Aug 2026) under Apache 2.0, delivering frontier-grade coding and math reasoning on single-workstation GPUs.",
    },
    {
        "name": "Qwen3.8 Max Prime",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://qwenlm.github.io/",
        "description": "Enhanced reasoning edition of Qwen 3.8 Max (Sep 2026) with extended test-time compute for math, code, and agent tasks.",
    },
    {
        "name": "Qwen3.8 Omni Flash",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://qwenlm.github.io/",
        "description": "End-to-end multimodal model (Sep 2026) processing text, audio, image, and video streams with real-time speech output.",
    },
    {
        "name": "Qwen3.8 Flash",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 4 & 3.8 (Open-Weight & API)",
        "url": "https://qwenlm.github.io/",
        "description": "Fast, cost-efficient hybrid-thinking model in the Qwen 3.8 series (Aug 2026) with 1M context support.",
    },
    {
        "name": "Qwen3.6-35B-A3B (Open-Weight MoE)",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 3",
        "url": "https://huggingface.co/Qwen",
        "description": "Highly efficient open-weight sparse MoE (35B total, 3B active parameters) designed for ultra-fast local inference and edge deployment.",
    },
    {
        "name": "Qwen3.6-27B (Open-Weight)",
        "category": "Alibaba (Qwen)",
        "subcategory": "Qwen 3",
        "url": "https://huggingface.co/Qwen",
        "description": "Open-weight 27B dense checkpoint in the Qwen 3.6 family with strong multilingual and tool-use benchmarks.",
    },
    # --- DeepSeek [Open-Weight] ---
    {
        "name": "DeepSeek-V4.1-Flash (1017) (Open-Weight)",
        "category": "DeepSeek",
        "subcategory": "DeepSeek-V4",
        "url": "https://github.com/deepseek-ai",
        "description": "Updated October 2026 open-weight MoE reasoning checkpoint with faster decoding, lower memory footprint, and stronger SWE-bench coding scores.",
    },
    {
        "name": "DeepSeek-V4.1-Flash (Open-Weight)",
        "category": "DeepSeek",
        "subcategory": "DeepSeek-V4",
        "url": "https://github.com/deepseek-ai",
        "description": "High-efficiency open-weight reasoning and coding model (Sep 2026) combining Multi-head Latent Attention with unified thinking traces.",
    },
    {
        "name": "DeepSeek-V4-Flash-Vision-Exp (Open-Weight)",
        "category": "DeepSeek",
        "subcategory": "DeepSeek-V4",
        "url": "https://github.com/deepseek-ai",
        "description": "Experimental open-weight multimodal vision-language reasoning model (Aug 2026) for document OCR, chart analysis, and UI grounding.",
    },
    # --- Meta [Open-Weight & Frontier] ---
    {
        "name": "Muse Spark Open (Open-Weight)",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Meta's flagship open-weight release of the Muse Spark architecture (Oct 2026), bringing native reasoning and agentic tool use to self-hosted deployments.",
    },
    {
        "name": "Muse Ember",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Compact, low-latency model in Meta's Muse family (Nov 2026) optimized for interactive assistants and fast coding workflows.",
    },
    {
        "name": "Muse Wonder & Wonder Full",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Meta's large-scale frontier multimodal reasoning models (Oct 2026) designed for deep scientific, mathematical, and software synthesis.",
    },
    {
        "name": "Muse Spark 1.3",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Third major iteration of Meta's Muse Spark reasoning model (Sep 2026) with mandatory chain-of-thought and high throughput on OpenRouter.",
    },
    {
        "name": "Muse Code",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Software engineering specialist in Meta's Muse family (Aug 2026) trained for repository-level code generation and automated debugging.",
    },
    {
        "name": "Muse Glimmer & Muse Image",
        "category": "Meta",
        "subcategory": "Muse / Experimental",
        "url": "https://ai.meta.com/",
        "description": "Meta's native visual generation and multimodal understanding models (Jul–Aug 2026) for high-fidelity image and video synthesis.",
    },
    # --- Mistral AI [Open-Weight & Frontier] ---
    {
        "name": "Mistral Large 4 'Le Chonk' (Open-Weight 1.05T MoE)",
        "category": "Mistral AI",
        "subcategory": "Mistral Large",
        "url": "https://mistral.ai/",
        "description": "Europe's 1.05-trillion-parameter open-weight frontier MoE model (Oct 2026), trained on EU Grace Blackwell clusters with top-tier multilingual and coding capability.",
    },
    {
        "name": "Devstral 2 (2512) (Open-Weight)",
        "category": "Mistral AI",
        "subcategory": "Codestral / Mathstral",
        "url": "https://mistral.ai/",
        "description": "Open-weight agentic software engineering model built for SWE-bench workflows, multi-file edits, and autonomous terminal use.",
    },
    {
        "name": "Leanstral 1.5 (Open-Weight)",
        "category": "Mistral AI",
        "subcategory": "Codestral / Mathstral",
        "url": "https://mistral.ai/",
        "description": "Open-weight formal theorem-proving and mathematical verification model (Jul 2026) specialized in Lean 4 proof synthesis.",
    },
    {
        "name": "Ministral 3 (Open-Weight)",
        "category": "Mistral AI",
        "subcategory": "Mistral Small",
        "url": "https://mistral.ai/",
        "description": "Compact open-weight edge and on-device model family delivering high instruction-following accuracy under strict memory budgets.",
    },
    {
        "name": "Voxtral 3",
        "category": "Mistral AI",
        "subcategory": "Multimodal, Speech & Safety",
        "url": "https://mistral.ai/",
        "description": "Mistral's third-generation speech understanding, translation, and real-time voice dialogue model (Oct 2026).",
    },
    {
        "name": "Shieldstral",
        "category": "Mistral AI",
        "subcategory": "Multimodal, Speech & Safety",
        "url": "https://mistral.ai/",
        "description": "Open-weight guardrail and prompt-injection defense model (Aug 2026) for real-time policy enforcement in enterprise AI pipelines.",
    },
    {
        "name": "Robostral Navigate & Mistral OCR 4",
        "category": "Mistral AI",
        "subcategory": "Multimodal, Speech & Safety",
        "url": "https://mistral.ai/",
        "description": "Mistral's specialized embodied-navigation model (Jul 2026) and fourth-generation document layout/table extraction engine (Jun 2026).",
    },
    # --- Z.ai (Zhipu / GLM) [Open-Weight & Frontier] ---
    {
        "name": "GLM-5.3 (Open-Weight & API)",
        "category": "Z.ai (Zhipu / GLM)",
        "subcategory": "GLM-5",
        "url": "https://z.ai/",
        "description": "Z.ai's flagship GLM-5.3 reasoning and agentic coding model (Oct 2026) with bilingual mastery and long-horizon tool orchestration.",
    },
    {
        "name": "GLM-5.3-FlashX & GLM-5.3-Flash",
        "category": "Z.ai (Zhipu / GLM)",
        "subcategory": "GLM-5",
        "url": "https://z.ai/",
        "description": "High-speed reasoning models (128K output capacity, Sep 2026) offering frontier-level synthesis and coding at a fraction of traditional frontier cost.",
    },
    # --- xAI (Grok) ---
    {
        "name": "Grok 4.7",
        "category": "xAI (Grok)",
        "subcategory": "Grok 4",
        "url": "https://x.ai/",
        "description": "xAI's latest Grok 4 series flagship (Sep 2026) featuring upgraded deep-thinking traces, real-time search grounding, and coding accuracy.",
    },
    {
        "name": "Grok 4.6",
        "category": "xAI (Grok)",
        "subcategory": "Grok 4",
        "url": "https://x.ai/",
        "description": "August 2026 Grok 4 release improving multimodal reasoning, tool use, and long-context coherence.",
    },
    {
        "name": "Grok Voice 3.0 & Imagine 2.0",
        "category": "xAI (Grok)",
        "subcategory": "Grok Build",
        "url": "https://x.ai/",
        "description": "xAI's low-latency native voice dialogue engine (Oct 2026) and photorealistic image/video generation suite (Aug 2026).",
    },
    # --- Moonshot AI (Kimi) [Open-Weight & Frontier] ---
    {
        "name": "Kimi K3",
        "category": "Moonshot AI (Kimi)",
        "subcategory": "Kimi K3",
        "url": "https://www.kimi.com/",
        "description": "Moonshot AI's third-generation frontier reasoning and agentic model (Aug 2026) with ultra-long context mastery and autonomous multi-step research.",
    },
    {
        "name": "Kimi K2.7 Code",
        "category": "Moonshot AI (Kimi)",
        "subcategory": "Kimi K2 (Open-Weight)",
        "url": "https://www.kimi.com/",
        "description": "Specialized software-engineering release in the Kimi K2 series (Jun 2026) tuned for repository-scale code generation, refactoring, and terminal execution.",
    },
    {
        "name": "Kimi K2.6 & Kimi K2.5 (Open-Weight MoE)",
        "category": "Moonshot AI (Kimi)",
        "subcategory": "Kimi K2 (Open-Weight)",
        "url": "https://huggingface.co/moonshotai",
        "description": "Moonshot AI's open-weight 1-trillion-parameter Mixture-of-Experts models (32B active, Jan–Apr 2026) trained with the MuonClip optimizer for agentic tool use.",
    },
    # --- MiniMax ---
    {
        "name": "MiniMax M3.1 Flash",
        "category": "MiniMax",
        "subcategory": "MiniMax M3",
        "url": "https://www.minimax.io/",
        "description": "High-speed hybrid-attention model in the MiniMax M3 generation (Oct 2026) built for long-context agent workflows and rapid synthesis.",
    },
    {
        "name": "MiniMax M3",
        "category": "MiniMax",
        "subcategory": "MiniMax M3",
        "url": "https://www.minimax.io/",
        "description": "MiniMax's flagship M3 reasoning and synthesis model (May 2026) featuring Lightning Attention for ultra-long context windows and disciplined JSON output.",
    },
    # --- Cohere ---
    {
        "name": "Command A+",
        "category": "Cohere",
        "subcategory": "Command A / Aya",
        "url": "https://cohere.com/",
        "description": "Cohere's upgraded enterprise flagship model (Sep 2026) optimized for verifiable RAG citation, multi-step tool use, and high-throughput on-prem deployment.",
    },
    {
        "name": "Cohere North Mini Code (Open-Weight / Free)",
        "category": "Cohere",
        "subcategory": "Command A / Aya",
        "url": "https://cohere.com/",
        "description": "Compact coding and workspace automation model (Jun 2026) designed for Cohere North agentic enterprise deployments.",
    },
    # --- Tencent [Open-Weight & Frontier] ---
    {
        "name": "Hunyuan Hy4",
        "category": "Tencent",
        "subcategory": "Hunyuan",
        "url": "https://hunyuan.tencent.com/",
        "description": "Tencent's fourth-generation frontier MoE foundation model (Nov 2026) with upgraded reasoning, coding, and multimodal understanding.",
    },
    {
        "name": "WeVisOne-VL (Open-Weight)",
        "category": "Tencent",
        "subcategory": "Hunyuan",
        "url": "https://huggingface.co/tencent",
        "description": "Tencent's open-weight unified vision-language model (Nov 2026) for high-resolution document, video, and GUI understanding.",
    },
    {
        "name": "Hunyuan Hy-MT2-30B-A3B & 7B (Open-Weight)",
        "category": "Tencent",
        "subcategory": "Hunyuan",
        "url": "https://huggingface.co/tencent",
        "description": "Open-weight sparse MoE (30B total / 3B active) and dense 7B/1.8B models (Aug 2026) for efficient local deployment.",
    },
    # --- NVIDIA [Open-Weight] ---
    {
        "name": "Nemotron 3.5 Super VL (Open-Weight)",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://huggingface.co/nvidia",
        "description": "NVIDIA's open-weight multimodal vision-language reasoning model (Oct 2026) for document intelligence, chart reasoning, and visual agent workflows.",
    },
    {
        "name": "NVIDIA Switchyard",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://build.nvidia.com/",
        "description": "NVIDIA's dynamic multi-model routing and orchestration model (Sep 2026) engineered for enterprise NIM inference pipelines.",
    },
    {
        "name": "Nemotron 3.5 Lightning (Open-Weight)",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://huggingface.co/nvidia",
        "description": "NVIDIA's high-throughput open-weight hybrid Mamba-Transformer model (Aug 2026) optimized for low-latency reasoning and enterprise RAG.",
    },
    {
        "name": "Nemotron 3 Ultra & Super (Open-Weight)",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://huggingface.co/nvidia",
        "description": "Open-weight frontier-scale and mid-size reasoning models trained with reinforcement learning for complex math, code, and tool calling.",
    },
    {
        "name": "Nemotron 3 Nano 30B-A3B & Nano Omni (Open-Weight)",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://huggingface.co/nvidia",
        "description": "Ultra-fast open-weight 30B-A3B MoE and multimodal omni checkpoints for edge and single-GPU inference.",
    },
    {
        "name": "Nemotron 3.5 Content Safety (Open-Weight)",
        "category": "NVIDIA",
        "subcategory": "Nemotron 3.5 & 3 (Open-Weight)",
        "url": "https://huggingface.co/nvidia",
        "description": "Open-weight safety classifier and guardrail model for detecting jailbreaks, PII leaks, and policy violations in real time.",
    },
    # --- Decision Models & Routing ---
    {
        "name": "TypeSafe Jev 1.13 (jev-1.13.0)",
        "category": "Decision Models & Routing",
        "subcategory": "Choice & Noul Decision Models",
        "url": "https://typesafe.ai/",
        "description": "TypeSafe's flagship non-generative structured decision model (SystemOne API, Sep 2026) returning calibrated Choice and Noul primitives up to 200x faster and 400x cheaper than LLM judges.",
    },
    {
        "name": "Nace AI Drex Max v1.1",
        "category": "Decision Models & Routing",
        "subcategory": "Calibrated Decision & Document Adjudication",
        "url": "https://artificialanalysis.ai/",
        "description": "#1 ranked model on the Artificial Analysis Decision Index v2 (score 73, Nov 2026), optimized for calibrated confidence scoring and multi-question document extraction.",
    },
    {
        "name": "Fastino Labs GLiDE v1.2",
        "category": "Decision Models & Routing",
        "subcategory": "Calibrated Decision & Document Adjudication",
        "url": "https://fastino.ai/",
        "description": "Co-leader on the Artificial Analysis Decision Index v2 (score 73, Nov 2026), engineered for high-symmetry, low-latency enterprise classification and fact adjudication.",
    },
    {
        "name": "Perplexity pplx-decider-27b (Decider v1.2) & Decider Flash v1.2 (Open-Weight)",
        "category": "Decision Models & Routing",
        "subcategory": "Open-Weight Decision Models",
        "url": "https://www.perplexity.ai/",
        "description": "Perplexity's state-of-the-art open-weight multimodal Decision Model and Decisions API (Oct–Nov 2026), sitting on the Decision Index v2 vs. Cost Pareto frontier.",
    },
    {
        "name": "Cloudflare Clef (27B) & Clef-Flash (9B) (Open-Weight)",
        "category": "Decision Models & Routing",
        "subcategory": "Open-Weight Decision Models",
        "url": "https://developers.cloudflare.com/workers-ai/",
        "description": "Cloudflare's open-weight decision models (Oct 2026) post-trained from Qwen3.8-27B and Qwen3.5-9B for edge request routing, guardrail evaluation, and structured triage.",
    },
    {
        "name": "Base Labs Mammoth 27B",
        "category": "Decision Models & Routing",
        "subcategory": "Calibrated Decision & Document Adjudication",
        "url": "https://artificialanalysis.ai/",
        "description": "High-accuracy 27B calibrated decision model scoring 72 on the Artificial Analysis Decision Index v2 (Nov 2026) across AA-Paperclip and AA-Symmetry benchmarks.",
    },
    {
        "name": "Celeris-1.1 Decision",
        "category": "Decision Models & Routing",
        "subcategory": "Choice & Noul Decision Models",
        "url": "https://artificialanalysis.ai/",
        "description": "Ultra-low-cost Pareto-frontier decision model ($14 per 1M tasks on the Artificial Analysis Decision Index v2, Nov 2026) built for high-volume pipeline filtering.",
    },
    {
        "name": "Baidu ERNIE-Light-DT-1.0",
        "category": "Decision Models & Routing",
        "subcategory": "Choice & Noul Decision Models",
        "url": "https://yiyan.baidu.com/",
        "description": "Baidu's lightweight Decision-Thinking model (Nov 2026) combining fast structured routing with calibrated confidence estimation.",
    },
    # --- Open-Weight Community & Labs ---
    {
        "name": "Thinking Machines Inkling 2 Mini (26.4B Looped MoE Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://thinkingmachines.ai/",
        "description": "Thinking Machines Lab's open-weight 26.4B-parameter looped Mixture-of-Experts model (Nov 2026), delivering deep recurrent reasoning while fitting on a 32GB consumer Mac.",
    },
    {
        "name": "Reflection Beam (501B MoE / 23B Active Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://reflection.ai/",
        "description": "US open-weight frontier MoE model (501B total, 23B active parameters, Oct 2026) delivering 3–4x compute efficiency and closed-frontier parity.",
    },
    {
        "name": "Marin Mochi 535B-A23B (Open-Weight MoE)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://huggingface.co/marin-community",
        "description": "Fully open-source, reproducibly trained 535B MoE (23B active, Nov 2026) released with complete training data recipes, logs, and technical report.",
    },
    {
        "name": "Nous Hermes 4 405B (Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://huggingface.co/NousResearch",
        "description": "Nous Research's flagship 405B open-weight model fine-tuned for steerable reasoning, structured function calling, and agentic workflows.",
    },
    {
        "name": "AllenAI OLMo-core 3, OLMo 2 32B & Tülu 3 405B (Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://allenai.org/",
        "description": "Ai2's fully open-weight, open-data, and open-recipe MoE/dense foundation models (Oct 2026) setting the scientific standard for transparent AI.",
    },
    {
        "name": "Microsoft Phi-4 (14B Open-Weight) & MAI-Transcribe-2",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Frontier Open-Weight MoE & Dense",
        "url": "https://huggingface.co/microsoft",
        "description": "Microsoft's compact 14B open-weight STEM/coding model and #1-ranked MAI-Transcribe-2-Streaming speech recognition model (Oct 2026).",
    },
    {
        "name": "LiquidAI LFM3-1.7B & LFM2.5-24B-A2B (Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Edge, Diffusion & Multimodal Open-Weight",
        "url": "https://www.liquid.ai/",
        "description": "LiquidAI's third-generation 1.7B edge model (Nov 2026) and 24B-A2B hybrid Liquid Foundation Model (Oct 2026) with constant memory footprint for long context.",
    },
    {
        "name": "Inception Mercury 2.5 (Diffusion LLM)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Edge, Diffusion & Multimodal Open-Weight",
        "url": "https://www.inceptionlabs.ai/",
        "description": "Parallel discrete-diffusion language model (Sep 2026) generating code and text at over 1,000 tokens/sec.",
    },
    {
        "name": "Reka Inverse Dynamics Model & Reka Edge (Open-Weight)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Edge, Diffusion & Multimodal Open-Weight",
        "url": "https://www.reka.ai/",
        "description": "Reka AI's Apache-2.0 open-weight physical robotics inverse-dynamics model (Oct 2026) and compact multimodal edge model.",
    },
    {
        "name": "ByteDance UI-TARS 7B (Open-Weight GUI Agent)",
        "category": "Open-Weight Community & Labs",
        "subcategory": "Edge, Diffusion & Multimodal Open-Weight",
        "url": "https://github.com/bytedance/UI-TARS",
        "description": "Open-weight native GUI and computer-use agent model capable of visual screen grounding and autonomous desktop/mobile action execution.",
    },
]

PROVIDER_TO_MAKER: Dict[str, Tuple[str, str, str]] = {
    "openai": ("OpenAI", "GPT-6", "https://openai.com/"),
    "anthropic": ("Anthropic", "Claude Fable / Mythos", "https://www.anthropic.com/claude"),
    "google": ("Google", "Gemini 4", "https://deepmind.google/technologies/gemini/"),
    "meta-llama": ("Meta", "Muse / Experimental", "https://ai.meta.com/"),
    "deepseek": ("DeepSeek", "DeepSeek-V4", "https://github.com/deepseek-ai"),
    "mistralai": ("Mistral AI", "Mistral Large", "https://mistral.ai/"),
    "qwen": ("Alibaba (Qwen)", "Qwen 4 & 3.8 (Open-Weight & API)", "https://qwenlm.github.io/"),
    "z-ai": ("Z.ai (Zhipu / GLM)", "GLM-5", "https://z.ai/"),
    "moonshotai": ("Moonshot AI (Kimi)", "Kimi K3", "https://www.kimi.com/"),
    "x-ai": ("xAI (Grok)", "Grok 4", "https://x.ai/"),
    "minimax": ("MiniMax", "MiniMax M3", "https://www.minimax.io/"),
    "cohere": ("Cohere", "Command A / Aya", "https://cohere.com/"),
    "tencent": ("Tencent", "Hunyuan", "https://hunyuan.tencent.com/"),
    "nvidia": ("NVIDIA", "Nemotron 3.5 & 3 (Open-Weight)", "https://huggingface.co/nvidia"),
    "reflection": ("Open-Weight Community & Labs", "Frontier Open-Weight MoE & Dense", "https://reflection.ai/"),
    "nousresearch": ("Open-Weight Community & Labs", "Frontier Open-Weight MoE & Dense", "https://huggingface.co/NousResearch"),
    "liquid": ("Open-Weight Community & Labs", "Edge, Diffusion & Multimodal Open-Weight", "https://www.liquid.ai/"),
    "inception": ("Open-Weight Community & Labs", "Edge, Diffusion & Multimodal Open-Weight", "https://www.inceptionlabs.ai/"),
}


def _normalize_key(name: str) -> str:
    cleaned = re.sub(r"\(.*?\)", "", name.lower())
    cleaned = re.sub(r"^[^:]+:\s*", "", cleaned)
    cleaned = re.sub(r"[^a-z0-9]+", "", cleaned)
    return cleaned


def load_directory_models() -> List[Dict[str, Any]]:
    if not WEB_MODELS_JSON.exists():
        return []
    return json.loads(WEB_MODELS_JSON.read_text(encoding="utf-8"))


def build_updated_catalog(existing: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int, int]:
    """Prune obsolete models and merge curated + config-tracked releases."""
    retained: List[Dict[str, Any]] = []
    pruned_count = 0

    for model in existing:
        name = str(model.get("name") or "").strip()
        subcat = str(model.get("subcategory") or "").strip()
        if not name:
            continue
        if subcat in OBSOLETE_SUBCATEGORIES or name.lower() in OBSOLETE_MODEL_NAMES:
            pruned_count += 1
            continue
        retained.append(dict(model))

    known_keys = {_normalize_key(m["name"]) for m in retained}
    for m in retained:
        # Also index sub-parts for combined names like "A & B"
        for part in re.split(r"\s+(?:&|/)\s+", m["name"]):
            if len(part.strip()) >= 4:
                known_keys.add(_normalize_key(part))

    added: List[Dict[str, Any]] = []
    for entry in CURATED_NEW_MODELS:
        key = _normalize_key(entry["name"])
        if key in known_keys:
            # Update description/subcategory if exact name exists
            for item in retained:
                if _normalize_key(item["name"]) == key:
                    item["category"] = entry["category"]
                    item["subcategory"] = entry["subcategory"]
                    item["description"] = entry["description"]
                    break
            continue
        known_keys.add(key)
        for part in re.split(r"\s+(?:&|/)\s+", entry["name"]):
            if len(part.strip()) >= 4:
                known_keys.add(_normalize_key(part))
        added.append(dict(entry))

    # Merge real 2026+ releases from config/model_releases.yaml not yet covered
    stealth_or_minor_patterns = re.compile(
        r"\b(banana|daybreak|flare|sunburst|watermelon|privacy filter|gpt-red|gpt-next|"
        r"tts|stt|transcribe|translate|whisper|live-1|flash-live|sql2|sl2t|tabfm|sensorfm|eupe|brain2qwerty)\b",
        re.I,
    )
    if MODEL_RELEASES_YAML.exists():
        releases = yaml.safe_load(MODEL_RELEASES_YAML.read_text(encoding="utf-8")) or {}
        for provider, pmodels in releases.items():
            if not isinstance(pmodels, dict) or provider not in PROVIDER_TO_MAKER:
                continue
            maker, default_subcat, default_url = PROVIDER_TO_MAKER[provider]
            for model_name, meta in pmodels.items():
                if not isinstance(meta, dict):
                    continue
                ga_date = str(meta.get("ga_date") or "")
                if not ga_date.startswith("2026-"):
                    continue
                if stealth_or_minor_patterns.search(model_name):
                    continue
                key = _normalize_key(model_name)
                if key in known_keys or any(key in k or k in key for k in known_keys if len(k) >= 6):
                    continue
                display_name = (
                    model_name.replace("-", " ")
                    if "-" in model_name and not model_name.lower().startswith(("gpt-", "glm-", "deepseek-"))
                    else model_name
                )
                subcat = default_subcat
                low = display_name.lower()
                if maker == "Google":
                    if "gemini 4" in low:
                        subcat = "Gemini 4"
                    elif "gemini 3" in low:
                        subcat = "Gemini 3"
                    elif "gemma" in low:
                        subcat = "Gemma 4 & 3 (Open-Weight)"
                    else:
                        subcat = "Science & Agents"
                elif maker == "OpenAI":
                    if "gpt-6" in low:
                        subcat = "GPT-6"
                    elif "gpt-5" in low:
                        subcat = "GPT-5"
                    else:
                        subcat = "Multimodal & Specialized"
                elif maker == "xAI (Grok)":
                    subcat = "Grok 4" if "grok 4" in low or "grok-4" in low else "Grok Build"
                known_keys.add(key)
                added.append({
                    "name": display_name,
                    "category": maker,
                    "subcategory": subcat,
                    "url": default_url,
                    "description": f"{maker} release ({ga_date}) tracked in the R[AI]DAR model release registry.",
                })

    # Place newly added models at the top of their respective Maker/Subcategory
    combined = added + retained
    return combined, pruned_count, len(added)


def check_live_openrouter(known_keys: set[str]) -> List[Tuple[str, str, str]]:
    """Optional live check against OpenRouter's public /api/v1/models endpoint."""
    url = "https://openrouter.ai/api/v1/models"
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "Wiredframe-Radar-ModelAudit/1.0"})
    try:
        with urlopen(req, timeout=20) as resp:
            payload = json.load(resp)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"WARNING: Could not query live OpenRouter catalog: {exc}", file=sys.stderr)
        return []

    untracked: List[Tuple[str, str, str]] = []
    for item in payload.get("data", []):
        model_id = str(item.get("id") or "")
        if "/" not in model_id:
            continue
        provider, slug = model_id.split("/", 1)
        if provider not in PROVIDER_TO_MAKER:
            continue
        name = str(item.get("name") or slug)
        key = _normalize_key(name)
        slug_key = _normalize_key(slug)
        if key not in known_keys and slug_key not in known_keys:
            untracked.append((provider, model_id, name))
    return untracked[:30]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and sync the R[AI]DAR Models Directory.")
    parser.add_argument("--check", action="store_true", help="Report outdated/missing models without writing files.")
    parser.add_argument("--sync", action="store_true", help="Write updated models.json to web/data and frontend/static/data.")
    parser.add_argument("--live", action="store_true", help="Also query OpenRouter /api/v1/models for newly listed models.")
    args = parser.parse_args()

    existing = load_directory_models()
    updated, pruned_count, added_count = build_updated_catalog(existing)

    print(f"Models Directory Audit:")
    print(f"  Current entries in web/data/models.json : {len(existing)}")
    print(f"  Obsolete legacy entries to prune        : {pruned_count}")
    print(f"  New frontier/open-weight entries to add : {added_count}")
    print(f"  Resulting directory size                : {len(updated)}")

    if args.live:
        known_keys = {_normalize_key(m["name"]) for m in updated}
        live_candidates = check_live_openrouter(known_keys)
        print(f"  Live OpenRouter untracked candidates    : {len(live_candidates)}")
        for provider, model_id, name in live_candidates[:15]:
            print(f"    - [{provider}] {name} ({model_id})")

    if args.sync or not args.check:
        for path in (WEB_MODELS_JSON, STATIC_MODELS_JSON):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"  Updated {path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
