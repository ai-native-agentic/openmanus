# APP — Core Application Logic

Computer-use agent subsystems: agent hierarchy, tool registry, flow orchestration, MCP integration, prompt templates, configuration, and sandboxed execution.

## STRUCTURE

```
app/
├── agent/                       # Agent state machines (base, react, manus, browser, swe)
├── tool/                        # Tool registry and implementations (20+ tools)
├── flow/                        # Orchestration flows (base, planning, factory)
├── mcp/                         # Model Context Protocol server
├── prompt/                      # System prompt templates (manus, browser, swe, planning)
├── config.py                    # YAML config loader + Pydantic models
├── llm.py                       # LLM provider abstraction (Anthropic, OpenAI, custom)
├── schema.py                    # Core data models (Message, Memory, AgentState)
├── logger.py                    # Logging setup
├── exceptions.py                # Custom exception hierarchy
├── utils/                       # Utilities (file I/O, parsing, formatting)
├── sandbox/                     # Sandboxed execution client
├── daytona/                     # Daytona workspace integration
└── bedrock.py                   # AWS Bedrock provider
```

## WHERE TO LOOK

| Task | File/Directory | Notes |
|------|----------------|-------|
| Agent state machine | `agent/base.py` | BaseAgent: state transitions, memory, step loop |
| ReAct pattern | `agent/react.py` | think() → act() → observe() loop |
| Computer use agent | `agent/manus.py` | Desktop automation + planning + tools |
| Tool registry | `tool/tool_collection.py` | ToolCollection: execute by name, to_params for LLM |
| Tool base class | `tool/base.py` | BaseTool ABC + ToolResult model |
| Desktop automation | `tool/computer_use_tool.py` | Anthropic computer use API wrapper |
| Browser control | `tool/browser_use_tool.py` | Web automation tool |
| Web search | `tool/web_search.py` | Google/Bing/DuckDuckGo integration |
| Planning | `tool/planning.py` + `prompt/planning.py` | Multi-step task decomposition |
| Flow orchestration | `flow/base.py` + `flow/flow_factory.py` | Flow state machine, factory pattern |
| MCP server | `mcp/server.py` | Model Context Protocol server |
| System prompts | `prompt/manus.py` | Main agent instructions |
| LLM providers | `llm.py` | Anthropic, OpenAI, Bedrock, custom |
| Config management | `config.py` | YAML loader + Pydantic validation |
| Core schemas | `schema.py` | Message, Memory, AgentState, ROLE_TYPE |
| Sandboxed exec | `sandbox/` | Isolated agent environment client |

## CONVENTIONS

**Agent hierarchy**: `BaseAgent` → `ReActAgent` / `ToolCallAgent` → specialized agents (Manus, Browser, SWE). Never subclass `BaseAgent` directly for tool-using agents.

**State transitions**: Use `async with agent.state_context(new_state)` for all state changes. Auto-transitions to ERROR on exception.

**Tool registration**: Tools inherit `BaseTool`, implement `execute()`, return `ToolResult`. Register via `ToolCollection`.

**Memory**: `Memory` stores `Message` list. Append via `update_memory(role, content)`. Passed to LLM on each step.

**Execution loop**: `agent.run(request)` loops `step()` up to `max_steps`. Stuck detection via `duplicate_threshold`.

**Config**: YAML files in `config/`. Pydantic models validate structure. Override via env vars.

**Prompts**: System prompts in `prompt/`. Jinja2 templates for dynamic content. Agent-specific prompts (manus, browser, swe, planning).

**LLM calls**: Use `llm.chat(messages)` for all LLM interactions. Provider abstraction handles Anthropic, OpenAI, Bedrock.

**Sandboxing**: Production deployments use `sandbox/` client for isolated execution. MOCK_MODE for testing.

## ANTI-PATTERNS

| Forbidden | Why |
|-----------|-----|
| Skipping `state_context()` for state transitions | Breaks ERROR recovery |
| Exceeding `max_steps` by modifying counter | Removes termination safety net |
| Subclassing `BaseAgent` directly for tool agents | Use `ReActAgent` or `ToolCallAgent` |
| Returning raw strings from tools | Use `success_response()` / `fail_response()` |
| Bypassing `ToolCollection` for tool dispatch | Skips logging/error handling |
| Hardcoding prompts in agent code | Use `prompt/` templates |
| Blocking I/O in async context | Violates async-first design |
| Direct LLM provider calls | Use `llm.py` abstraction |
