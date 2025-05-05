import os
import subprocess
from dotenv import load_dotenv
import openai

# Load .env file
load_dotenv()

# Now read API key from env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment.")

# Pass the key to the client
client = openai.OpenAI(api_key=api_key)

# Get git diff
git_diff = subprocess.getoutput("git diff HEAD^ HEAD")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a CI/CD deployment assistant."},
        {"role": "user", "content": f"Here's the git diff:\n{git_diff}\nWhich tests should I run? Should I proceed with deployment?"}
    ]
)

decision = response.choices[0].message.content
print("Agent Decision:\n", decision)

# Save output
with open("tests_to_run.txt", "w") as f:
    f.write("test_user_auth.py test_api_rate_limit.py")
