import nltk
from transformers import AutoModelForCausalLM, AutoTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from translator import translate_input,translate_output

class ChatbotAI:

    def __init__(self):

        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
        nltk.download('punkt_tab')

        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def preprocess_text(self, text): #tokenize text
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        return " ".join(lemmatized_tokens)
    
    def multilingual_chatbot_response(self, user_input, user_language='en'):
        translated_input = translate_input(user_input, target_language='en')
        sentiment = self.analyze_sentiment(translated_input)
        response = self.chatbot_ai_response(translated_input)

        if sentiment == "positive":
            return f"{translate_output(response, target_language=user_language)}, It's great to see you're feeling positive!"
        elif sentiment == "negative":
            return f"{translate_output(response, target_language=user_language)}, I'm here to help if you're feeling down."
        return translate_output(response, target_language=user_language)
    
    def analyze_sentiment(self, user_input):
        sentiment = TextBlob(user_input).sentiment.polarity
        if sentiment > 0.5:
            return "positive"
        elif sentiment < -0.5:
            return "negative"
        else:
            return "neutral"


    def chatbot_ai_response(self, context): #generate ai respond
        inputs = self.tokenizer.encode(context + self.tokenizer.eos_token, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=100, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
        return response