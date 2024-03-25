import random
class Chatbot:
    def __init__(self, greeting="Hi there!"):
        self.greeting = greeting
        self.responses = {
            "hello": ["Hi! How can I help you today?", "Hey there! What's on your mind?"],
            "how are you": ["I'm doing well, thanks for asking! How about you?"],
            "goodbye": ["Bye! Have a great day!", "See you later!"],
            "default": ["Sorry, I didn't quite understand that. Can you rephrase?"]
        }

    def greet(self):
        print(self.greeting)

    def get_response(self, user_input):
        # Lowercase user input for case-insensitive matching
        user_input = user_input.lower()

        if user_input in self.responses:
            # Choose a random response from the list for variety
            return random.choice(self.responses[user_input])
        else:
            return self.responses["default"]


def main():
    
    # Create a Chatbot object
    chatbot = Chatbot()

    # Greet the user
    chatbot.greet()

    while True:
        # Get user input
        user_input = input("You: ")

        # Exit if user types 'quit'
        if user_input.lower() == "quit":
            break

        # Get chatbot response and print it
        response = chatbot.get_response(user_input)
        print("Chatbot:", response)


if __name__ == "__main__":
    main()
