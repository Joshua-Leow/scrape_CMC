import google.generativeai as genai

from resources.constants import gemeni_private_key


def gen_ai(result):
    prompt = ("You are a business development representative at Coinstore. \n"
              "Your role is to work with crypto startups to list their digital currency on Coinstore's exchange. \n"
              "Now, write for me a casual personalised pitch to this startup, attracting them to the benefits of listing their digital currency on our exchange. \n"
              "\n"
              f"Crypto Name (Symbol): {result[0]}\n"
              f"Related tags: {result[1]}\n"
              f"CEX and DEX listed [volume %]: {result[2]}\n"
              f"CEX listed: {result[3]}\n"
              f"About the business: {result[10]}\n")

    genai.configure(api_key=gemeni_private_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

