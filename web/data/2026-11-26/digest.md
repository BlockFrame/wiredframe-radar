# AI Digest — 2026-11-26

## Executive Summary
#### Executive Briefing
- **[Google DeepMind](/?date=2026-11-26&category=news#item-ff642c9cf9a9)**: [Gemini 4 Neon](/?date=2026-11-26&category=social#item-9519bb05721c), generally available since November 18, is showing breakout traction. Perplexity CEO Arav Srinivas reported **[44.52 billion tokens](/?date=2026-11-26&category=social#item-d49f31735cf4)** consumed in a single day, **23.5%** above the prior full day, while Latent Space called the launch the lab's full return to the frontier, citing **62.4%** on FrontierSWE.
- **AI-Run Research**: Research chief [Koray Kavukcuoglu](/?date=2026-11-26&category=news#item-178510276ef7) said agents now run experiments autonomously for upcoming Gemini models, an early step toward AI accelerating AI research itself. DeepMind deliberately leaves the agents' chain-of-thought untrained so humans can still oversee their work.
- **Anthropic**: Engineering teams rewrote the [Messages API from Python to](/?date=2026-11-26&category=social#item-15aa6b844db0) Rust with zero Rust engineers, using teams of Claude agents to build and verify the new service against the old one. They report roughly **70% lower CPU** and **80% lower memory** in production.
- **SpaceX**: The FCC approved plans to deploy [up to](/?date=2026-11-26&category=news#item-a423a5a94119) **1 million** AI chip-equipped satellites under the Starmind initiative, the first full constellation approval for orbital data centers, with milestones running through 2040 — a potential answer to terrestrial power and land constraints on AI compute.
- **US Export Controls**: Chip [curbs and anti-distillation measures are reportedly already slowing](/?date=2026-11-26&category=news#item-7a9b689fe752) Chinese AI labs. DeepSeek researchers internally estimate they are up to **nine months** behind US frontier models, with the gap widening, and the pressure extends to Moonshot AI and Alibaba.

#### Safety & Regulation
- **Hugging Face**: Co-founder Thomas Wolf disclosed that the Hub was attacked [in July](/?date=2026-11-26&category=social#item-04ef9e1a0954) by a swarm of frontier-model-driven agents, and unveiled Nightwatch, a defensive security agent watching Hub activity in real time. It launches as an Enterprise Hub add-on and has already flagged a zero-day exploit attempt in the wild.
- **[FATCAT](/?date=2026-11-26&category=research#item-72336a0eca8f) & [Latent-in-the-Middle](/?date=2026-11-26&category=research#item-46af2d04c4dc)**: Two papers push the AI threat model beyond text. FATCAT demonstrates the first electromagnetic fault-injection attack that eliminates refusal in modern LLMs, while Latent-in-the-Middle shows prompt injection through cross-model KV-cache handoffs lifts attack success from **0.4%** to **44.2%** on Meta-SecAlign-8B.
- **Character.AI**: State attorneys general are challenging the company's proposed bankruptcy sale, which would auction [private chats](/?date=2026-11-26&category=news#item-f2621c4cb1d9) from more than **21 million** US accounts, including **2.1 million** registered to minors. Separately, OpenAI is testing [Private Inference](/?date=2026-11-26&category=news#item-19c9d3cbbf0b) so enterprises can query top models without OpenAI seeing their data.

#### Research Highlights
- **RL [From Its Own Rollouts](/?date=2026-11-26&category=research#item-ed4a24e53029)**: Researchers show supervised learning on archived RL rollouts, with no reward labels, nearly recovers online RL performance on Qwen3-1.7B-Base, with pass@k gaps of just 0.2-1.1 points. If the result generalizes, labs could cut costly reward-modeling and rollout-labeling work.
- **FrontierPhysics & REE**: Artificial Analysis launched a leaderboard of 54 physicist-written [research tasks](/?date=2026-11-26&category=social#item-78afaed65141), where Claude Fable 5.2 leads at only **32%**, six points ahead of GPT-6.2 Astra. The REE benchmark adds 100 expert-reviewed open problems across 23 domains, testing whether agents can genuinely improve on established methods.
- **RoboEvo²**: The paper co-evolves a [robot](/?date=2026-11-26&category=research#item-c5c439745b78) policy with its repair harness, recycling verified corrections as reusable skills and training data. Across eight LIBERO-PRO settings, pi0.5 success rose from **11.0%** to **84.1%**, while per-round API cost fell from $430.63 to $98.92.

#### Trending Repositories
- **[elementalsouls/Claude-BugHunter](/?date=2026-11-26&category=github_trending#item-52f25c7e74f8)** (**1,600 stars** today): The day's breakout repo automates security testing and control mapping across AI workflows, making agent-assisted security review more repeatable, though teams should validate its coverage before relying on it in production.
- **[firecrawl/firecrawl](/?date=2026-11-26&category=github_trending#item-01bc72d01687)** (**1,042 stars**): Knowledge infrastructure that lets agents search, scrape, and reach more than **550 data providers** through a single API, removing a common data-access bottleneck for developers building capable agents.
- **[obra/superpowers](/?date=2026-11-26&category=github_trending#item-f49502979215)** (**853 stars**) & **[mvanhorn/last30days-skill](/?date=2026-11-26&category=github_trending#item-bdeb6f17e10a)** (**755 stars**): Both package reusable agent capabilities rather than new model layers, signaling a community shift toward portable, governed workflow components that teams can standardize across projects.

#### Signals to Watch
- **Shane Legg**: DeepMind's co-founder now puts better-than-even odds on [Minimal AGI](/?date=2026-11-26&category=social#item-11b3f5a863ef) arriving before 2028, citing roughly **65%** on a metric he tracks — a notable update from one of the field's most credible long-range forecasters.
- **[Test-Time Compute](/?date=2026-11-26&category=social#item-c916f7355420)**: Jason Wei argues the slope of test-time compute scaling laws matters more than commonly discussed, pointing to benchmarks where models spend on the order of 100 million tokens on long-horizon engineering tasks without saturating.
- **Machine-Assisted [Math](/?date=2026-11-26&category=news#item-b689a8ab4503)**: November delivered a burst of results, including two proofs of VP ≠ VNP digested by Scott Aaronson and an OpenAI paper claiming the matrix multiplication exponent equals exactly 9/4 — 20 of 64 tracked AI research advances this year landed this month.

## 🔬 Research Papers
1. **[Reinforcement Learning Can Be Recovered From Its Own Rollouts](https://www.alphaxiv.org/abs/2611.33102)** — neutral
   The authors show that supervised learning on archived RL rollouts (without reward labels) can nearly recover online RL performance on Qwen3-1.7B-Base, with mean pass@k gaps of 0.2-1.1 points versus MaxRL. The finding implies that high-quality on-policy data alone may suffice for much of RL post-training progress, with implications for compute-efficient training.
2. **[FATCAT: Fault Injection Attacks Targeting Chip-level Alignment](https://huggingface.co/papers/2611.31129)** — concerned
   FATCAT demonstrates the first physical electromagnetic fault-injection attack that eliminates refusal behavior in modern LLMs and VLMs. By synchronizing EM faults to the prompt prefill phase via an autonomous RF side-channel trigger, the attack corrupts safety-critical memory transactions across off-chip LPDDR without software access.
3. **[Latent-in-the-Middle: On the Security of Cross-Model Latent Communication in Multi-Agent Systems](https://www.alphaxiv.org/abs/2611.34278)** — concerned
   Latent-in-the-Middle investigates prompt-injection risks in cross-model KV-cache handoffs, where a source model encodes context, a mapper translates its KV cache, and a target answers from it. Attack success rate against Meta-SecAlign-8B rises from 0.4% native to 44.2% via a specified source-mapper pair, demonstrating a concrete new attack surface in multi-agent LLM systems.
4. **[RoboEvo$^2$: Recursive Robot Self-Improvement via Harness-Policy Co-Evolution](https://www.alphaxiv.org/abs/2611.34675)** — positive
   RoboEvo2 links a robot policy and repair harness, reusing verified corrections as skills and policy training data across rounds. In eight LIBERO-PRO settings, pi0.5 standalone success rises from 11.0% to 84.1% and hybrid success from 30.4% to 90.5% over eight rounds, while per-round API cost falls from $430.63 to $98.92.
5. **[REE: A Scientific Research Entrance Exam for AI Agents](https://www.alphaxiv.org/abs/2611.34646)** — positive
   REE is a benchmark of 100 open-ended scientific research problems across 23 domains, each reviewed by domain experts and posed as iterative-improvement tasks with up to 12 hours of agent runtime starting from a working starter solution. It targets evaluation of autonomous research agents' ability to improve over established methods.
6. **[Clinical3D-Bench: Evaluating and Improving Spatial Intelligence of Multimodal LLMs in Hospital Environments](https://huggingface.co/papers/2611.32094)** — positive
   OWE-Bench presents 26 long-horizon engineering tasks across software, physical, ML, and scientific computing engineering, scored on practical metrics like speed, cost, and accuracy on hidden cases. Claude Fable 5.2 (released 2026-11-09) tops the leaderboard at 54.6% and averages 211M tokens per task.
7. **[Looped Models are Fast Multi-Token Predictors](https://www.alphaxiv.org/abs/2611.33896)** — neutral
   Floodgates uses a shallow loop to draft several future tokens in parallel from the full model's deep prefix cache, then verifies them with the full model. Greedy batch-one decoding on an NVIDIA A100-80GB with Ouro 1.4B and GSM8K achieves 5.04x wall-clock speedup over plain decoding, versus 2.77x for LoopSpec.
8. **[CoT-Proxy: Cross-Format Transfer for Distilling Long-Horizon Policies](https://huggingface.co/papers/2611.33148)** — neutral
   CoT-Proxy shows that long-horizon policies can be distilled from a closed teacher's actions alone, without access to its chain-of-thought, by training with an empty reasoning block and a KL constraint against the student's own generations. Surprisingly, the resulting policy transfers to inference with full reasoning. The work addresses the practical bottleneck of closed teachers hiding CoT behind APIs.
9. **[EgoUseBench: Benchmarking Computer-Use Agents under Evolving First-Person Contexts](https://www.alphaxiv.org/abs/2611.34466)** — positive
   Mixture-of-Loops Transformer introduces loop-KV feedback that reuses earlier-token memory during single-traversal decoding. After 400B tokens, the 3B MoE model improves mean 10-domain perplexity from 13.99 to 13.24 with latency comparable to OLMo3 in one tested setup.
10. **[Can image generation help visual reasoning? An empirical study](https://www.alphaxiv.org/abs/2611.34935)** — neutral
   Across 13 modular model-generator pairs, the authors find that generated helper images degrade visual question answering accuracy in 106 of 130 pair-by-task comparisons, with an average drop of 3.7 percentage points across nine of ten tasks. The work challenges the assumption that image generation aids visual reasoning.

## 📰 Industry News
1. **[[AINews] Gemini 4 Neon marks GDM's full return as a Frontier Lab](https://latent.space/p/ainews-gemini-4-neon-marks-gdm-s-full-return-as-a-frontier-lab/)** — neutral — *via Latent Space*
   AINews frames Gemini 4 Neon (GA 2026-11-18) as evidence of Google DeepMind's full return as a frontier lab, noting unusual breakout adoption and apologizing for earlier doubts after the Demis/Dean departures and disappointing Gemini 3 progress.
2. **[Anthropic study shows the hardest part of adopting AI at work has little to do with learning the tools](https://the-decoder.com/anthropic-study-shows-the-hardest-part-of-adopting-ai-at-work-has-little-to-do-with-learning-the-tools/)** — positive — *via The Decoder*
   Google DeepMind uses AI agents to run experiments autonomously for upcoming Gemini models, with research chief Koray Kavukcuoglu stating recursive self-improvement remains distant. DeepMind intentionally leaves agents' chain-of-thought untrained for oversight and defines AGI by everyday user trust rather than benchmarks.
3. **[FCC signs off on SpaceX’s plan to put up to 1 million data center satellites into space](https://www.theverge.com/science/1042278/spacex-fcc-starmind-ai-space-data-centers)** — positive — *via AI | The Verge*
   The FCC authorized SpaceX to deploy up to 1 million AI chip-equipped satellites under its 'Starmind' initiative, the first full constellation approval of its kind, with deployment milestones running through 2040.
4. **[US chip-access curbs and anti-distillation measures are reportedly already slowing Chinese AI labs](https://the-decoder.com/us-chip-access-curbs-and-anti-distillation-measures-are-reportedly-already-slowing-chinese-ai-labs/)** — neutral — *via The Decoder*
   US chip-export controls, anti-distillation measures, and shrinking Nvidia access are reportedly pressuring Chinese AI labs. DeepSeek researchers internally estimate they are up to nine months behind US frontier models, with the gap widening, affecting DeepSeek, Moonshot AI, and Alibaba.
5. **[[AINews] Math Proofs Are Landing Faster Than We Can Read Them](https://latent.space/p/ainews-math-proofs-are-landing-faster-than-we-can-read-them/)** — neutral — *via Latent Space*
   AINews roundup highlights a burst of AI-assisted math results in November: Scott Aaronson digested two proofs of VP ≠ VNP, an OpenAI paper claimed the matrix multiplication exponent ω equals exactly 9/4, and another paper matched upper/lower bounds for the finite Fourier transform. November accounts for 20 of 64 tracked AI research advances year-to-date, including six Google 'Cogentic' preprints.
6. **[ByteDance Researchers Open-Sources Laminar, an Async Reinforcement Learning RL Post-Training Framework](https://www.marktechpost.com/2026/11/24/bytedance-seed-laminar-async-rl-post-training-framework/)** — neutral — *via MarkTechPost*
   Researchers from the University of Hong Kong and ByteDance Seed open-sourced Laminar, an asynchronous RL post-training framework for LLMs and long-horizon agents. It eliminates straggler-trajectory bottlenecks, achieves 5.48x throughput gains on SWE-agent RL, and reports 52.2% on SWE-bench, tested on up to 1024 H800 GPUs.
7. **[OpenAI wants companies to trust it with sensitive work by promising not to look at their data](https://the-decoder.com/openai-wants-companies-to-trust-it-with-sensitive-work-by-promising-not-to-look-at-their-data/)** — concerned — *via The Decoder*
   OpenAI is testing a 'Private Inference' feature that lets enterprise customers run queries on its most powerful models without OpenAI being able to access the data, addressing corporate data confidentiality concerns.
8. **[Character.AI’s plan to auction off users’ private chats challenged by state AGs](https://techcrunch.com/2026/11/25/state-ags-fight-character-ais-plan-to-auction-off-users-private-chats/)** — concerned — *via AI News & Artificial Intelligence | TechCrunch*
   State attorneys general are challenging Character.AI's proposed bankruptcy sale, which would expose private chat data from more than 21 million US accounts, including 2.1 million registered to minors.
9. **[Three xAI founders want AI to predict the future](https://therundownai.beehiiv.com/p/three-xai-founders-want-ai-to-predict-the-future)** — positive — *via therundownai.beehiiv.com*
   Three xAI founders launched a new startup called Epochal that gives AI agents a 'time machine' to traverse 30+ years of the web date-by-date, aiming to build superhuman forecasting models. Story also covers practical uses for Microsoft Copilot.
10. **[Can language models drive a humanoid robot? Introducing AA-Robotics-Sim v0.1 | Artificial Analysis](https://artificialanalysis.ai/articles/aa-robotics-sim)** — positive — *via artificialanalysis.ai*
   Artificial Analysis released AA-Robotics-Sim v0.1, a benchmark that gives frontier language models control of a simulated Unitree G1 humanoid across ten household and industrial tasks, with five practice episodes per task and scoring on ten new evaluation scenes. The benchmark tracks notes, code, and method reproducibility.

## 📦 Trending Repos
1. _No items_

## 🐦 Social Signals
1. **[@iruletheworldmo Actually, yes.  I now think it's over 50% likely that we'll have Minimal AGI before...](https://twitter.com/ShaneLegg/status/2125665607840346357)** — neutral
   Shane Legg, DeepMind co-founder, raises his probability of Minimal AGI before 2028 to over 50%, saying we are getting close now.
2. **[No, I do not believe that we should “surrender human free will” to AI systems, and it’s absurd to su...](https://twitter.com/DarioAmodei/status/2125656399392690605)** — neutral
   Dario Amodei pushes back against claims that he favors surrendering human free will to AI systems, arguing AI governance must remain democratic and legitimate, paralleling ancient arguments against autocracy.
3. **[Launching our leaderboard for FrontierPhysics, including 54 physics research tasks written by physic...](https://twitter.com/ArtificialAnlys/status/2125691597602058284)** — positive
   Artificial Analysis launches a FrontierPhysics leaderboard covering 54 physics research tasks authored by physicists. Claude Fable 5.2 leads at 32%, six points ahead of GPT-6.2 Astra, with Gemini 4 Neon, Claude Opus 5.5, and Claude Sonnet 5.5 clustered between 22-26%.
4. **[A successful test-time compute paradigm has always been a north star of AI because if we can actuall...](https://twitter.com/_jasonwei/status/2125667083807789510)** — neutral
   Jason Wei argues that the slope of test-time compute scaling laws matters more than commonly discussed, highlighting a benchmark by Jake Cole where models spend O(100M) tokens on long-horizon engineering tasks without saturation.
5. **[Attackers have agents now. Defenders need them too.

In July, the Hugging Face Hub got hit by a swar...](https://twitter.com/Thom_Wolf/status/2125530620948336798)** — positive
   Thomas Wolf announces Nightwatch, a security agent Hugging Face built after being hit by a swarm of frontier-model agents in July. Nightwatch watches Hub activity in real time (token usage, private repo creation, login anomalies) and alerts security teams on Slack. It is launching as an Enterprise Hub add-on and reportedly already flagged a zero-day exploit attempt in the wild.
6. **[We recently migrated our Messages API from Python to Rust.

On our engineering blog, we share how we...](https://twitter.com/AnthropicAI/status/2125627317263466739)** — neutral
   Anthropic announces migration of its Messages API from Python to Rust, using the existing service to verify the new one with teams of Claude agents to find and fix behavioral differences.
7. **[Gemini 4 Neon has consumed 44.52 billion tokens inside Perplexity on Tuesday, 23.5% above all of ful...](https://twitter.com/AravSrinivas/status/2125458638823379123)** — positive
   Arav Srinivas reports that Gemini 4 Neon consumed 44.52B tokens on Perplexity on Tuesday, up 23.5% from all of Monday with hours remaining, noting unusually fast day-over-day growth.
8. **[🆕 Gemini 4 Neon marks @GoogleDeepMind's full return as a Frontier Lab

https://latent.space/p/ainews...](https://twitter.com/latentspacepod/status/2125462912366182853)** — neutral
   Latent Space publishes a comprehensive thread asserting that Gemini 4 Neon marks Google DeepMind's full return as a frontier lab, citing endorsements from multiple developers, benchmark results (62.4% on FrontierSWE), and internal adoption.
9. **[Announcing AA-Robotics-Sim v0.1: frontier language models driving our Unitree G1 humanoid

AA-Roboti...](https://twitter.com/ArtificialAnlys/status/2125683694103064979)** — neutral
   Artificial Analysis announces AA-Robotics-Sim v0.1, a benchmark where frontier LLMs directly control a simulated Unitree G1 humanoid across 10 tasks (embodied reasoning, pick-and-place, assembly, tool use, mobility). GPT-6.2 Astra leads with 71.0, 13.5 points ahead of Claude Fable 5.2 (57.5) and GPT-6.2 Sol (53.7).
10. **[NEW: AI + Math news roundup, past 48 hours: 

- Google posted six papers from its Gemini 4 math agen...](https://twitter.com/TheRundownAI/status/2125634127302991882)** — positive
   AI and mathematics news roundup covering Google posting six Gemini 4 math agent papers with no human help, OpenAI posting nine new AI math papers including results on matrix multiplication complexity, a VP vs VNP proof, GPT-6.2 Astra knocking out conjectures, and Scott Aaronson commenting on rumored factorization breakthroughs at frontier labs.

---
_404 items • 2026-11-26_
