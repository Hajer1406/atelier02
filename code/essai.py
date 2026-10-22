import os
from groq import Groq
client = Groq(api_key=os.environ["GROQ_API_KEY"])
reponse = client.chat.completions.create(
 model="openai/gpt-oss-20b",
 messages=[{"role": "user", "content": "Réponds : OK"}])
print(reponse.choices[0].message.content)