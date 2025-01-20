import os
import re
import httpx
from openai import OpenAI
from dotenv import load_dotenv
import fal_client

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages
        )
        return completion.choices[0].message.content

class ReActAgent:
    def __init__(self):
        self.prompt = """
        You run in a loop of Thought, Action, PAUSE, Observation.
        At the end of the loop you output an Answer
        Use Thought to describe your thoughts about the question you have been asked.
        Use Action to run one of the actions available to you - then return PAUSE.
        Observation will be the result of running those actions.

        Your available actions are:

        calculate:
        e.g. calculate: 4 * 7 / 3
        Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

        wikipedia:
        e.g. wikipedia: Django
        Returns a summary from searching Wikipedia

        simon_blog_search:
        e.g. simon_blog_search: Django
        Search Simon's blog for that term

        generate_image:
        e.g. generate_image: A beautiful sunset over mountains
        Generates an image based on the provided description using Flux Pro AI

        Always look things up on Wikipedia if you have the opportunity to do so.
        For image generation requests, use the generate_image action with a detailed description.

        Example session:

        Question: What is the capital of France?
        Thought: I should look up France on Wikipedia
        Action: wikipedia: France
        PAUSE

        You will be called again with this:

        Observation: France is a country. The capital is Paris.

        You then output:

        Answer: The capital of France is Paris
        """.strip()
        
        self.action_re = re.compile(r'^Action: (\w+): (.*)$')
        self.known_actions = {
            "wikipedia": self.wikipedia,
            "calculate": self.calculate,
            "simon_blog_search": self.simon_blog_search,
            "generate_image": self.generate_image
        }

    def query(self, question, max_turns=5):
        i = 0
        bot = ChatBot(self.prompt)
        next_prompt = question
        while i < max_turns:
            i += 1
            result = bot(next_prompt)
            print(result)
            actions = [self.action_re.match(a) for a in result.split('\n') if self.action_re.match(a)]
            if actions:
                action, action_input = actions[0].groups()
                if action not in self.known_actions:
                    raise Exception(f"Unknown action: {action}: {action_input}")
                print(f" -- running {action} {action_input}")
                observation = self.known_actions[action](action_input)
                print("Observation:", observation)
                next_prompt = f"Observation: {observation}"
            else:
                return

    @staticmethod
    def wikipedia(q):
        return httpx.get("https://en.wikipedia.org/w/api.php", params={
            "action": "query",
            "list": "search",
            "srsearch": q,
            "format": "json"
        }).json()["query"]["search"][0]["snippet"]

    @staticmethod
    def simon_blog_search(q):
        results = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
            "sql": """
            select
              blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
              blog_entry.created
            from
              blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
            where
              blog_entry_fts match escape_fts(:q)
            order by
              blog_entry_fts.rank
            limit
              1""".strip(),
            "_shape": "array",
            "q": q,
        }).json()
        if not results:
            return "No blog entries found matching that search."
        return results[0]["text"]

    @staticmethod
    def calculate(what):
        return eval(what)

    @staticmethod
    def generate_image(prompt):
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(log["message"])

        try:
            result = fal_client.subscribe(
                "fal-ai/flux-pro/v1.1-ultra",
                arguments={"prompt": prompt},
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            if result and "images" in result and len(result["images"]) > 0:
                return f"Image generated successfully. URL: {result['images'][0]['url']}"
            return "Failed to generate image."
        except Exception as e:
            return f"Error generating image: {str(e)}"

def main():
    agent = ReActAgent()
    
    # Example usage
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        agent.query(question)

if __name__ == "__main__":
    main() 