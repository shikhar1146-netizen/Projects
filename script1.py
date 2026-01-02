import random

# List of words
words = ["python", "developer", "programming", "computer", "analytics", "machine", "learning"]

# Select a random word
secret_word = random.choice(words)
guessed_letters = []
attempts = 6

print("🎯 Welcome to Hangman Game")
print("Guess the word letter by letter")
print("_ " * len(secret_word))

while attempts > 0:
    guess = input("\nEnter a letter: ").lower()

    # Validation
    if len(guess) != 1 or not guess.isalpha():
        print("❌ Please enter a single alphabet letter.")
        continue

    if guess in guessed_letters:
        print("⚠️ You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess in secret_word:
        print("✅ Correct guess!")
    else:
        attempts -= 1
        print(f"❌ Wrong guess! Attempts left: {attempts}")

    # Display word progress
    display_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    print(display_word)

    # Win condition
    if "_" not in display_word:
        print("\n🎉 Congratulations! You guessed the word correctly.")
        break

# Lose condition
if attempts == 0:
    print("\n💀 Game Over!")
    print(f"The correct word was: {secret_word}")

