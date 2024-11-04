from groq import Groq
from dotenv import load_dotenv
from storytime import main

story = main()
print(f"got this from main: ", story)

load_dotenv()
client = Groq()
completion = client.chat.completions.create(

    model="llama-3.2-90b-vision-preview",
    messages=[
        {
            "role": "system",
            "content": "You are F1GPT, given context about season outcomes, create an enthralling story detailing the four races that led to Lando winning the WDC. Also, talk about strategies and events."
        },
        {
            "role": "user",
            "content": story
        },
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message.content)
