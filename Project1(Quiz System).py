def main():
  
  # Sample quiz questions in a dictionary format
  questions = {
      "What is the capital of France?": {
          "answer": "Paris",
          "options": ["Paris", "London", "Berlin"],
          "difficulty": "easy"
      },
      "What is the tallest mountain in the world?": {
          "answer": "Mount Everest",
          "options": ["Mount Everest", "K2", "Kangchenjunga"],
          "difficulty": "medium"
      },
      "What is the equation for the area of a circle?": {
          "answer": "pi * r^2",
          "options": ["pi * r^2", "2 * pi * r", "pi * d"],
          "difficulty": "hard"
      },
  }

  user_performance = []  # Stores scores and difficulty for each attempt

  while True:
    # Choose difficulty level
    difficulty = input("Choose difficulty (easy, medium, hard, all): ").lower()

    
    filtered_questions = questions.copy()
    if difficulty != "all":
      filtered_questions = {q: details for q, details in questions.items() if details["difficulty"] == difficulty}

    # Initialize score and timer variables
    user_score = 0
    num_questions = len(filtered_questions)
    time_limit = 10  # Adjust time limit (in seconds) per question

    # Loop through each question
    for question, details in filtered_questions.items():
      print(f"\nQuestion: {question}")
      for option in details["options"]:
        print(f"{option}")

      # Timer for each question
      import time
      start_time = time.time()
      user_answer = input(f"Enter your answer within {time_limit} seconds: ").lower()
      elapsed_time = time.time() - start_time

      # Check answer and consider time penalty
      if user_answer == details["answer"].lower():
        if elapsed_time <= time_limit:
          print("Correct!")
          user_score += 1
        else:
          print(f"Correct, but time limit exceeded! (-1 point)")
      else:
        print(f"Incorrect. The correct answer is: {details['answer']}")

    # Calculate and display results
    percentage = (user_score / num_questions) * 100
    print(f"\nYour final score: {user_score} out of {num_questions} ({percentage:.2f}%)")

    # Track user performance
    user_performance.append({"difficulty": difficulty, "score": user_score})

    # Play again prompt with performance summary
    play_again = input("Play again? (y/n) or view performance (p): ").lower()
    if play_again == "n":
      break
    elif play_again == "p":
      print("\nYour performance history:")
      for attempt in user_performance:
        print(f"- Difficulty: {attempt['difficulty']}, Score: {attempt['score']}")

if __name__ == "__main__":
  main()
