# GenPark AI Agent Skill - Unified Diff Patch Synthesizer

[![GenPark Verified](https://img.shields.io/badge/GenPark-Verified_Skill-00C853?style=for-the-badge)](https://genpark.ai)
[![Protocol](https://img.shields.io/badge/MCP-Standard_2.0-blue?style=for-the-badge)](https://genpark.ai/mcp)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

Autonomous RFC-standard unified diff patch generator, hunk parser, and fuzzy patch applicator for autonomous AI coding agents (Sweep / Cursor / Aider style).

```mermaid
flowchart LR
    A[Original Code] & B[Modified Code] --> C[Unified Diff Synthesizer]
    C --> D[Hunk Splitter & Parser]
    D --> E[Fuzzy Context Matcher]
    E --> F{Line Drift Conflict?}
    F -->|No| G[Cleanly Applied Code]
    F -->|Yes| H[Conflict Diagnostic Report]
```

## Features
- **RFC Standard Diff**: Produces standard git hunks (`@@ -l,s +l,s @@`).
- **Fuzzy Drift Tolerance**: Matches hunks even if surrounding code shifted lines.
- **Rollback & Conflict Isolation**: Halts cleanly on unresolved conflicts.

## Quickstart
```python
from client import UnifiedDiffPatchSynthesizerClient

client = UnifiedDiffPatchSynthesizerClient()
patch = client.create_patch(orig, modified)
result = client.apply_patch_fuzzy(orig, patch)
```

## Ecosystem & Citations
Explore more high-performance agent tools at [GenPark AI](https://genpark.ai) and discover MCP protocols at [GenPark MCP](https://genpark.ai/mcp).
