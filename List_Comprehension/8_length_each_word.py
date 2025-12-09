# Length of each word

# Input: words = ["apple", "banana", "kiwi"]

# Task: ["apple:5", "banana:6", "kiwi:4"] using f-strings + comprehension.# Input list of words
words = ["apple", "banana", "kiwi"]

# List comprehension with f-strings
word_lengths = [f"{word}:{len(word)}" for word in words]

print(word_lengths)


# Explanation:
# Input List:

# words = ["apple", "banana", "kiwi"] is the input list of words.
# List Comprehension:

# Iterates over each word in the list.

# Uses len(word) to calculate the length of each word.
# f-Strings:

# Formats each word and its length as word:length.
# Output:

# Combines the word and its length into the desired format.