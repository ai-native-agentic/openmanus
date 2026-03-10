# A2A — Agent-to-Agent Protocol

Inter-agent communication via the A2A standard. Wraps OpenManus agents as A2A-compliant executors.

## STRUCTURE

```
a2a/
└── app/
    ├── main.py              # ENTRY: A2A server startup
    ├── agent.py             # A2AManus — wraps Manus agent for A2A invocation
    └── agent_executor.py    # ManusExecutor — AgentExecutor implementation
```

## KEY PATTERNS

### A2A Invocation
```python
class A2AManus:
    async def invoke(self, query: str, session_id: str) -> dict:
        # Creates Manus agent → agent.run(query) → returns {"content": ...}
```

### ManusExecutor
Implements `AgentExecutor` interface from the `a2a` library:
1. `_validate_request(context)` — check request format
2. `agent_factory()` — create fresh Manus agent
3. `agent.invoke(query, context_id)` — run task
4. `event_queue.enqueue_event(completed_task(...))` — emit result as `Part(root=TextPart(text=...))`

### Message Format
Results wrapped as: `Part(root=TextPart(text=content))` → `new_artifact()` → `completed_task()`. Uses `a2a.types` and `a2a.utils` from the A2A SDK.

## ANTI-PATTERNS

- Never instantiate Manus directly in A2A handlers — use `agent_factory` for fresh agent per request
- Never bypass ManusExecutor for A2A requests — it handles validation and event queueing
- The `print()` statements in `agent_executor.py` are debug artifacts — use `logger` instead
