# ReAct Agent

A Python implementation of the ReAct (Reasoning + Acting) pattern for Large Language Models, inspired by [Simon Willison's implementation](https://til.simonwillison.net/llms/python-react-pattern).

## Overview

ReAct is a prompting pattern that enables LLMs to solve complex tasks by breaking them down into a loop of:
- **Thought**: Reasoning about the current state and what to do next
- **Action**: Executing a specific action from available tools
- **Observation**: Processing the result of that action
- **Answer**: Providing a final response based on accumulated information

## Features

- Uses OpenAI's GPT-4o-mini model
- Implements three built-in actions:
  - `wikipedia`: Search Wikipedia and get summaries
  - `calculate`: Perform mathematical calculations
  - `simon_blog_search`: Search Simon Willison's blog
- Interactive command-line interface
- Extensible action system

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd react-agent
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install openai httpx python-dotenv
```

4. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the agent from the command line:
```bash
python react_agent.py
```

Enter questions when prompted. The agent will:
1. Think about how to answer the question
2. Take appropriate actions using available tools
3. Observe the results
4. Provide a final answer

Example interaction:
```
Enter your question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
-- running wikipedia France
Observation: France is a country. The capital is Paris.
Answer: The capital of France is Paris
```

## Adding New Actions

To add a new action:

1. Add the action to the prompt template in `ReActAgent.__init__`
2. Add a corresponding method to the `ReActAgent` class
3. Register the action in `self.known_actions` dictionary

Example of adding a new action:
```python
@staticmethod
def new_action(input):
    # Implementation here
    return result

# Add to self.known_actions in __init__:
self.known_actions = {
    # ... existing actions ...
    "new_action": self.new_action
}
```

## Architecture

- `ChatBot`: Handles interactions with the OpenAI API
- `ReActAgent`: Implements the ReAct pattern and manages available actions
- Actions are implemented as static methods for simplicity
- Regular expressions parse action requests from the LLM's output

## License

[Insert your chosen license here]

## Credits

- Original ReAct pattern implementation by Simon Willison
- Built using OpenAI's GPT-4o-mini model
```


```