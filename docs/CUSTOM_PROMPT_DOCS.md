# Custom System Prompt Feature

## Overview

The `IterBotReactAgent` now supports custom system prompts that can be appended to the default ReAct prompt. This allows you to customize the agent's behavior and persona while preserving all the core ReAct functionality.

## Features

- **Custom System Prompts**: Add personalized instructions to guide agent behavior
- **Size Limiting**: Automatic truncation of oversized prompts with smart word boundary detection
- **Dynamic Updates**: Change the custom prompt at runtime
- **Preserved ReAct**: Original ReAct functionality remains completely intact
- **Easy Management**: Simple methods to add, update, and remove custom prompts

## Usage

### Basic Usage

```python
from iterbot import IterBotReactAgent

# Create agent with custom system prompt
agent = IterBotReactAgent(
    custom_system_prompt="You are an expert data analyst. Always show your calculations.",
    max_custom_prompt_size=300
)

# The custom prompt will be appended to the ReAct instructions
result = agent.run("What's the current time?")
```

### Constructor Parameters

```python
IterBotReactAgent(
    model='llama3.2',                    # Ollama model to use
    tools=None,                          # Dictionary of tools (uses defaults if None)
    max_iterations=15,                   # Maximum reasoning iterations
    custom_system_prompt=None,           # Custom prompt to append (optional)
    max_custom_prompt_size=500           # Maximum characters for custom prompt
)
```

### Dynamic Management

```python
# Create agent without custom prompt
agent = IterBotReactAgent()

# Add custom prompt
agent.update_custom_system_prompt("You are a helpful coding assistant.")

# Check current custom prompt
print(agent.get_custom_system_prompt())

# Update the prompt
agent.update_custom_system_prompt("You are a creative problem solver.")

# Remove custom prompt (revert to default ReAct behavior)
agent.remove_custom_system_prompt()
```

### Size Limiting

```python
# Long prompts are automatically truncated
very_long_prompt = "This is a detailed instruction..." * 100

agent = IterBotReactAgent(
    custom_system_prompt=very_long_prompt,
    max_custom_prompt_size=200  # Will truncate to 200 characters
)

# Check the truncated result
print(f"Truncated prompt: {agent.get_custom_system_prompt()}")
```

## Examples

### Data Analysis Specialist

```python
data_analyst = IterBotReactAgent(
    custom_system_prompt="""You are a data analysis expert. When working with data:
    1. Always validate your calculations
    2. Provide context for any numbers you present
    3. Explain your methodology clearly
    4. Consider potential limitations or biases"""
)
```

### Creative Assistant

```python
creative_agent = IterBotReactAgent(
    custom_system_prompt="Think outside the box and offer innovative solutions. "
                        "Always consider multiple perspectives and encourage brainstorming."
)
```

### Teaching Assistant

```python
teacher_agent = IterBotReactAgent(
    custom_system_prompt="You are a patient teacher. Break down complex concepts into "
                        "simple steps and use analogies to help explain difficult topics."
)
```

### Persona Switching

```python
agent = IterBotReactAgent()

# Switch to different personas as needed
personas = {
    "analyst": "You are a precise, detail-oriented analyst.",
    "creative": "You are a creative problem-solver who thinks outside the box.",
    "teacher": "You are a patient teacher who explains concepts clearly."
}

# Use the analyst persona
agent.update_custom_system_prompt(personas["analyst"])
result = agent.run("Analyze this data...")

# Switch to creative persona
agent.update_custom_system_prompt(personas["creative"])
result = agent.run("How can we solve this problem differently?")
```

## System Prompt Structure

When a custom prompt is provided, the final system prompt follows this structure:

```
[Original ReAct Instructions]
- Available tools
- ReAct format (Thought/Action/Observation/Final Answer)
- Core behavioral guidelines

Additional instructions:
[Your Custom System Prompt]
```

This ensures that:
1. All ReAct functionality is preserved
2. Tool usage remains consistent
3. Your custom instructions enhance rather than replace the core behavior

## API Reference

### Methods

#### `update_custom_system_prompt(custom_prompt)`
Update the custom system prompt and regenerate the full system prompt.

**Parameters:**
- `custom_prompt` (str): New custom system prompt

#### `get_custom_system_prompt()`
Get the current custom system prompt.

**Returns:**
- `str` or `None`: The current custom system prompt

#### `remove_custom_system_prompt()`
Remove the custom system prompt, reverting to default ReAct behavior.

### Properties

#### `custom_system_prompt`
The current custom system prompt (read-only access).

#### `max_custom_prompt_size`
The maximum allowed size for custom prompts.

## Best Practices

1. **Keep it focused**: Custom prompts work best when they're specific and targeted
2. **Avoid conflicts**: Don't contradict the ReAct instructions in your custom prompt
3. **Test different sizes**: Experiment with `max_custom_prompt_size` for your use case
4. **Use dynamic updates**: Switch personas based on the type of task
5. **Preserve ReAct**: The custom prompt enhances, doesn't replace the ReAct behavior

## Migration from Previous Versions

Existing code continues to work without changes:

```python
# This still works exactly as before
agent = IterBotReactAgent()
```

To add custom prompts to existing code:

```python
# Before
agent = IterBotReactAgent(model='llama3.2', max_iterations=10)

# After (with custom prompt)
agent = IterBotReactAgent(
    model='llama3.2', 
    max_iterations=10,
    custom_system_prompt="Your custom instructions here"
)
```
