# MISSO AI Agent

An AI-powered administrative reference assistant built as a portfolio project to demonstrate enterprise AI engineering concepts using Python, Retrieval-Augmented Generation (RAG), vector search, tool calling, guardrails, audit logging, and a web-based user interface.

## Overview

The MISSO AI Agent allows users to ask administrative questions in natural language and receive responses grounded in approved reference documents.

Rather than relying only on the language model's existing knowledge, the application retrieves relevant information from its document knowledge base before generating an answer.

The system is designed to avoid unsupported answers when sufficient reference information is not available.

## Key Features

- Retrieval-Augmented Generation (RAG)
- Semantic search using OpenAI embeddings
- ChromaDB vector database
- PDF and text document ingestion
- Document chunking
- Source metadata and page tracking
- Retrieval confidence scoring
- AI tool selection
- Administrative knowledge search tool
- Reference document listing tool
- Domain guardrails
- Grounded-response controls
- JSONL audit logging
- Automated retrieval evaluation
- Streamlit chat interface
- Environment-variable protection for API credentials

## Architecture

```text
User
  |
  v
Streamlit Web Interface
  |
  v
AI Agent
  |
  +--> Guardrails
  |
  +--> Tool Selection
          |
          +--> Search Knowledge
          |       |
          |       v
          |    ChromaDB
          |       |
          |       v
          |    RAG Pipeline
          |
          +--> List Available References
  |
  v
Grounded AI Response
  |
  v
Audit Log