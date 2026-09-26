import os
from dotenv import load_dotenv
from groq import Groq

from rag import retrieve_relevant_context


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


query = (
    "AWS Networking: An EC2 instance in a private subnet "
    "cannot access the internet. The route table has been "
    "configured, but internet connectivity is still unavailable."
)

print("1. Starting RAG retrieval...")

retrieved_results = retrieve_relevant_context(
    query,
    top_k=4
)

print("2. RAG retrieval completed.")

retrieved_context = "\n\n".join(
    result["content"]
    for result in retrieved_results
)

prompt = f"""
You are a professional network troubleshooting assistant.

Device or Technology:
AWS Networking

Network Problem:
An EC2 instance in a private subnet cannot access the internet.
The route table has been configured, but internet connectivity
is still unavailable.

Retrieved Knowledge Base Context:
{retrieved_context}

Use the retrieved knowledge-base context when it is relevant
to the reported problem.

If the retrieved context does not contain enough information
to completely troubleshoot the issue, you may supplement it
with your general networking knowledge.

Do not invent command outputs or claim that a command was executed.

Analyze the network problem and provide the response using
the following structure:

1. Problem Analysis
2. Possible Causes
3. Step-by-Step Troubleshooting Procedure
4. Relevant Commands or Checks
5. Recommended Solution
6. Additional Verification

Keep the response practical, technically accurate,
structured, and easy to understand.
"""

print(f"3. Prompt length: {len(prompt)} characters")
print(f"4. Retrieved chunks: {len(retrieved_results)}")
print("5. Sending request to Groq...")

try:

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("6. Groq response received.\n")

    print(
        response.choices[0]
        .message.content
    )

except Exception as e:

    print("\nGroq request failed:")
    print(e)