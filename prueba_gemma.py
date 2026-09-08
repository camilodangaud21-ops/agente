from ollama import chat

response = chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": "Hola. Responde únicamente con: conexión exitosa."
        }
    ]
)

print(response.message.content)