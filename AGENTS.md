# OPENMANUS - KNOWLEDGE BASE

**Generated:** 2026-03-10
**Commit:** 99eae65
**Branch:** main

## OVERVIEW

Open-source computer use agent framework — no invite code needed. Desktop GUI automation, browser control, planning, MCP integration, and agent-to-agent (A2A) protocol. From MetaGPT team. Supports multiple LLM providers, sandboxed execution, and SWE-bench tasks.

Stack: Python 3.12, asyncio, Anthropic SDK, MCP, Crawl4AI, Protocol Buffers

## STRUCTURE

openmanus/
├── app/
│   ├── agent/
│   ├── daytona/
│   ├── flow/
│   ├── mcp/
│   ├── prompt/
│   ├── sandbox/
│   ├── tool/
│   ├── utils/
├── assets/
├── config/
├── examples/
│   ├── benchmarks/
│   └── use_case/
├── openmanus.egg-info/
├── protocol/
│   └── a2a/
├── tests/
│   └── sandbox/
├── workspace/
├── AGENTS.md
├── README.md
├── main.py

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Run GUI agent | `main.py` | Desktop automation with computer use tools |
| LLM providers | `app/llm.py` | Supports Anthropic, OpenAI, custom providers |
| System prompts | `app/prompt/manus.py` | Main agent instructions |
| Planning | `app/prompt/planning.py` + `app/tool/planning.py` | Multi-step task planning |
| Browser control | `app/prompt/browser.py` | Web automation instructions |
| SWE tasks | `app/prompt/swe.py` | Software engineering benchmarks |
| Web search | `app/tool/web_search.py` | Search tool integration |
| Web crawling | `app/tool/crawl4ai.py` | Crawl4AI wrapper |
| MCP integration | `run_mcp.py` + `app/prompt/mcp.py` | Model Context Protocol client |
| A2A protocol | `protocol/a2a/app/agent_executor.py` | Agent-to-agent messaging |
| Configuration | `config/main.yaml` | Model, tools, workspace settings |
| Sandboxed exec | `sandbox_main.py` | Isolated agent environment |

## CONVENTIONS

### Agent-to-Agent (A2A) Protocol
```python
# protocol/a2a/app/agent.py
class Agent:
    async def execute(self, task: str) -> Response:
        # Plan → Execute → Return results
        ...
```

### Tool Registration
```python
# app/tool/base.py
@register_tool
def my_tool(param: str) -> str:
    """Tool description for LLM"""
    ...
```

### Message Schema
```python
# app/schema.py
class Message:
    role: str  # "user" | "assistant"
    content: str | list[ContentBlock]
```

### Config Format (YAML)
```yaml
model: claude-3-5-sonnet-20241022
provider: anthropic
workspace: ./workspace
tools:
  - computer_use
  - browser
  - web_search
```

## ANTI-PATTERNS (THIS PROJECT)

| Forbidden | Why | Reference |
|-----------|-----|-----------|
| Running without sandbox in production | Security risk for desktop automation | `sandbox_main.py` |
| Hardcoding API keys in code | Use env vars or config | `config/main.yaml` |
| Skipping planning for multi-step tasks | Leads to inefficient execution | `app/tool/planning.py` |
| Blocking I/O in async context | Violates async-first design | `app/llm.py` |
| Manual tool registration | Use `@register_tool` decorator | `app/tool/base.py` |

## PROVEN RESULTS

**Production Features**:
- Desktop GUI automation (computer use API)
- Browser control with planning
- MCP protocol integration
- Agent-to-agent communication (A2A)
- SWE-bench task support
- Multi-provider LLM support (Anthropic, OpenAI)
- Hugging Face demo available

**MetaGPT Team**:
- Core authors: Xinbin Liang, Jinyu Xiang
- Contributors: Zhaoyang Yu, Jiayi Zhang, Sirui Hong
- Launched prototype in 3 hours
- Related project: OpenManus-RL (UIUC collaboration)

## COMMANDS

```bash
# Setup (conda)
conda create -n open_manus python=3.12
conda activate open_manus
pip install -r requirements.txt

# Run GUI agent
python main.py

# Run with flow
python run_flow.py

# Run MCP client
python run_mcp.py

# Run MCP server
python run_mcp_server.py

# Run sandboxed
python sandbox_main.py

# Tests
pytest tests/
```

## NOTES

- **No invite code**: Open-source alternative to proprietary Manus
- **Computer use**: Full desktop automation via Anthropic API
- **A2A protocol**: Agent-to-agent messaging for multi-agent systems
- **MCP support**: Model Context Protocol for tool integration
- **OpenManus-RL**: Separate project for RL-based agent tuning (GRPO)
- **Hugging Face demo**: https://huggingface.co/spaces/lyh-917/OpenManusDemo
- **Discord**: https://discord.gg/DYn29wFk9z
