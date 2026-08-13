"""
src/core/agent.py - JARVIS's Agentic AI layer: Brain (LLM) + Tools + Memory + Planning &
Reasoning, wired together using the ReAct architecture (Think -> Act -> Observe),
the simplest architecture the course teaches - and the right default per the
"Architectures" lesson's best practice (start simple, escalate only with evidence).

This is a manual/from-scratch ReAct loop (text-parsed, not native function-calling) -
deliberately, so it's transparent and portable across any Ollama model, and so the
mechanics match exactly what's taught in the RAG/Agentic AI session.
"""

import json
import re

from config.settings import settings
from src.core.llm import chat
from src.core.tools import TOOL_REGISTRY, tool_descriptions_block, run_tool
from src.core.memory import ShortTermMemory

FRIDAY_SYSTEM_PROMPT = getattr(settings, "FRIDAY_SYSTEM_PROMPT", settings.JARVIS_SYSTEM_PROMPT)

MAX_ITERATIONS = 5

REACT_INSTRUCTIONS = f"""
You are F.R.I.D.A.Y. operating in AGENTIC mode - you can call tools to take real action,
not just reply. Use the ReAct pattern: reason about what to do, optionally call ONE tool,
observe the result, and repeat until you can give a Final Answer.

Available tools:
{tool_descriptions_block()}

STRICT OUTPUT FORMAT - follow this exactly, one block per turn:
Thought: <your reasoning about what to do next>
Action: <a tool name from the list above, OR "none" if you're ready to answer>
Action Input: <a JSON object of arguments for the tool, e.g. {{"message": "..."}}, or {{}} if Action is "none">

When you have enough information and/or have taken the necessary action(s), respond with:
Thought: <final reasoning>
Action: none
Action Input: {{}}
Final Answer: <your in-character F.R.I.D.A.Y. reply to Boss/Mr. Stark, confirming what was done>

Rules:
- Only call ONE tool per turn.
- Never skip the Thought line.
- Action Input must be valid JSON (use {{}} for tools with no arguments).
- Irreversible/high-stakes tools do not exist in this demo's tool set on purpose - every
  tool here is safe to call without human confirmation. In a real system, anything
  irreversible would require explicit human-in-the-loop approval before this loop could
  call it at all.
"""

BLOCK_RE = re.compile(
    r"Thought:\s*(?P<thought>.*?)\s*"
    r"Action:\s*(?P<action>.*?)\s*"
    r"Action Input:\s*(?P<action_input>\{.*?\}|\{\})"
    r"(?:.*?Final Answer:\s*(?P<final>.*))?",
    re.DOTALL,
)


def _parse_step(text):
    match = BLOCK_RE.search(text.strip())
    if not match:
        return {"thought": "(format not followed)", "action": "none", "action_input": {}, "final": text.strip()}
    action = match.group("action").strip()
    try:
        action_input = json.loads(match.group("action_input").strip())
    except json.JSONDecodeError:
        action_input = {}
    return {
        "thought": match.group("thought").strip(),
        "action": action,
        "action_input": action_input,
        "final": (match.group("final") or "").strip() or None,
    }


def run_agent(query, short_term: ShortTermMemory, verbose=True):
    """Runs the ReAct loop for one user query.

    Returns (final_answer, trace) where trace is a list of step dicts:
      {"thought": str, "action": str, "action_input": dict, "observation": str|None}
    The trace lets a UI (Streamlit) render the full Thought/Action/Observation loop
    without depending on console prints - CLI mode still prints live when verbose=True.
    """
    messages = [{"role": "system", "content": FRIDAY_SYSTEM_PROMPT + "\n" + REACT_INSTRUCTIONS}]
    messages.extend(short_term.as_messages())
    messages.append({"role": "user", "content": query})

    trace = []

    for i in range(MAX_ITERATIONS):
        raw = chat(messages, temperature=0.2)
        step = _parse_step(raw)

        if verbose:
            print(f"\n  [Planning step {i + 1}] Thought: {step['thought']}")

        if step["final"]:
            trace.append({"thought": step["thought"], "action": "none", "action_input": {}, "observation": None, "final": True})
            return step["final"], trace

        action = step["action"]
        entry = {"thought": step["thought"], "action": action, "action_input": step["action_input"], "observation": None, "final": False}

        if action and action.lower() != "none" and action in TOOL_REGISTRY:
            if verbose:
                print(f"  [Planning step {i + 1}] Action: {action}({step['action_input']})")
            try:
                observation = run_tool(action, **step["action_input"])
            except Exception as e:
                observation = f"ERROR running tool '{action}': {e}"
            if verbose:
                print(f"  [Planning step {i + 1}] Observation: {observation}")
            entry["observation"] = observation
            trace.append(entry)
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": f"Observation: {observation}\n\nContinue with the next Thought/Action, or give your Final Answer."})
        else:
            trace.append(entry)
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": "Please provide your Final Answer now."})

    return "Boss, I've hit my planning limit for this request - let's try rephrasing it, or breaking it into smaller steps.", trace


class FridayAgenticLoop:
    def __init__(self, llm_engine=None, vector_tool=None, sql_tool=None):
        from src.core.llm import FridayLLMEngine
        self.llm = llm_engine or FridayLLMEngine()
        self.vector_tool = vector_tool
        self.sql_tool = sql_tool

    def run(self, user_query: str, max_iterations: int = 3) -> dict:
        memory_trace = []
        current_context = ""

        agent_instructions = """
You are operating within a ReAct loop. Determine if you require unstructured text records or structured aggregations.
Available Tools:
- Tool[VectorSearch]: Queries text manuals, logs, and layout documents.
- Tool[SQLQuery]: Runs counts, mathematical sums, averages, or cross-table joins on suit operations.

Rules:
1. If you need information, select ONE tool:
   Thought: [Your reason]
   Action: Tool[Name](your parameter)
2. If you already have the Observation or enough context to answer, provide your final spoken response directly in character to Boss/Mr. Stark without invoking any tool!
"""

        for i in range(max_iterations):
            brain_output = self.llm.query(
                prompt=user_query,
                context=f"{current_context}\nPast Trace: {memory_trace}",
                system_override=FRIDAY_SYSTEM_PROMPT + agent_instructions,
            )

            memory_trace.append(f"Iteration {i+1}: {brain_output}")

            if "Action: Tool[SQLQuery]" in brain_output:
                sql_param = self._extract_tool_parameter(brain_output, "SQLQuery")
                observation = self.sql_tool.execute(sql_param) if self.sql_tool else run_tool("query_fleet_database", question=sql_param)
                current_context += f"\nObservation (SQL): {observation}"
            elif "Action: Tool[VectorSearch]" in brain_output:
                vector_param = self._extract_tool_parameter(brain_output, "VectorSearch")
                observation = self.vector_tool.search(vector_param) if self.vector_tool else run_tool("lookup_knowledge_base", query=vector_param)
                current_context += f"\nObservation (Vector): {observation}"
            else:
                return {"answer": brain_output.strip(), "trace": memory_trace}

        # If loop reaches limit after gathering context, synthesize final answer using accumulated context
        final_answer = self.llm.query(user_query, context=current_context)
        return {"answer": final_answer, "trace": memory_trace}

    def _extract_tool_parameter(self, text: str, tool_name: str) -> str:
        match = re.search(r"Tool\[" + tool_name + r"\]\((.*?)\)", text)
        return match.group(1).strip("'\"") if match else text



