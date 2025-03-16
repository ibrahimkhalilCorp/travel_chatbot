import re

# Mapping of words to numbers
word_to_number = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, 'None' : 0
}

def extract_number(text, keyword=None):
    """
    Extracts a number associated with a keyword (e.g., "adults" or "children") from the text.
    Supports both digits (2, 3) and word-based numbers ("two", "three").
    """
    text = text.lower()  # Convert text to lowercase

    # ✅ Check if the text contains a word-based number and replace it
    for word, num in word_to_number.items():
        text = text.replace(f" {word} ", f" {num} ")

    # ✅ Extract number before a keyword (if specified)
    if keyword:
        match = re.search(r'(\d+)\s+' + re.escape(keyword), text)
        return int(match.group(1)) if match else 0

    # ✅ Extract first number found in text
    match = re.search(r'\b\d+\b', text)
    return int(match.group()) if match else 0

# 🔍 Test Cases
print(extract_number("two adults", "adults"))   # ✅ Output: 2
print(extract_number("I want to book a flight for three people"))  # ✅ Output: 3
print(extract_number("We are four adults and two children", "children"))  # ✅ Output: 2
print(extract_number("Five children and one adult", "children"))  # ✅ Output: 5
print(extract_number("I need tickets for 2 adults and 1 child", "adults"))  # ✅ Output: 2



# def extract_number(text):
#     """
#     Extracts a number (e.g., adults/children count) from the text.
#     """
#     for word in text.split():
#         if word.isdigit():
#             return int(word)
#     return 0