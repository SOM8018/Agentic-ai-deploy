import openai
import subprocess

# Get git diff
git_diff = subprocess.getoutput("git diff HEAD^ HEAD")

# Call LLM (or local agent) to analyze
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a CI/CD deployment assistant."},
        {"role": "user", "content": f"Here's the git diff:\n{git_diff}\nWhich tests should I run? Should I proceed with deployment?"}
    ]
)

decision = response['choices'][0]['message']['content']
print("Agent Decision:\n", decision)

# Save output for GitHub Actions (e.g., via env or file)
with open("tests_to_run.txt", "w") as f:
    f.write("test_user_auth.py test_api_rate_limit.py")
