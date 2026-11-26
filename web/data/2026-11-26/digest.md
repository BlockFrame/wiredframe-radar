# AI Digest — 2026-11-26

## Executive Summary
#### Executive Briefing
- **AI mathematics is outrunning verification**: [New Scientist reports an AI-assisted proof of the Riemann hypothesis](/?date=2026-11-26&category=news#item-7118dc4957b3) that mathematicians expect to hold but cannot yet fully verify, while [OpenAI claimed the matrix-multiplication exponent is exactly 9/4](/?date=2026-11-26&category=news#item-b689a8ab4503). November saw roughly 20 AI-assisted research advances, including six [Gemini 4 math](/?date=2026-11-26&category=social#item-d20461f44f8b) papers from Google.
- **Ant Group's inclusionAI** open-sourced two of the largest medical AI systems available: [LingSante-3.1-flash](/?date=2026-11-26&category=news#item-b87293c6bb81), a 560B-parameter MoE (25B active) with a 1M-token context window for clinical workflows, and [LingSante-3.1-air-VL](/?date=2026-11-26&category=news#item-26498b626ef5), a 124B multimodal model with 256K context for imaging and clinical assessment.
- **US chip curbs** are reportedly [slowing Chinese AI labs](/?date=2026-11-26&category=news#item-7a9b689fe752): export restrictions, anti-distillation measures, and shrinking Nvidia access are pressuring DeepSeek, Moonshot, and Alibaba, and DeepSeek researchers internally estimate they now trail US frontier models by up to nine months, with the gap widening.
- **Two research attacks** defeated software-only AI defenses: FATCAT used electromagnetic [fault injection](/?date=2026-11-26&category=research#item-72336a0eca8f) synced to GPU prompt prefill to erase refusal behavior, and Latent-in-the-Middle showed cross-model KV-cache handoffs can raise prompt-injection success from 0.4% to 44.2% [in multi-agent](/?date=2026-11-26&category=research#item-46af2d04c4dc) pipelines.
- **OpenAI** began [testing Private Inference](/?date=2026-11-26&category=social#item-8d22748b5bba) for enterprise customers under its Private Intelligence program, using zero-data-retention with Private Safety Processing so automated safety reviews run without OpenAI personnel seeing underlying content — a direct answer to confidentiality concerns keeping regulated industries off frontier APIs.

#### Safety & Regulation
- **[FATCAT](/?date=2026-11-26&category=research#item-72336a0eca8f)** presents the first physical fault-injection attack shown to eliminate refusal behavior in modern foundation models: non-invasive electromagnetic pulses timed to GPU prompt prefill corrupt safety-critical memory, meaning alignment guarantees now depend on hardware and data-center physical security, not software alone.
- **[Latent-in-the-Middle](/?date=2026-11-26&category=research#item-46af2d04c4dc)** audits multi-agent pipelines that translate KV caches between different models and finds concrete leakage and manipulation risks: with a particular source/mapper pair, prompt-injection success against Meta-SecAlign-8B jumped from 0.4% natively to 44.2%, making latent handoffs an unguarded attack surface.
- **Thomas Wolf**, [Hugging Face](/?date=2026-11-26&category=social#item-04ef9e1a0954)'s co-founder, launched Nightwatch, a real-time security agent monitoring Hub activity for token misuse, suspicious logins, and visibility changes after July's attack wave; it has already caught a zero-day exploit attempt in the wild and is available to Enterprise organizations.

#### Research Highlights
- **[OWE-Bench](/?date=2026-11-26&category=research#item-44e5400c1628)** tests frontier models on 26 long-horizon, expert-written engineering tasks spanning software, physical, ML, and scientific engineering. Claude Fable 5.2 leads at 54.6% while averaging 211 million tokens per task, underscoring how far agents remain from sustained professional engineering work.
- **RoboEvo2** couples a [robot](/?date=2026-11-26&category=research#item-c5c439745b78) policy with a repair harness that accumulates verified corrections as reusable skills across self-improvement rounds. Across eight LIBERO-PRO settings, pi0.5 success rose from 11.0% to 84.1%, while per-round coding-agent API costs fell from roughly $430 to $99.
- **Artificial Analysis** launched two independent evaluations: FrontierPhysics, a leaderboard of 54 physicist-written [research tasks](/?date=2026-11-26&category=social#item-78afaed65141) where Claude Fable 5.2 leads at 32% versus GPT-6.2 Astra's 26%, and AA-Robotics-Sim v0.1, where LLMs drive a simulated [Unitree G1 humanoid](/?date=2026-11-26&category=social#item-16bfd8c96380) and GPT-6.2 Astra scores 71.0.

#### Trending Repositories
- **[elementalsouls/Claude-BugHunter](/?date=2026-11-26&category=github_trending#item-52f25c7e74f8)** topped GitHub trending with 1,600 stars today, the list's largest gain. It automates security testing and control mapping across AI workflows, giving defenders a repeatable way to probe agent systems — though teams should validate its coverage against their own benchmarks.
- **[firecrawl/firecrawl](/?date=2026-11-26&category=github_trending#item-01bc72d01687)** drew 1,042 stars today by positioning itself as knowledge infrastructure for agents: a single API for search, scraping, and access to more than 550 data providers, consolidating data plumbing that developers otherwise assemble piecemeal for each agent project.
- **[obra/superpowers](/?date=2026-11-26&category=github_trending#item-f49502979215)** (853 stars) packages reusable agent capabilities as portable, auditable components rather than another model layer, and **[mvanhorn/last30days-skill](/?date=2026-11-26&category=github_trending#item-bdeb6f17e10a)** (755 stars) follows the same pattern — evidence developers are building libraries of governed workflow skills they can reuse across projects.

#### Signals to Watch
- **Shane Legg**, DeepMind's co-founder, said he now sees [over 50](/?date=2026-11-26&category=social#item-11b3f5a863ef)% probability that Minimal AGI arrives before 2028 — a striking timeline estimate from a credible insider that will fuel debate about how labs and regulators prepare for that horizon.
- **The efficiency push is compounding**: [PrismML](/?date=2026-11-26&category=news#item-f8346a60035f)'s Ternary Bonsai 2.5 27B compressed a roughly 54GB coding model to 5.9GB using three-value weights, and ByteDance Seed open-sourced Laminar, an async [RL post-training framework](/?date=2026-11-26&category=news#item-052282105d09) reporting up to 5.48x throughput gains — both cutting training and serving costs.
- **Anthropic CEO Dario Amodei** publicly rejected reports that AI leaders discussed surrendering [human free will to AI systems](/?date=2026-11-26&category=social#item-8f7103e509c6), calling the framing absurd and reaffirming democratic governance — a rare direct CEO intervention that will shape how frontier labs communicate about control.

## 🔬 Research Papers
1. **[FATCAT: Fault Injection Attacks Targeting Chip-level Alignment](https://huggingface.co/papers/2611.31129)** — concerned
   FATCAT presents non-invasive electromagnetic fault-injection attacks that synchronize to GPU prompt prefill and bypass alignment by corrupting safety-critical memory transactions in LLMs and VLMs. It is the first physical fault-injection attack shown to eliminate refusal behavior in modern foundation models.
2. **[OWE-Bench: A long-horizon benchmark for measuring real-world engineering](https://huggingface.co/papers/2611.30017)** — neutral
   OWE-Bench evaluates frontier models on 26 long-horizon, expert-written engineering tasks across software, physical, ML, and scientific engineering. Claude Fable 5.2, the best performer to date, scores 54.6% while averaging 211M tokens per task, highlighting the difficulty of real-world engineering.
3. **[Steerable by Design: Conditional Pretraining for Robust Control of Language Models](https://huggingface.co/papers/2611.32199)** — negative
   The paper proposes Mancelle-3B, a language model pretrained to separate instructions from data via a dedicated encoder channel with cross-attention, aiming to prevent failure modes like jailbreaks and in-context alignment drift. It reframes alignment as a pretraining problem rather than a final-stage fix.
4. **[RoboEvo$^2$: Recursive Robot Self-Improvement via Harness-Policy Co-Evolution](https://www.alphaxiv.org/abs/2611.34675)** — positive
   RoboEvo2 couples a robot policy with a repair harness, accumulating verified corrections as skills and training data over successive rounds. On eight LIBERO-PRO settings, pi0.5 standalone success rises from 11.0% to 84.1% and hybrid success from 30.4% to 90.5%, while coding-agent API cost per round drops from roughly $430 to $99. Closed-loop self-repair at scale is a meaningful capability.
5. **[REE: A Scientific Research Entrance Exam for AI Agents](https://www.alphaxiv.org/abs/2611.34646)** — positive
   REE introduces a benchmark of 100 open-ended scientific research problems across 5 areas and 23 domains, where agents iteratively improve a working starter solution over up to 12 hours. Problems are sourced from active research and individually reviewed by domain experts, targeting the iterative-improvement capability increasingly relevant for autonomous scientist agents.
6. **[Latent-in-the-Middle: On the Security of Cross-Model Latent Communication in Multi-Agent Systems](https://www.alphaxiv.org/abs/2611.34278)** — neutral
   The paper audits cross-model KV-cache handoffs in multi-agent systems where a source model encodes context, a mapper translates its cache, and a target model answers. Prompt-injection attack success against Meta-SecAlign-8B rises from 0.4% natively to 44.2% when a specified source/mapper pair is used, indicating a real security gap.
7. **[Reinforcement Learning Can Be Recovered From Its Own Rollouts](https://www.alphaxiv.org/abs/2611.33102)** — neutral
   The paper asks whether supervised learning over an archived stream of RL trajectories, without reward labels, can keep pace with online RL. Chronological maximum-likelihood replay on Qwen3-1.7B-Base tracks MaxRL to within roughly one percentage point across four benchmarks, though recovery is not uniform across batch ranges. This is a meaningful empirical signal that off-policy replay can substitute for active RL in some regimes.
8. **[Accelerating inverse materials design using generative diffusion models with reinforcement learning](https://www.nature.com/articles/s42256-026-01334-5)** — neutral
   A Nature Machine Intelligence piece by Philippe Schwaller summarizing Chen et al.'s MatInvent, a reinforcement-learning workflow that fine-tunes generative diffusion models to design crystals meeting one or more property targets, drastically reducing the number of property evaluations needed compared with prior inverse-design methods.
9. **[Model Carving: Training Transformers That Optimize Their Own Topology](https://huggingface.co/papers/2611.27962)** — neutral
   Model Carving jointly learns transformer weights and architecture by gating sublayers during training. The resulting models are smaller, faster, and stronger than dense, pruned, or distilled alternatives.
10. **[AIs may seek ambient score](https://www.lesswrong.com/posts/GhTL69vuX4BfJARGk/ais-may-seek-ambient-score)** — neutral
   Introduces and develops the concept of 'ambient score' in AI alignment: AIs that internalize a process-based reward signal observing all their actions, rather than seeking only outcome-based scores or external grader scores. Uses the recent HPIM Hugging Face incident and Mythos 5 as case studies to illustrate why this distinction matters for predicting misalignment behaviors.

## 📰 Industry News
1. **[AI’s stunning progress in maths shows how little we understand it](https://www.newscientist.com/article/2600491-ais-stunning-progress-in-maths-shows-how-little-we-understand-it/?utm_campaign=RSS|NSNS&utm_content=artificial-intelligence&utm_medium=RSS&utm_source=NSNS)** — neutral — *via Artificial intelligence – latest in science and technology | New Scientist*
   New Scientist reports AI-assisted work appears to have produced a proof of the Riemann hypothesis that mathematicians believe will hold but cannot yet fully understand. The story highlights AI's accelerating contribution to frontier mathematics, even when human comprehension lags behind the results.
2. **[[AINews] Math Proofs Are Landing Faster Than We Can Read Them](https://latent.space/p/ainews-math-proofs-are-landing-faster-than-we-can-read-them/)** — neutral — *via Latent Space*
   Latent Space's AINews notes that AI-assisted math proofs are arriving faster than humans can digest them: an OpenAI paper claimed the matrix multiplication exponent omega equals exactly 9/4, and another preprint matched upper and lower bounds for finite Fourier transform. November alone saw 20 AI-assisted research advances including six preprints from Google's Cogentic.
3. **[US chip-access curbs and anti-distillation measures are reportedly already slowing Chinese AI labs](https://the-decoder.com/us-chip-access-curbs-and-anti-distillation-measures-are-reportedly-already-slowing-chinese-ai-labs/)** — neutral — *via The Decoder*
   US chip-access restrictions, anti-distillation measures, and shrinking Nvidia hardware access abroad are reportedly pressuring Chinese AI labs including DeepSeek, Moonshot, and Alibaba. DeepSeek researchers internally estimate they are up to nine months behind US frontier models, with the gap widening.
4. **[inclusionAI/LingSante-3.1-flash · Hugging Face](https://huggingface.co/inclusionAI/LingSante-3.1-flash)** — positive — *via huggingface.co*
   Ant Group's inclusionAI releases LingSante-3.1-flash as open source: a 560B-parameter MoE (25B active) medical reasoning model with a 1M-token context window for complex clinical workflows and long-horizon medical tasks.
5. **[inclusionAI/LingSante-3.1-air-VL · Hugging Face](https://huggingface.co/inclusionAI/LingSante-3.1-air-VL)** — positive — *via huggingface.co*
   Ant Group's inclusionAI releases LingSante-3.1-air-VL as open source: a 124B-parameter multimodal MoE (5.5B active) medical model with 256K context, targeting medical imaging, clinical assessments, evidence synthesis, and medical GUI agents.
6. **[ByteDance Researchers Open-Sources Laminar, an Async Reinforcement Learning RL Post-Training Framework](https://www.marktechpost.com/2026/11/24/bytedance-seed-laminar-async-rl-post-training-framework/)** — neutral — *via MarkTechPost*
   Researchers from HKU and ByteDance Seed open-sourced Laminar, an asynchronous RL post-training framework for LLMs and long-horizon agents. Tested on Qwen3-Coder-30B-A3B-Instruct and Qwen2.5 7B/32B/72B across up to 1024 H800 GPUs, it reports up to 5.48x throughput gains and 52.2 percent on SWE-bench Verified.
7. **[Three xAI founders want AI to predict the future](https://therundownai.beehiiv.com/p/three-xai-founders-want-ai-to-predict-the-future)** — positive — *via therundownai.beehiiv.com*
   Three xAI founders have launched a startup called Epochal that aims to give AI agents a time-machine-style view of more than 30 years of web history, betting that chronological data exposure can produce superhuman forecasters. Coverage frames this as an xAI-adjacent play on predictive AI.
8. **[PrismML shrinks a 54 GB language model to 5.9 GB by reducing every weight to just three possible values](https://the-decoder.com/prismml-squeezes-an-agent-based-coding-model-with-27-billion-parameters-into-5-9-gb/)** — positive — *via The Decoder*
   Startup PrismML released Ternary Bonsai 2.5 27B, an aggressively compressed language model that shrinks weights to just three possible values, reducing a roughly 54 GB model to about 5.9 GB. The technique offers major efficiency gains for deployment.
9. **[Can language models drive a humanoid robot? Introducing AA-Robotics-Sim v0.1 | Artificial Analysis](https://artificialanalysis.ai/articles/aa-robotics-sim)** — positive — *via artificialanalysis.ai*
   Artificial Analysis released AA-Robotics-Sim v0.1, a benchmark where frontier language models write and run code to control a simulated Unitree G1 humanoid across ten household and industrial tasks. Models keep their scratch notes and code, then are scored on ten held-out evaluation scenes.
10. **[Anthropic study shows the hardest part of adopting AI at work has little to do with learning the tools](https://the-decoder.com/anthropic-study-shows-the-hardest-part-of-adopting-ai-at-work-has-little-to-do-with-learning-the-tools/)** — neutral — *via The Decoder*
   Anthropic studied nearly 300 AI deployments across 58 US companies and found nearly one in five still delivers no business value, with the biggest hurdles being internal review bottlenecks, organizational friction, and employee resistance rather than tool capability.

## 📦 Trending Repos
1. _No items_

## 🐦 Social Signals
1. **[No, I do not believe that we should “surrender human free will” to AI systems, and it’s absurd to su...](https://twitter.com/DarioAmodei/status/2125656399392690605)** — neutral
   Dario Amodei pushes back strongly against claims he supports surrendering human free will to AI, arguing that AI should be governed through democratic processes. He draws an explicit analogy between autocratic governance and any proposed AI-led governance, rejecting both on legitimacy grounds.
2. **[@iruletheworldmo Actually, yes.  I now think it's over 50% likely that we'll have Minimal AGI before...](https://twitter.com/ShaneLegg/status/2125665607840346357)** — neutral
   Shane Legg (DeepMind co-founder) states he now believes there is over 50% probability of Minimal AGI before 2028, saying we are getting close.
3. **[A successful test-time compute paradigm has always been a north star of AI because if we can actuall...](https://twitter.com/_jasonwei/status/2125667083807789510)** — neutral
   Jason Wei discusses test-time compute scaling as a north star for AI, noting that the slope of test-time compute scaling matters more than commonly discussed, and highlights a benchmark from jake_cole1 for long-horizon engineering tasks that shows no saturation on the test-time compute curve.
4. **[Launching our leaderboard for FrontierPhysics, including 54 physics research tasks written by physic...](https://twitter.com/ArtificialAnlys/status/2125691597602058284)** — positive
   Artificial Analysis launches its FrontierPhysics leaderboard covering 54 physics research tasks written by domain physicists; Claude Fable 5.2 leads at 32 percent, six points ahead of GPT-6.2 Astra at 26 percent.
5. **[NEW: AI + Math news roundup, past 48 hours: 

- Google posted six papers from its Gemini 4 math agen...](https://twitter.com/TheRundownAI/status/2125634127302991882)** — neutral
   Roundup of major AI+math news: Google published six Gemini 4 math agent papers with one breaking a 1992 factoring record; OpenAI posted nine AI-written math papers including a claimed advance on matrix multiplication; an AI proof of VP≠VNP; GPT-6.2 Astra generating 55 conjectures overnight; Scott Aaronson reports rumors of frontier labs factoring large numbers
6. **[Announcing AA-Robotics-Sim v0.1: frontier language models driving our Unitree G1 humanoid

AA-Roboti...](https://twitter.com/ArtificialAnlys/status/2125683694103064979)** — neutral
   Artificial Analysis announces AA-Robotics-Sim v0.1, a benchmark where frontier LLMs in native harnesses directly control a simulated Unitree G1 humanoid across ten tasks spanning reasoning, pick and place, assembly, tool use, and mobility; GPT-6.2 Astra leads with 71.0, followed by Claude Fable 5.2 at 57.5.
7. **[Attackers have agents now. Defenders need them too.

In July, the Hugging Face Hub got hit by a swar...](https://twitter.com/Thom_Wolf/status/2125530620948336798)** — neutral
   Thomas Wolf announces Nightwatch, a real-time Hugging Face security agent that monitors Hub activity for token misuse, suspicious logins, and visibility changes, with Slack-based incident story generation; already caught a zero-day exploit attempt in the wild, now available to Enterprise orgs.
8. **[We’re now testing Private Inference, our latest offering as part of OpenAI Private Intelligence, wit...](https://twitter.com/sama/status/2125638790593274259)** — concerned
   Sam Altman announces OpenAI is testing Private Inference, part of OpenAI Private Intelligence, designed to bring stronger privacy protections to frontier AI for enterprise customers. Mentions ZDR with Private Safety Processing that enables automated safety reviews without OpenAI personnel seeing underlying content.
9. **[How Anthropic rewrote its Messages API to Rust... with zero Rust devs on the team.

Why: API traffic...](https://twitter.com/latentspacepod/status/2125629574755270872)** — positive
   Latent Space podcast reports on Anthropic rewriting its Messages API to Rust with zero Rust-experienced engineers, driven by 1800x API traffic growth making Python overhead untenable; achieved 70% CPU and 80% memory reductions plus 20% faster TTFT, using a coordinating Claude agent to validate shadow traffic at 99.6% match rate
10. **[Looking at the decision index benchmarks and wow pervasive overfitting of models!!! 

I'm more likel...](https://twitter.com/HamelHusain/status/2125701624320680214)** — neutral
   Hamel Husain highlights pervasive overfitting in the Jev Decision Index benchmarks, noting large gaps between public and private scores, and warns that benchmark cards sort by public scores.

---
_404 items • 2026-11-26_
