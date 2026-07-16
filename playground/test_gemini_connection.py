import os
from dotenv import load_dotenv
from google import genai

def test_gemini():
    # Cargar variables de entorno del archivo .env
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: No se encontró GEMINI_API_KEY en el entorno.")
        return

    try:
        print("Inicializando cliente de Gemini...")
        client = genai.Client(api_key=api_key)
        
        print("Enviando mensaje de prueba a gemini-3.5-flash...\n")
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents='Responde únicamente con un breve y amigable saludo de bienvenida de un sistema de IA industrial listo para ayudar.'
        )
        
        print("--- Respuesta de Gemini ---")
        print(response.text.strip())
        print("---------------------------")
        print("\n✅ ¡Conexión con la API de Gemini exitosa!")
    except Exception as e:
        print(f"\n❌ Error al conectar con Gemini: {e}")

if __name__ == "__main__":
    test_gemini()
