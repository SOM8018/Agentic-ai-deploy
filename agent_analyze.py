import openai
import subprocess
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get git diff
git_diff = subprocess.getoutput("git diff HEAD^ HEAD")

# Call OpenAI chat model using the new API
client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a CI/CD deployment assistant."},
        {"role": "user", "content": f"Here's the git diff:\n{git_diff}\nWhich tests should I run? Should I proceed with deployment?"}
    ]
)

decision = response.choices[0].message.content
print("Agent Decision:\n", decision)

# Save a mock test file list
with open("tests_to_run.txt", "w") as f:
    f.write("test_user_auth.py test_api_rate_limit.py")
