# IterBot

A flexible Python framework for building AI agents that work with any Ollama model - whether they support tool calling or not.

IterBot implements the ReAct (Reasoning and Acting) pattern, allowing AI models to iteratively reason about problems and use tools to solve them step by step.

## Features

- **Works with any Ollama model** - No need for specific tool-calling model support
- **Built-in tools** - Includes time/date utilities out of the box
- **Custom tools** - Easy to add your own functions as tools
- **Custom system prompts** - Personalize agent behavior while preserving ReAct functionality
- **ReAct pattern** - Implements Reasoning and Acting for step-by-step problem solving
- **Loop detection** - Prevents infinite loops with automatic stopping
- **Configurable** - Adjust models, iteration limits, and verbosity
- **Simple API** - Get started with just a few lines of code

## Installation

```bash
pip install ollama
```

Make sure you have [Ollama](https://ollama.ai/) installed and running on your system.

## Quick Start

```python
from iterbot import IterBotReactAgent

# Create an agent with default settings
agent = IterBotReactAgent()

# Ask a question that requires tool usage
result = agent.run("What time is it?")
print(result)
```

## Usage Examples

### Basic Usage

```python
from iterbot import IterBotReactAgent

# Create the agent with default tools (time/date functions)
agent = IterBotReactAgent()
print("Agent ready to use!")

# Ask time-related questions
result = agent.run("What time is it?")
print(result)

result = agent.run("What's the current date?")
print(result)
```

### Custom Configuration

```python
# Custom configuration with different model and iteration limit
agent = IterBotReactAgent(
    model='phi4-mini',  # Different Ollama model
    max_iterations=10  # Different iteration limit
)

result = agent.run("What's the current date and time?")
print(result)
```

### Custom System Prompts

```python
# Agent with custom system prompt for specific behavior
agent = IterBotReactAgent(
    model='llama3.2',
    custom_system_prompt="You are an expert data analyst. Always show your calculations and provide statistical context.",
    max_custom_prompt_size=300
)

result = agent.run("What time is it and how does this relate to productivity patterns?")
print(result)

# Dynamic system prompt updates
agent.update_custom_system_prompt("You are a creative problem solver. Think outside the box.")
result = agent.run("What are some innovative ways to track time?")
print(result)

# Remove custom prompt to revert to default behavior
agent.remove_custom_system_prompt()
```

### Creating Custom Tools

```python
from iterbot import IterBotReactAgent
from IterBotTools import TimeTool

# Define custom tools
def calculator(expression):
    """Calculate mathematical expressions safely"""
    try:
        # Note: In production, use ast.literal_eval or a proper math parser
        return f"Result: {eval(expression)}"
    except Exception as e:
        return f"Error: {e}"

def get_weather(location):
    """Mock weather tool for demonstration"""
    return f"The weather in {location} is sunny and 75°F."

# Create agent with custom tools (replaces default tools)
custom_tools = {
    "get_weather": get_weather,
    "calculator": calculator,
    "get_current_time": TimeTool.get_current_time  # Keep some default tools
}

custom_agent = IterBotReactAgent(
    model='deepseek-r1',
    tools=custom_tools,
    max_iterations=15
)

# Use the custom tools
result = custom_agent.run("Calculate 15 * 23 + 7")
print(result)

result = custom_agent.run("What's the weather in Tokyo?")
print(result)
```

### Dynamic Tool Management

```python
# Start with default agent
agent = IterBotReactAgent()

# Add tools dynamically
def calculator(expression):
    """Calculate mathematical expressions safely"""
    try:
        return f"Result: {eval(expression)}"
    except Exception as e:
        return f"Error: {e}"

agent.add_tool("calculator", calculator)

# Now use the newly added tool
result = agent.run("What's 10 plus 5 times 2?")
print(result)

# List all available tools
print(f"Available tools: {agent.list_tools()}")

# Remove a tool if needed
agent.remove_tool("calculator")
```

### Controlling Verbosity

```python
# Verbose mode (default) - shows all reasoning steps
result = agent.run("What's the current time?", verbose=True)

# Non-verbose mode - only shows final result
result = agent.run("What's the current date?", verbose=False)
print(f"Final answer: {result}")
```

## Built-in Tools

IterBot comes with several time/date tools by default:

- `get_current_time()` - Returns current time in HH:MM:SS format
- `get_current_date()` - Returns current date in YYYY-MM-DD format  
- `get_current_datetime(format)` - Returns formatted datetime string
- `get_epoch_time()` - Returns Unix epoch timestamp

## Web Search with SearXNG

IterBot includes powerful web search capabilities through the SearXNG tool:

```python
from iterbot import IterBotReactAgent
from IterBotTools import SearXNGTool, get_default_tools

# Add web search to your agent
tools = get_default_tools()
tools["search_web"] = SearXNGTool.search_web

agent = IterBotReactAgent(
    tools=tools,
    custom_system_prompt="You can search the web for current information. Always cite sources."
)

# Search the web
result = agent.run("What are the latest developments in AI?")
print(result)
```

**Features:**
- Local or remote SearXNG instances
- Custom search engines (Google, Bing, DuckDuckGo, etc.)
- Configurable result limits
- Academic and news-focused search options

**Requirements:**
- `pip install httpx`
- Running SearXNG instance (see [setup guide](https://github.com/searxng/searxng))

For detailed SearXNG configuration and examples, see [SearXNG Tool Documentation](docs/SEARXNG_TOOL_DOCS.md).

## API Reference

### IterBotReactAgent

```python
class IterBotReactAgent:
    def __init__(self, model='llama3.2', tools=None, max_iterations=15, 
                 custom_system_prompt=None, max_custom_prompt_size=500):
        """
        Initialize the ReAct agent.
        
        Args:
            model (str): The Ollama model to use
            tools (dict): Dictionary of available tools {name: function}
            max_iterations (int): Maximum number of reasoning iterations
            custom_system_prompt (str, optional): Additional system prompt to append to the ReAct prompt
            max_custom_prompt_size (int): Maximum character length for custom system prompt (default: 500)
        """
```

#### Methods

- `run(user_input, verbose=True)` - Run the agent with a question/request
- `add_tool(name, function)` - Add a new tool to the agent
- `remove_tool(name)` - Remove a tool from the agent  
- `list_tools()` - List all available tools
- `update_custom_system_prompt(custom_prompt)` - Update the custom system prompt
- `get_custom_system_prompt()` - Get the current custom system prompt
- `remove_custom_system_prompt()` - Remove custom prompt, reverting to default ReAct behavior

## How It Works

IterBot implements the ReAct (Reasoning and Acting) pattern:

1. **Thought** - The agent reasons about the problem
2. **Action** - The agent calls a tool with specific arguments
3. **Observation** - The agent observes the tool's result
4. **Repeat** - Continue until a final answer is reached

The agent automatically formats its reasoning in this structure and uses JSON to call tools, making it compatible with any Ollama model regardless of built-in tool support.

## Testing Your Setup

```python
# Simple test to verify the agent class works
print("Testing IterBot class...")

try:
    test_agent = IterBotReactAgent()
    print("✅ Agent created successfully!")
    print(f"Available tools: {list(test_agent.tools.keys())}")
    print(f"Model: {test_agent.model}")
    print(f"Max iterations: {test_agent.max_iterations}")
except Exception as e:
    print(f"❌ Error creating agent: {e}")

# Test with actual Ollama (requires Ollama to be running)
# result = test_agent.run("What time is it?")
# print(f"Result: {result}")
```

## Requirements

### Core Requirements
- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running
- `ollama` Python package
- `pytz` Python Timezone Package

### Optional Dependencies
- `httpx` - Required for SearXNG web search functionality

## Documentation

For detailed information about advanced features, see:
- [Custom System Prompt Documentation](docs/CUSTOM_PROMPT_DOCS.md)
- [SearXNG Tool Documentation](docs/SEARXNG_TOOL_DOCS.md)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
