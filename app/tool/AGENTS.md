# TOOL — Tool Registration & Execution

Pydantic-based tool system with `BaseTool` ABC, `ToolCollection` registry, and specialized tools for computer use, browser, web search, and file operations.

## STRUCTURE

```
tool/
├── base.py                  # ENTRY: BaseTool ABC + ToolResult model
├── tool_collection.py       # ToolCollection registry (execute by name, to_params for LLM)
├── computer_use_tool.py     # Desktop GUI automation (Anthropic computer use API)
├── browser_use_tool.py      # Browser control and web automation
├── web_search.py            # Web search (Google, Bing, DuckDuckGo)
├── crawl4ai.py              # Crawl4AI web scraping wrapper
├── file_operators.py        # File read/write/edit
├── str_replace_editor.py    # String replacement editor (SWE-bench pattern)
├── python_execute.py        # Python code execution
├── bash.py                  # Bash command execution
├── planning.py              # Multi-step task planning
├── ask_human.py             # Human-in-the-loop tool
├── terminate.py             # Task termination tool
├── create_chat_completion.py # LLM sub-call tool
├── mcp.py                   # MCP tool bridge
├── search/                  # Search tool variants
├── sandbox/                 # Sandboxed execution tools
└── chart_visualization/     # Data visualization tools
```

## KEY PATTERNS

### BaseTool Interface
```python
class BaseTool(ABC, BaseModel):
    name: str
    description: str
    parameters: Optional[dict]
    async def execute(self, **kwargs) -> Any: ...    # Implement this
    def to_param(self) -> Dict: ...                   # OpenAI function calling format
    def success_response(self, data) -> ToolResult: ...
    def fail_response(self, msg) -> ToolResult: ...
```

### ToolCollection
Registry pattern: `tool_collection.execute(name, input)` → `ToolResult`. `to_params()` generates function definitions for LLM.

### ToolResult Composition
`ToolResult` supports `+` operator for combining results: `result_a + result_b` merges output/error/base64_image.

## ANTI-PATTERNS

- Never skip `ToolCollection` for tool dispatch — direct tool calls bypass logging/error handling
- Never return raw strings from tools — use `success_response()` / `fail_response()` for consistent `ToolResult`
- Tool `parameters` dict must follow OpenAI function calling JSON Schema format
