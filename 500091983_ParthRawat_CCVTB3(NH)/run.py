import basic as ba

# Specify the file path
file_path = "LEXSAMPLE.txt"

# Initialize an empty list to store the lines from the file
lines = []

try:
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Append the line to the list, removing the newline character
            lines.append(line.strip())

    # Print the lines or perform any further processing
    for text in lines:
        print(text)

        result, error = ba.run('<stdin>', text)

        if error:
            print(error.as_string())
        else:
            print(result)

except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")