import openai
# from sk import my_sk
openai.api_key = "insert api key here"

response = openai.chat.completions.create(
    model= "gpt-4o-mini",
    messages= [
        {'role': 'system', 'content': 'You are a pro Clash Royale player'},
        {
            'role': 'user',
            'content': 'Give me a competitive 2v2 clash royale deck'
        }
    ]
)
print(response)