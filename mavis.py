import os
from PIL import Image
import google.generativeai as genai


class MavisAI:
    def __init__(self, api_key: str = "AIzaSyAfK2sEYxnluVqRacyCdccPH1hKZseqlA0", model_name: str = 'gemini-2.0-flash-lite', answer_length: int = 2):
        self.api_key = api_key
        self.model_name = model_name
        self.answer_length = answer_length

        # Set up Gemini configuration
        os.environ["GOOGLE_API_KEY"] = self.api_key
        genai.configure(api_key=self.api_key)

        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)

    def ask(self, image_path: str, custom_question: str = None) -> str:
        try:
            # Load the image
            image = Image.open(image_path)

            # Define question
            if custom_question is None:
                question = f"Answer the question in the image in {self.answer_length} lines."
            else:
                question = custom_question

            # Generate the response
            response = self.model.generate_content([question, image])
            print("\n")
            print(response.text)
            print("\n")
            return response.text

        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == '__main__':
    # Replace with your actual image and key
    # api_key = "AIzaSyAfK2sEYxnluVqRacyCdccPH1hKZseqlA0"
    image_path = "img_to_ask.png"

    mavis = MavisAI()
    result = mavis.ask(image_path)
    print("Response:\n", result)
