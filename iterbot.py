import json
import ollama
import re

from IterBotTools import TimeTool, get_default_tools

# System prompt to guide ReAct behavior
class IterBotReactAgent:
    """A ReAct (Reasoning and Acting) agent that uses Ollama for inference."""
    
    def __init__(self, model='llama3.2', tools=None, max_iterations=15):
        """
        Initialize the ReAct agent.
        
        Args:
            model (str): The Ollama model to use
            tools (dict): Dictionary of available tools {name: function}
            max_iterations (int): Maximum number of reasoning iterations
        """
        self.model = model
        self.tools = tools if tools is not None else get_default_tools()
        self.max_iterations = max_iterations
        
        # Generate system prompt based on available tools
        self.system_prompt = self._generate_system_prompt()
    
    def _generate_system_prompt(self):
        """Generate system prompt based on available tools."""
        tool_descriptions = []
        for i, (tool_name, tool_func) in enumerate(self.tools.items(), 1):
            # Extract function signature for documentation
            import inspect
            sig = inspect.signature(tool_func)
            tool_descriptions.append(f"{i}. {tool_name}{sig}")
        
        tools_text = "\n".join(tool_descriptions)
        system_prompt = f"""You are a reasoning agent. You can use tools to solve problems step by step.
        Available tools:
        {tools_text}

        Use this format:
        Thought: [your reasoning]
        Action: {{"tool": "tool_name", "args": {{arg1: val1, ...}}}}

        IMPORTANT: After outputting an Action, STOP and wait for the Observation. Do NOT generate the Observation yourself.
        The Observation will be provided to you automatically after the tool executes.
        
        Only after receiving real Observations can you output a Final Answer.
        
        When you have enough information, output:
        Final Answer: [your final answer to the user]

        Never generate fake Observations. Only output Thought and Action, then wait.
        """
        return system_prompt

    def _is_final_answer(self, content):
        """Detect if the agent has produced a final answer."""
        return bool(re.search(r"Final Answer\s*:", content, re.IGNORECASE))
    
    def _parse_action(self, content):
        """Extract the Action JSON from the agent's output."""
        for line in content.splitlines():
            if line.strip().startswith("Action:"):
                action_json = line.replace("Action:", "").strip()
                try:
                    return json.loads(action_json)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON in action: {e}")
        return None
    
    def run(self, user_input, verbose=True):
        """
        Run the agent with a given input.
        
        Args:
            user_input (str): The user's question or request
            verbose (bool): Whether to print intermediate steps
            
        Returns:
            str: The agent's final answer
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]

        iter_count = 0
        recent_actions = []

        while iter_count < self.max_iterations:
            response = ollama.chat(model=self.model, messages=messages)
            content = response['message']['content']
            
            if verbose:
                print(f"\nAgent:\n{content}")

            # Parse Action JSON from the response first
            tool_executed = False
            try:
                tool_call = self._parse_action(content)
                if not tool_call:
                    observation = "Observation: No valid Action found."
                else:
                    tool_name = tool_call["tool"]
                    args = tool_call["args"]

                    # Loop detection: stop if repeating the same action 3 times in a row
                    recent_actions.append(tool_name)
                    if len(recent_actions) >= 3 and recent_actions[-3:] == [tool_name]*3:
                        observation = f"Observation: Repeated action '{tool_name}' detected. Stopping."
                        if verbose:
                            print(observation)
                        break

                    if tool_name in self.tools:
                        result = self.tools[tool_name](**args)
                        observation = f"Observation: {result}"
                        tool_executed = True
                    else:
                        observation = f"Observation: Unknown tool '{tool_name}'"
            except Exception as e:
                observation = f"Observation: Error parsing tool call - {e}"

            # Check for final answer after tool execution
            if self._is_final_answer(content) and not tool_executed:
                # Extract the final answer
                final_answer = self._extract_final_answer(content)
                return final_answer

            # Append LLM output and observation to the conversation
            if tool_executed or not self._is_final_answer(content):
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": observation})
            else:
                # If there's a final answer and no tool was executed, return it
                final_answer = self._extract_final_answer(content)
                return final_answer

            iter_count += 1

        if iter_count >= self.max_iterations:
            if verbose:
                print("\nAgent stopped: iteration limit reached.")
            return "Agent stopped: iteration limit reached."
        
        return "Agent stopped unexpectedly."
    
    def _extract_final_answer(self, content):
        """Extract the final answer from the agent's response."""
        lines = content.splitlines()
        for line in lines:
            if re.search(r"Final Answer\s*:", line, re.IGNORECASE):
                return line.split(":", 1)[1].strip()
        return content  # Fallback to full content if no clear final answer found
    
    def add_tool(self, name, function):
        """Add a new tool to the agent."""
        self.tools[name] = function
        self.system_prompt = self._generate_system_prompt()
    
    def remove_tool(self, name):
        """Remove a tool from the agent."""
        if name in self.tools:
            del self.tools[name]
            self.system_prompt = self._generate_system_prompt()
    
    def list_tools(self):
        """List all available tools."""
        return list(self.tools.keys())