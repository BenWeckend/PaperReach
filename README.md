# PaperReach — Intelligent Research Paper Discovery & Management

PaperReach is a research assistance tool designed to streamline academic literature discovery and management. It integrates metadata and full-text sources (e.g., arXiv, Semantic Scholar, and CrossRef), extracts relevant information from scientific papers, and provides a desktop interface for efficiently evaluating and organizing research findings.

<img width="1395" height="892" alt="Bildschirmfoto vom 2026-06-10 21-09-14" src="https://github.com/user-attachments/assets/3b28b96d-4a65-409a-b742-106bfb57f34a" />

The most important feature is the ability to adjust the granularity when researching user quotes or statements in scientific papers. This works in two modes:

**Standard Mode:** Leave the High Accuracy box unchecked to only compare the input with the paper's abstract.

**High Accuracy Mode:** Check the box to trigger a deep analysis of the entire PDF:
1. Downloads the PDF paper
2. Extracts the full text
3. Separates the text into chunks of 300 symbols
4. Compares the semantic similarity of each chunk to the input
5. Takes the highest score of all chunks as the final rating

## Project Goal

The goal of PaperReach is to take research texts, claims, or document sections as input and automatically discover, rank, and prepare relevant scientific publications for further analysis.

## Core Features (Planned / Implemented)

* **Multi-source Integration:** Connects to arXiv, Semantic Scholar, CrossRef, and other academic providers.
* **Metadata & PDF Retrieval:** Downloads and parses paper metadata and full-text content.
* **Claim Matching & Relevance Analysis:** Evaluates how well a paper supports or relates to a given claim, question, or research topic.
* **Embeddings & Semantic Search:** Supports vector embeddings and semantic retrieval pipelines for context-aware document discovery.
* **Desktop GUI:** Qt-based interface for exploring search results and managing saved papers.
* **Modular Architecture:** Clear separation of backend logic, data providers, and user interface components for easy extensibility.

## Project Structure

* `PaperReach_Qt/` — Qt client and desktop GUI application (`main.py` is the main entry point).
* `backend_server/` — Backend APIs, processing pipelines, and server-side components.
* `providers/` and `PaperReach_Qt/providers/` — Adapters for external services such as arXiv, Semantic Scholar, and CrossRef.
* `dev_tests/` — Development tests, validation scripts, and experimental prototypes.
* `docs/` and `pr-docs/` — Project documentation, diagrams, and supporting resources.

## Quick Start

### Requirements

* Python 3.9+
* Optional: `virtualenv` or `venv`

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r PaperReach_Qt/requirements.txt
```

### Launch the Desktop Application

```bash
python3 PaperReach_Qt/main.py
```

> **Note:** Some features require API keys (e.g., Semantic Scholar). Never store credentials directly in source code. Use environment variables or a `.env` file in the project root instead.

## Developer Notes

* **Testing:** See `dev_tests/` for available test scripts and experimental notebooks.
* **Adding Providers:** New academic sources should be implemented as provider modules under `providers/` and expose a consistent search/retrieval interface.
* **Embeddings & Retrieval:** Embedding-related functionality is located in `PaperReach_Qt/embeddings.py` and can be adapted to different backends, including local models and third-party embedding services.

## What Are Word Embeddings?

Word embeddings are dense vector representations of words, sentences, or documents in a high-dimensional vector space. Instead of representing text as discrete symbols, embeddings map semantic meaning into numerical vectors:

$$
E(w) \in \mathbb{R}^d
$$

where (w) is a word (or text fragment) and (d) is the embedding dimension.

Semantically similar texts are positioned close together in this vector space. Similarity is commonly measured using **cosine similarity**:

$$
\text{sim}(a,b)=\frac{a \cdot b}{|a| |b|}
$$

where (a) and (b) are embedding vectors.

For example, the embeddings of *"transformer architecture"* and *"attention-based neural network"* will typically have a higher similarity score than unrelated concepts. PaperReach leverages embeddings to perform semantic search, claim matching, and relevance ranking beyond simple keyword-based retrieval.
