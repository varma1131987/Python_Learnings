# Filter emails ending with "@gmail.com"

# Input: emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com"]

# Task: list of only Gmail addresses.


# Input list of emails
emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com"]

# List comprehension to filter Gmail addresses
gmail_addresses = [email for email in emails if email.endswith("@gmail.com")]

print(gmail_addresses)


# Explanation:
# Input List:

# emails = ["a@gmail.com", "b@yahoo.com", "c@gmail.com"] is the input list of email addresses.
# Condition email.endswith("@gmail.com"):

# Filters the emails to include only those that end with @gmail.com.
# List Comprehension:

# Iterates over each email in the list and applies the condition.
# Output:

# Creates a new list containing only Gmail addresses.
# Output:
# This filters the input list to include only the Gmail addresses.