# AGENT — Agent Hierarchy & Execution

State-machine-based agent framework with ReAct pattern, step-based execution, and specialized agent types.

## STRUCTURE

```
agent/
├── base.py              # ENTRY: BaseAgent — state machine, memory, step loop
├── react.py             # ReActAgent — think() → act() pattern
├── toolcall.py          # ToolCallAgent — direct tool calling variant
├── manus.py             # Manus agent — computer use + planning + tools
├── browser.py           # Browser agent — web automation
├── swe.py               # SWE agent — software engineering (SWE-bench)
├── data_analysis.py     # Data analysis agent
├── mcp.py               # MCP-integrated agent
└── sandbox_agent.py     # Sandboxed execution wrapper
```

## KEY PATTERNS

### Agent State Machine
```python
class AgentState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FINISHED = "finished"
    ERROR = "error"
```
Transitions via `state_context(new_state)` async context manager. Error → auto-transition to ERROR state.

### Execution Loop
`BaseAgent.run(request)` → loop `step()` up to `max_steps` → check state (FINISHED?) → return result. Stuck detection: `duplicate_threshold` consecutive identical outputs triggers `handle_stuck_state()`.

### Agent Hierarchy
```
BaseAgent (state machine, memory, step loop)
  └── ReActAgent (think → act pattern)
       ├── Manus (computer use + planning)
       ├── BrowserAgent (web automation)
       ├── SWEAgent (software engineering)
       └── DataAnalysisAgent
  └── ToolCallAgent (direct tool calling)
```

### Memory
`Memory` stores `Message` list. `update_memory(role, content)` appends. Memory is passed to LLM on each step.

## ANTI-PATTERNS

- Never skip `state_context()` for state transitions — it handles ERROR recovery
- Never exceed `max_steps` by modifying the counter — it's the termination safety net
- Never subclass `BaseAgent` directly for tool-using agents — use `ReActAgent` or `ToolCallAgent`
