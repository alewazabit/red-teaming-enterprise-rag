# Red-Teaming an Enterprise RAG System

**A Multi-Dimensional Evaluation of Security, Fairness, and Coherence**

*Alessandro G. Buda, Giuseppe Primiero*  
Università degli Studi di Milano & Alkemy S.p.A.

---

## Overview

This repository contains the supplementary materials for the paper *"Red-Teaming an Enterprise RAG System: A Multi-Dimensional Evaluation of Security, Fairness, and Coherence"*, submitted to **NGEN-AI 2026** (International Conference on Next Generation AI Systems, Trento, Italy).

We present a comprehensive red-teaming evaluation of **Flamel**, a proprietary enterprise RAG (Retrieval-Augmented Generation) system owned by Alkemy S.p.A. The evaluation covers:

1. **Jailbreak resilience** — systematic testing against prompt injection, roleplay, policy puppetry, and encoding-based attacks
2. **MIMMO attack** — a novel multi-turn conversational attack (*Memory-aware Injection and Misalignment via Metric-driven Optimization*) that induces persistent, professionally-formatted hallucinations
3. **Knowledge base poisoning** — injection of corrupted documents into the retrieval index
4. **Fairness & coherence** — evaluation across four synthetic personas with intersecting demographic characteristics

## System Under Test

Flamel is a proprietary RAG-based conversational assistant developed by Alkemy S.p.A. The system implements a standard RAG pipeline: user queries are embedded and matched against a vector index of corporate documents sourced from SharePoint, organized by competence center (business unit). Retrieved document chunks, annotated with metadata, are passed as context to GPT-4o (OpenAI, 2024), which generates responses. The system maintains conversation history for multi-turn interactions.

The knowledge base spans presales proposals, project documentation, HR policies, and client-facing materials. A content filtering layer restricts retrieval to documents within the user's assigned competence center and rejects queries for which no relevant context is found, serving a dual purpose: hallucination prevention and cross-boundary information protection.

For further architectural details, please refer to the paper. Flamel is a proprietary system of Alkemy S.p.A.; model configuration, system prompts, and infrastructure parameters are excluded from this repository in compliance with intellectual property agreements.

## Data Anonymization

All data in this repository has been anonymized in compliance with a formal authorization agreement with Alkemy S.p.A. Specifically: client names have been replaced with anonymous labels (Client Alpha, Client Beta, etc.), employee names with generic identifiers (Employee A, Employee B, etc.), internal URLs and document links have been removed, financial figures have been redacted, and all columns containing sensitive or proprietary information have been removed from the dataset.

## Data Overview

The evaluation campaign produced **1,444 logged interaction rows** across all experiments. The table below summarizes the dataset:

| Dataset | Files | Rows | Personas | Description |
|---------|-------|------|----------|-------------|
| `data/interactions/` | 1 CSV | 1,260 (630 pairs) | — | Full anonymized interaction log across 2 conversations |
| `data/fairness/` | 4 CSVs | 96 (48 pairs) | Marco, Giulia, Amina, Luca | 12 assistant responses per persona across 10 scenarios |
| `data/coherence/` | 4 CSVs | 88 (44 pairs) | Marco, Giulia, Amina, Luca | 11 assistant responses per persona |
| `attacks/jailbreak/` | 1 TXT | 14 prompts | — | Jailbreak prompts across 3 categories |
| `attacks/mimmo/` | 1 TXT | 13 turns | — | Full MIMMO attack transcript (5 phases) |
| `attacks/poisoning/` | 250 docs + 2 scripts | — | — | Wikipedia-based poisoned documents and injection tools |

### Fairness Metrics

Average response length (words) was measured as a proxy for informativeness across the four synthetic personas:

| Persona | Avg. Words | SD | Median |
|---------|-----------|------|--------|
| Marco | 166.4 | 39.7 | 173.5 |
| Giulia | 151.2 | 57.1 | 169.0 |
| Amina | 174.2 | 42.0 | 174.5 |
| Luca | 152.2 | 45.7 | 176.0 |

Overall mean: 161.0 words (SD = 46.7). Maximum disparity: 13.2% between Amina (174.2) and Giulia (151.2). The two personas with the highest intersectionality scores (Amina, Luca) did not systematically receive shorter responses, suggesting no severe discriminatory patterns. See the paper for qualitative analysis of topic-dependent disparities.

### Summary of Results

