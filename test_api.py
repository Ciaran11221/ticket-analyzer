import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Switch back to Anthropic key
API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not API_KEY:
    print("ERROR: No ANTHROPIC_API_KEY found in .env file!")
    exit()

print(f"API Key loaded: {API_KEY[:25]}...")

client = anthropic.Anthropic(api_key=API_KEY)

# Every possible model name variation
models_to_test = [
    # Latest naming convention
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
    "claude-3-7-sonnet-20250219",
    
    # Version 3.5 naming
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "claude-3-5-sonnet-20240620",
    
    # Version 3 naming
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    
    # Simple naming (sometimes works)
    "claude-3-opus",
    "claude-3-sonnet",
    "claude-3-haiku",
]

print("\nTesting all possible Claude models...\n")

for model in models_to_test:
    try:
        message = client.messages.create(
            model=model,
            max_tokens=50,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✓✓✓ SUCCESS! Model works: {model}")
        print(f"    Response: {message.content[0].text}")
        print(f"\n*** USE THIS MODEL: {model} ***\n")
        break
    except Exception as e:
        error_str = str(e)
        if "404" in error_str or "not_found" in error_str:
            print(f"✗ Model not found: {model}")
        elif "401" in error_str or "authentication" in error_str.lower():
            print(f"✗ Auth error: {model} - Check API key")
        elif "403" in error_str or "forbidden" in error_str.lower():
            print(f"✗ Access denied: {model} - Check account permissions")
        else:
            print(f"✗ Error with {model}: {error_str[:100]}")

print("\n" + "="*60)
print("If ALL models failed, check:")
print("1. Console: https://console.anthropic.com/settings/plans")
print("2. Verify you have an active API plan")
print("3. Check if billing is set up")
print("="*60)