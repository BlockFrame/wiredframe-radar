# AI Digest — 2026-11-27

## Executive Summary
#### Executive Briefing
- **Nvidia** has instructed manufacturing partners to pause server [shipments to](/?date=2026-11-27&category=news#item-88bbfb00194a) Malaysia, Singapore, Thailand, and Indonesia as tightened US export controls aim to keep AI chips out of China. The pause is a material setback for Southeast Asia's data-center buildout and a sharp escalation in chip geopolitics.
- **Microsoft** published details on ARTEX, an AI framework that state-backed hackers have used since July 2026 [to automate cyberattacks](/?date=2026-11-27&category=news#item-ab5ddf0b7ed2) through specialized agents with minimal human oversight, attributed to groups in China and North Korea plus criminal organizations. It is concrete evidence that offensive AI cyber capabilities are operational today, not theoretical.
- **Compute, data, and usage limits became battlegrounds**: OpenAI and Anthropic restricted data access, reportedly pushing Z.AI and Moonshot AI to delay flagship launches and turn [to Google and Meta](/?date=2026-11-27&category=news#item-35150db404c8) for training data, while OpenAI cut GPT-6.2 allowances days after launch — Astra users now hit [limits 40](/?date=2026-11-27&category=news#item-b7ac755e2890)% faster and Sol users 25% faster.
- **AI mathematics hit the mainstream**: former OpenAI researcher Scott Aaronson argued the recent AI-assisted Riemann proof matters less for its result than for [the fact that an AI system](/?date=2026-11-27&category=news#item-89fce0273ad2) could produce it, warning labs may hold unpublished cryptographic advances. Separately, a researcher described [months of Astra-assisted work with a mathematics professor on long-standing open problems](/?date=2026-11-27&category=social#item-e4b84d466755).

#### Safety & Regulation
- **England and Wales courts**: an investigation found at least 25 cases in 2026 were [affected by undisclosed AI use](/?date=2026-11-27&category=news#item-a2b781a0780b), including AI-generated witness statements, fabricated case law, and nonexistent statutes, prompting judicial complaints — quantified evidence that undisclosed AI is already straining legal safeguards.
- **OpenAI** confirmed that Private Inference, a confidential-computing capability keeping [prompts and responses](/?date=2026-11-27&category=social#item-ecdab81b4811) under strict control even during model processing, is now in testing. It targets the confidentiality concerns that keep banks, health systems, and other regulated industries off frontier APIs.

#### Research Highlights
- **DexEngine** is a simulation pipeline that converts everyday human hand-object video [into physically executable whole-robot](/?date=2026-11-27&category=research#item-58ae6b113fef) arm-hand trajectories using reachability-aware placement, motion retargeting, and residual RL correction, producing roughly 65,000 trajectories and 325,000 episodes across nine datasets. It attacks dexterous manipulation's central data bottleneck, promising far cheaper training of capable robot policies.
- **NOPO ([Negative-Only Policy Optimization](/?date=2026-11-27&category=research#item-d4361145e47d))** formalizes one-sided verifiable rewards — where confirmed negatives are trustworthy but "positives" are merely non-falsified — and trains policies only by suppressing trusted negatives. This matches realistic verifiers in code, math, and agent settings, cutting reward-hacking risk where positive verification is unreliable.
- **"[Speak When You See It](/?date=2026-11-27&category=research#item-2fce1ed16bca)"** shows two proactive-assistant benchmarks can be dominated by a video-blind timer policy that ignores video content entirely, formalizing a "video-blind frontier" and proposing an evidence-based decision framework instead. The lesson is that flawed benchmarks can silently reward shortcuts and misdirect assistant research.

#### Trending Repositories
- **[cathrynlavery/diagram-design](/?date=2026-11-27&category=github_trending#item-1cbbd89c355a)** (731 stars today) generates editorial-quality diagrams across 52 types as self-contained HTML and SVG, working inside Claude Code, Codex, Copilot, Cursor, and other coding agents. Developers are adopting it to fix the chronically weak visual output of coding assistants.
- **[zhouxiaoka/autoclip](/?date=2026-11-27&category=github_trending#item-6e8f56a7cafa)** (733 stars today) is a local-first, open-source alternative to OpusClip that turns one link into a finished clip with zero subscriptions, including an MCP server for agent workflows — part of rising demand for subscription-free, locally run AI media tools.
- **[HKUDS/CLI-Anything](/?date=2026-11-27&category=github_trending#item-02fa09d11035)** (668 stars today) aims to make all software agent-native so coding agents can operate everyday command-line tools directly, extending today's clear pattern of developers rewarding agent-infrastructure projects that remove concrete workflow bottlenecks.

#### Signals to Watch
- **The open-source-versus-proprietary fight escalated**: Yann LeCun accused proprietary labs like OpenAI and Anthropic of being "[black holes](/?date=2026-11-27&category=social#item-afe4276bf491)" that absorb open research without contributing back, while Timnit Gebru called anti-open-source criticism corporate propaganda protecting a few [US companies](/?date=2026-11-27&category=social#item-9acbf058f5cd) — a clash that will shape coming policy battles over open weights.
- **Verifiability remains contested**: OpenAI's Jason Wei argued [verifiability is a](/?date=2026-11-27&category=social#item-83d1841b700b) spectrum, claiming even "non-verifiable" tasks can be judged by experts or market signals, just as papers like NOPO and the video-blind benchmark study push the field toward stricter, more honest evaluation.
- **Agents are spreading into go-to-market work**: [Clay](/?date=2026-11-27&category=news#item-99e4aaef9af6), a GTM automation platform that raised $115M at a $7.1B valuation in September, reports roughly half of its usage now runs through external harnesses like Claude Code, signaling agent workflows are moving beyond coding into sales and revenue operations.

## 🔬 Research Papers
1. **[DexEngine: Scaling Human Demonstrations into Physically Executable Whole-Robot Data](https://huggingface.co/papers/2611.33579)** — neutral
   DexEngine is a simulation pipeline that converts human hand-object video into physically executable arm-hand robot trajectories via reachability-aware placement, arm motion retargeting, and residual RL correction, yielding ~5,200 clips per hand across 65,000 trajectories and 325,000 episodes from nine datasets.
2. **[Negative-Only Policy Optimization for One-Sided Verifiable Rewards](https://huggingface.co/papers/2611.17287)** — neutral
   NOPO formalizes one-sided verifiability (verified negatives reliable, verified positives only non-falsified) and proposes Negative-Only Policy Optimization that updates policies only by suppressing trusted negatives, avoiding reward-hacking from uncertain positives.
3. **[Speak When You See It: Proactive Task Assistants Should Wait for Evidence, Not the Clock](https://huggingface.co/papers/2611.30895)** — neutral
   The paper shows that two proactive-assistant benchmarks can be dominated by a video-blind timer policy, formalizing this as a 'video-blind frontier' and proposing an Evidence-based decision formulation to push beyond it.
4. **[AIChipBench: Benchmarking LLM Agents for Automated AI Accelerator Design](https://huggingface.co/papers/2611.33093)** — neutral
   AIChipBench evaluates LLM coding agents on implementing synthesizable RTL decoders for quantized Qwen3.5, Gemma 3, Gemma 4, and Llama 3.2 against an executable integer reference, with held-out sequences, resets, stalls, and a synthesis-aware optimization track across 9,136+ runs.
5. **[EgoUseBench: Benchmarking Computer-Use Agents under Evolving First-Person Contexts](https://huggingface.co/papers/2611.34466)** — neutral
   Integral converts a pretrained vision-language model into a unified multimodal model by constructing a shared visual representation space, preserving understanding capability while enabling strong visual generation. It avoids the typical trade-off between comprehension and synthesis.
6. **[Evaluation-Free Recursive Self-Improvement for Coding Agents](https://huggingface.co/papers/2611.21056)** — positive
   ELITE enables coding agents to self-improve without downstream evaluations by independently exploring complementary implementations and integrating them via an Explore-then-Integrate scheme, achieving strong SWE-bench results and transfer.
7. **[DocSEAM: Bidirectional Cross-Page Encoding for Multi-Page Document Understanding](https://huggingface.co/papers/2611.34420)** — neutral
   Entangle is an in-context world-action model that maps a single human video and current robot observations to future states and actions. It addresses temporal alignment and shortcut reliance in human-video ICL for robotics via video-to-video alignment and explicit context tracking.
8. **[PyRUA-Dex: Learning Programmatic Policies for Dexterous Bimanual Manipulation with Coding Agents](https://huggingface.co/papers/2611.33144)** — positive
   Argues for model-driven context management via a context API, showing improvements in accuracy and token efficiency over harness-triggered compaction. Reusing KV caches after edits reduces prefill compute, pointing toward a shift in how long-context agents are designed.
9. **[Mixture-of-Loops Transformer](https://huggingface.co/papers/2611.34923)** — neutral
   Proposes a Mixture-of-Loops Transformer that reuses KV memory across loops and depths, with a U-shaped variant improving pretraining efficiency and inference latency. The approach targets parameter efficiency without sacrificing representational capacity.
10. **[SEEK: Self-Evolution through Execution Knowledge for Agentic Robot Manipulation](https://huggingface.co/papers/2611.33915)** — positive
   TT-RSI is a label-free test-time framework that improves LLMs by repeatedly re-solving questions with prior solutions and distilling refinements into model weights. It outperforms self-consistency methods under matched test-time scaling budgets.

## 📰 Industry News
1. **[Nvidia hits pause on chip shipments to Southeast Asia](https://techcrunch.com/2026/11/26/nvidia-hits-pause-on-chip-shipments-to-southeast-asia/)** — neutral — *via AI News & Artificial Intelligence | TechCrunch*
   Nvidia has instructed manufacturing partners to pause server shipments to Malaysia, Singapore, Thailand, and Indonesia as the US tightens export controls aimed at keeping AI chips out of China.
2. **[Microsoft details how state-backed hackers use the ARTEX AI framework to automate cyberattacks](https://the-decoder.com/microsoft-details-how-state-backed-hackers-use-the-artex-ai-framework-to-automate-cyberattacks/)** — neutral — *via The Decoder*
   Microsoft published details on ARTEX, an AI framework in active use since July 2026 that automates cyberattacks via specialized agents with minimal human oversight, attributing usage to state-backed groups in China and North Korea plus criminal organizations.
3. **[After OpenAI and Anthropic shut the door on their data, a Chinese AI developer is turning to Google and Meta instead](https://the-decoder.com/after-openai-and-anthropic-shut-the-door-on-their-data-a-chinese-ai-developer-is-turning-to-google-and-meta-instead/)** — positive — *via The Decoder*
   Chinese AI labs Z.AI and Moonshot AI are reportedly delaying flagship model launches because OpenAI and Anthropic have restricted access to their data, forcing a pivot to Google and Meta as alternative training data sources.
4. **[OpenAI cuts GPT-6.2 usage: Astra hits limits 40% faster, Sol 25% faster](https://twitter.com/thsottiaux/status/2125784147889393806)** — neutral — *via hackernews*
   OpenAI has reduced usage allowances for GPT-6.2 models: Astra hits its limits 40% faster and Sol hits limits 25% faster than before. This signals tightening rate limits on OpenAI's newest flagship-tier models.
5. **[Dozens of court cases in England and Wales affected by undisclosed AI use in 2026](https://www.theguardian.com/technology/2026/nov/26/dozens-of-court-cases-in-england-and-wales-affected-by-undisclosed-ai-use-in-2026)** — neutral — *via AI (artificial intelligence) | The Guardian*
   An investigation found at least 25 court cases in England and Wales were affected in 2026 by undisclosed AI use, including AI-generated witness statements, fabricated case law, and nonexistent statutes, prompting judicial complaints.
6. **[Former OpenAI researcher says the Riemann proof matters less than the fact that an AI system can produce it](https://the-decoder.com/former-openai-researcher-says-the-riemann-proof-matters-less-than-the-fact-that-an-ai-system-can-produce-it/)** — concerned — *via The Decoder*
   First spotted on [Social](/?date=2026-11-26&category=social#item-d20461f44f8b), now making mainstream headlines, Former OpenAI researcher Scott Aaronson argues AI's recent mathematics breakthroughs matter far beyond academia, warning labs likely possess unpublished cryptographic advances and that capabilities may reshape the global economy or threaten life on Earth.
7. **[Grand Theft Auto VI proves why efficiency isn’t a virtue](https://techcrunch.com/2026/11/26/as-anthropic-ipos-grand-theft-auto-vi-proves-why-efficiency-isnt-a-virtue/)** — positive — *via AI News & Artificial Intelligence | TechCrunch*
   TechCrunch commentary argues that on the day of Anthropic's public market debut, the meticulously human-made Grand Theft Auto VI became one of the most successful entertainment launches ever, suggesting efficiency is not the only virtue in tech.
8. **[How Clay Builds GTM Agents — Jeff Barg, Head of AI](https://latent.space/p/how-clay-builds-gtm-agents-jeff-barg-head-of-ai/)** — neutral — *via Latent Space*
   Clay, a GTM automation platform, raised $115M at a $7.1B valuation in September and reports roughly 50/50 usage between its own agent and external harnesses like Claude Code, with co-founder Jeff Barg discussing agent infrastructure design.
9. **[Google Will Make AI Agents Use Its MCP Servers. The Gmail One Can't Send Email](https://techstackups.com/articles/google-workspace-ai-agents-mcp/)** — neutral — *via hackernews*
   Google is pushing AI agents to use its MCP (Model Context Protocol) servers, but the Gmail MCP server reportedly cannot send email. The piece highlights both the strategic move toward agent infrastructure and early-stage reliability issues.
10. **[Your future housekeeper might be an XPeng](https://robotnews.therundown.ai/p/your-future-housekeeper-might-be-an-xpeng)** — neutral — *via robotnews.therundown.ai*
   XPeng unveiled an upgraded IRON humanoid robot that could greet car buyers in early 2027 and target household chores a year or two later, intensifying competition with Tesla, Figure AI, and other Chinese robotics firms.

## 📦 Trending Repos
1. _No items_

## 🐦 Social Signals
1. **[Open research and open source accelerate progress.

The proprietary AI shops are black holes that su...](https://twitter.com/ylecun/status/2126099761803760093)** — neutral
   Yann LeCun criticizes proprietary AI labs, especially Anthropic and OpenAI, for absorbing open-source techniques without contributing back, framing them metaphorically as black holes.
2. **[Great work from J! Using phantom transfer as a proxy task for "models inheriting subtle traits via d...](https://twitter.com/NeelNanda5/status/2125962350113272171)** — neutral
   Neel Nanda highlights research using phantom transfer as a proxy task to study data attribution techniques for models inheriting subtle traits via distillation.
3. **[great essay, i like the point that verifiability is a spectrum. makes sense that the "non-verifiable...](https://twitter.com/_jasonwei/status/2125982637378650303)** — neutral
   Jason Wei of OpenAI comments on verifiability being a spectrum, arguing even 'non-verifiable' tasks can be evaluated by experts or through market signals like willingness to pay.
4. **[OCRia-nano-1 is an insane model.

It's just 8.1M parameters (!!) and can parse scanned text, tables,...](https://twitter.com/jerryjliu0/status/2126008009759580616)** — neutral
   LlamaIndex founder highlights OCRia-nano-1, an 8.1M parameter OCR model that handles scanned text, tables, multiple languages, and bounding boxes, pitched for RAG document ingestion
5. **[Imagine a robot walking in a museum and mapping everything it sees.

The robot uses every camera fra...](https://twitter.com/svpino/status/2126011138554880148)** — neutral
   Technical breakdown of LingBot-Map 2.0 from Robbyant, a model that performs online camera-pose estimation and 3D scene reconstruction from video with a new Refine mechanism that reduces accumulated drift without an external optimizer.
6. **[Private Inference — confidential computing, with strict controls over prompts and responses while th...](https://twitter.com/gdb/status/2125824585027272727)** — neutral
   Continuing our coverage from [yesterday](/?date=2026-11-26&category=social#item-8d22748b5bba), Greg Brockman (gdb) announces that Private Inference — confidential computing with strict controls over prompts and responses during model processing — is now in testing at OpenAI.
7. **[@mahdyyon Also propaganda against open source AKA competition for the handful of US companies positi...](https://twitter.com/timnitGebru/status/2126084815791513607)** — concerned
   Timnit Gebru argues that criticism of open-source AI amounts to industry propaganda designed to protect a few US companies seeking government bailouts and bans on open-weight models.
8. **[I’ve spent a better part of the past 2-3 months collaborating with an old friend of mine who is a ma...](https://twitter.com/tunguz/status/2125926349592277014)** — positive
   AI researcher describes a multi-month collaboration with a math professor using Astra to solve long-standing open problems in mathematics, with public release planned on GitHub
9. **[A new issue of my weekly AI newsletter is out.

2026 in LLMs (so far)

[Open Source] Add runtime con...](https://twitter.com/burkov/status/2126082443073507638)** — neutral
   Andriy Burkov promotes his weekly AI newsletter covering NVIDIA OpenShell, Apple RAG retrieval, weight-space programming, AI agent scaling on chips, imbalanced logistic regression, and Google Gemini RL customization best practices.
10. **[Perplexity Teammates adoption is on an exponential rise. Doubling every ten days. This is just exter...](https://twitter.com/AravSrinivas/status/2126038741622104256)** — positive
   Arav Srinivas (Perplexity CEO) announces that Perplexity Teammates adoption among external Max ($200/mo) users is doubling roughly every ten days, with a growth chart attached.

---
_325 items • 2026-11-27_
