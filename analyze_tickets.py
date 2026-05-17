import anthropic
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def analyze_ticket(ticket_text, customer, subject):
    prompt = f"""Analyze this support ticket and respond with ONLY a JSON object (no markdown, no explanation):

Customer: {customer}
Subject: {subject}
Message: {ticket_text}

Return this exact format:
{{
    "urgency": "high" or "medium" or "low",
    "sentiment": "angry" or "frustrated" or "neutral" or "happy",
    "category": "billing" or "technical" or "account" or "feature_request",
    "suggested_team": "which team should handle this",
    "summary": "one sentence summary"
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    return json.loads(response_text)

df = pd.read_csv('tickets.csv')

print("Your CSV columns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\n" + "="*50 + "\n")

columns = df.columns.tolist()
id_col = customer_col = subject_col = message_col = None

for col in columns:
    col_lower = col.lower().strip()
    if 'id' in col_lower:
        id_col = col
    elif 'customer' in col_lower or 'name' in col_lower:
        customer_col = col
    elif 'subject' in col_lower or 'title' in col_lower:
        subject_col = col
    elif 'message' in col_lower or 'description' in col_lower or 'text' in col_lower:
        message_col = col

print("Analyzing tickets...\n")

for index, row in df.iterrows():
    ticket_id = row[id_col] if id_col else index + 1
    customer = row[customer_col] if customer_col else "Unknown"
    subject = row[subject_col] if subject_col else "No subject"
    message = row[message_col] if message_col else str(row.values[0])

    print(f"Ticket #{ticket_id} - {customer}")

    try:
        analysis = analyze_ticket(ticket_text=message, customer=customer, subject=subject)
        print(f"  Urgency:   {analysis['urgency']}")
        print(f"  Sentiment: {analysis['sentiment']}")
        print(f"  Category:  {analysis['category']}")
        print(f"  Team:      {analysis['suggested_team']}")
        print(f"  Summary:   {analysis['summary']}")
    except Exception as e:
        print(f"  Error analyzing: {e}")

    print()

print("Done!")