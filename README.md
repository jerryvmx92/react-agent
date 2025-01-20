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
- Implements four built-in actions:
  - `wikipedia`: Search Wikipedia and get summaries
  - `calculate`: Perform mathematical calculations
  - `simon_blog_search`: Search Simon Willison's blog
  - `generate_image`: Generate images using Flux Pro AI
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
pip install openai httpx python-dotenv fal-client
```

4. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your-openai-api-key-here
FAL_KEY=your-fal-api-key-here
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

Example interactions:
```
Enter your question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
-- running wikipedia France
Observation: France is a country. The capital is Paris.
Answer: The capital of France is Paris

Enter your question: Generate an image of a sunset over mountains
Thought: I should use the image generation feature to create this scene
Action: generate_image: A beautiful sunset over mountains with warm orange and purple hues, casting long shadows across snow-capped peaks
-- running generate_image
Observation: Image generated successfully. URL: [generated-image-url]
Answer: I've generated an image of a sunset over mountains for you. You can view it at the provided URL.
```

## Image Generation with Flux Pro

The agent integrates with Flux Pro AI for image generation capabilities. This feature:
- Uses the fal-ai/flux-pro/v1.1-ultra model
- Generates high-quality images from text descriptions
- Supports detailed prompts for precise image creation
- Provides real-time generation progress updates
- Returns a URL to the generated image

To use the image generation feature:
1. Ensure you have a valid FAL API key in your `.env` file
2. Use natural language to request image generation
3. The agent will automatically format your request and generate the image
4. You'll receive a URL to view the generated image

Note: Image generation requests cost $0.06 per image.

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

MIT License

Copyright (c) 2024 [Gerardo Vargas]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits

- Original ReAct pattern implementation by Simon Willison
- Built using OpenAI's GPT-4o-mini model