import google.generativeai as genai

from resources.constants import gemeni_private_key

def test():
    genai.configure(api_key=gemeni_private_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Explain how AI works")
    print(response.text)