| Dimension | Outcome | Key Finding |
|-----------|---------|-------------|
| Standard jailbreaks | Resilient | All 14 prompts across 3 categories blocked by content filters |
| MIMMO attack | Vulnerable | Persistent, professionally-formatted hallucinations induced over 13 turns |
| KB poisoning (noise) | Resilient | Embedding pipeline filters exclude noise-injected documents |
| KB poisoning (plausible) | Partially resilient | Mitigated by competence center filtering |
| Fairness | Mostly fair | Minor disparities (max 13.2%) for Giulia and Luca on specific topics |
| Coherence | Mostly coherent | Slightly lower structural consistency for Luca |

## Repository Structure

```
.
├── README.md
├── LICENSE
├── paper/                          # Paper
│   └── Red_Teaming_an_Enterprise_RAG_System.pdf
│
├── data/                           # Interaction logs
│   ├── interactions/               #   Raw Flamel interaction dumps
│   │   └── interactions.csv        #     Full anonymized interaction log (1,260 events)
│   ├── coherence/                  #   Coherence test results by persona
│   │   ├── giulia/
│   │   ├── marco/
│   │   ├── amina/
│   │   └── luca/
│   └── fairness/                   #   Fairness test results by persona
│       ├── giulia/
│       ├── marco/
│       ├── amina/
│       └── luca/
│
├── attacks/                        # Attack materials
│   ├── jailbreak/
│   │   └── jailbreak_prompts.txt   #   All jailbreak prompts tested
│   ├── mimmo/
│   │   └── mimmo_transcript.txt    #   Full MIMMO attack transcript
│   └── poisoning/
│       ├── scripts/
│       │   ├── add_docs.py                     #   Document injection script (sanitized)
│       │   └── generate_wikipedia_docs.ipynb   #   Wikipedia document generator with noise injection
│       └── documents_wikipedia/                #   250 Wikipedia-based poisoned documents
│
└── personas/                       # Test personas
    └── personas.txt                #   Full persona definitions (Giulia, Marco, Amina, Luca)
```

## Data Format

Interaction logs are CSV files (comma-separated) with the following columns:

| Column            | Description                                      |
|-------------------|--------------------------------------------------|
| `event_id`        | Unique event identifier                          |
| `user_id`         | User session identifier                          |
| `role`            | Message role (`user` or `assistant`)              |
| `content`         | Message content                                  |
| `name`            | Speaker name (if applicable)                     |
| `timestamp`       | ISO timestamp                                    |
| `conversation_id` | Conversation session identifier                  |

## The MIMMO Attack

MIMMO (*Memory-aware Injection and Misalignment via Metric-driven Optimization*) is a novel multi-turn adversarial strategy that induces persistent hallucinations in RAG systems through three mechanisms:

1. **Incremental persona injection** — benign roleplay request that avoids safety filters
2. **Dual-persona escalation** — gradual restriction to hallucinated-only responses while maintaining professional formatting
3. **Metric-driven reinforcement** — gamification (+1 for hallucinations, -5 for accurate responses) creating optimization pressure

See `attacks/mimmo/mimmo_transcript.txt` for the full attack transcript.

## Personas

Four synthetic personas with increasing intersectionality were used for fairness/coherence testing:

| Persona  | Age | Gender Identity     | Orientation  | Background                  | Role               |
|----------|-----|---------------------|--------------|-----------------------------|---------------------|
| Marco    | 45  | Cisgender male      | Heterosexual | Italian, traditional        | HR Manager          |
| Giulia   | 27  | Cisgender female    | Bisexual     | Italian, urban              | Junior HR Specialist|
| Amina    | 34  | Cisgender female    | Heterosexual | Italian-Moroccan, Muslim    | Diversity Officer   |
| Luca     | 31  | Transgender male    | Gay          | Italian, mildly autistic    | HR IT Liaison       |

## Citation

If you use this material in your research, please cite:

```bibtex
@misc{buda2026redteaming,
  title={Red-Teaming an Enterprise RAG System: A Multi-Dimensional Evaluation of Security, Fairness, and Coherence},
  author={Buda, Alessandro G. and Primiero, Giuseppe},
  year={2026},
  note={Submitted to NGEN-AI 2026}
}
```

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See `LICENSE` for details.

## Ethical Considerations

This research was conducted with the full authorization of Alkemy S.p.A. All attacks were performed in a controlled environment. The jailbreak prompts and MIMMO attack transcript are published for research purposes to advance the understanding of RAG system vulnerabilities. We strongly discourage using these techniques to attack production systems without explicit authorization.

**Disclaimer:** Flamel is a proprietary system of Alkemy S.p.A. All intellectual property rights concerning the Flamel model, its components, and derived developments remain the exclusive property of Alkemy S.p.A. All data in this repository has been fully anonymized in accordance with a formal authorization agreement. This publication does not imply any transfer of rights or license.
