from psychopy import visual, core, event, gui
import os
import random
# Create a window
win = visual.Window(size=(800, 600), color=(1, 1, 1), units="pix")

colors = ["blue", "green", "red"]

# Define button dimensions and positions
button_width = 100
button_height = 50
spacing = 20

# Define card dimensions and position
card_width = 200
card_height = 300
card_pos = (0, 0)

# Calculate the positions for the buttons in the bottom right corner
flip_button_pos = (win.size[0] / 2 - button_width / 2 - spacing, -win.size[1] / 2 + button_height / 2 + spacing)
dont_flip_button_pos = (
win.size[0] / 2 - 3 * button_width / 2 - 2 * spacing, -win.size[1] / 2 + button_height / 2 + spacing)

# Create the card
card = visual.Rect(win=win, width=card_width, height=card_height, fillColor=colors[0], lineColor=colors[0],
                   pos=card_pos)
cardlabel = visual.TextStim(win=win, pos=card_pos, color='white')

# Create the flip button
flip_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                          pos=flip_button_pos)
flip_label = visual.TextStim(win=win, text="flip", pos=flip_button_pos, color='white')

start_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                           pos=flip_button_pos)
start_label = visual.TextStim(win=win, text="Start", pos=flip_button_pos, color='white')

# Create the don't flip button
dont_flip_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                               pos=dont_flip_button_pos)
dont_flip_label = visual.TextStim(win=win, text="don't flip", pos=dont_flip_button_pos, color='white')

testtext = visual.TextStim(win=win, text="test", pos=(0, 0), color='black')
testblock = ("testowy napis wprowadzający", ("testowa karta 0", "testowa karta 1", "testowa karta 2"))


prompt_visual = visual.TextStim(win=win, text="", pos=(0, 0), color='black')
# Create a mouse object to detect clicks
mouse = event.Mouse(win=win)


def getinfo():  # popup to get identifier
    info = dict()
    info["identyfikator"] = ""
    info["wiek"] = ""
    info["płeć"] = ""
    dlg = gui.DlgFromDict(dictionary=info)
    if not dlg.OK:
        core.quit()
    data = (info["identyfikator"], info["wiek"], info["płeć"])
    return data


dane = getinfo()
print(dane[0])
print(dane[1])
print(dane[2])

os.makedirs(f'results/{dane[0]}')

file = open(f"results/{dane[0]}/{dane[0]}_data.txt", "w")
file.write("id,age,sex\n")
file.write(f"{dane[0]},{dane[1]},{dane[2]}\n")
file.close()


# Function to draw the card
def draw_card(text):
    card.fillColor = 'gray'
    card.lineColor = "gray"
    cardlabel.text = text
    card.draw()
    cardlabel.draw()

# Create the space prompt
space_prompt = visual.TextStim(win=win, text="Press space to continue", pos=(0, -200), color='black')


# Function to draw the buttons and labels
def draw_buttons():
    flip_button.draw()
    flip_label.draw()
    dont_flip_button.draw()
    dont_flip_label.draw()


# Initial draw
# Initial draw
def cardset(tfile):
    mpressed = False
    n = 0
    cumCorrect = 0

    # Open the testcards.txt file and read the prompts
    textfile = open(f"{tfile}.txt", "r")
    textlist = textfile.readlines()[1:]
    textfile.close()
    textlist = [line.strip().split(',') for line in textlist]
    print(textlist)

    # Open the prompts.txt file and read the prompts
    with open("prompts.txt", "r") as promptfile:
        promptlist = promptfile.readlines()[1:]
        promptlist = [line.strip().split(',') for line in promptlist]
        print(promptlist)

    # Only create a result file if tfile is not 'testcards'
    if tfile != 'testcards':
        os.makedirs(f'results/{dane[0]}', exist_ok=True)
        resultfile = open(f"results/{dane[0]}/{dane[0]}_result.txt", "a")  # Changed here
    else:
        resultfile = None

    last_set = None
    while n < len(textlist):
        current_set = textlist[n][2]

        # Find the matching prompt for the current set
        matching_prompt = next((prompt for prompt in promptlist if prompt[1] == current_set), None)
        if matching_prompt and current_set != last_set:
            # Display the prompt and wait for a space press
            prompt_visual.text = matching_prompt[0]
            prompt_visual.draw()
            space_prompt.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            last_set = current_set

        draw_card(textlist[n][0])
        draw_buttons()
        win.flip()
        start_time = core.getTime()  # Record the time the card is displayed

        response_made = False
        while not response_made:

            if mouse.isPressedIn(flip_button):
                reaction_time = (core.getTime() - start_time) * 1000  # Calculate reaction time in milliseconds
                correct = 1 if textlist[n][1] == 'f' else 0  # Check if the response is correct
                cumCorrect += correct  # Add the correct response to the cumulative correct responses
                if resultfile is not None:
                    resultfile.write(
                        f"{n + 1},{textlist[n][2]},Flipped,{reaction_time:.2f},{correct},{cumCorrect}\n")
                response_made = True
            elif mouse.isPressedIn(dont_flip_button):
                reaction_time = (core.getTime() - start_time) * 1000  # Calculate reaction time in milliseconds
                correct = 1 if textlist[n][1] == 'd' else 0  # Check if the response is correct
                cumCorrect += correct  # Add the correct response to the cumulative correct responses
                if resultfile is not None:
                    resultfile.write(
                        f"{n + 1},{textlist[n][2]},Not Flipped,{reaction_time:.2f},{correct},{cumCorrect}\n")
                response_made = True
            elif (core.getTime() - start_time) > 4:  # If 4 seconds have passed
                if resultfile is not None:
                    resultfile.write(
                        f"{n + 1},{textlist[n][2]},No Response,0,0,{cumCorrect}\n")  # Register no response
                response_made = True

            # After a response is made, display the space prompt and wait for a space press
            if response_made:
                space_prompt.draw()
                win.flip()
                event.waitKeys(keyList=['space'])

            # Check for quit (the Esc key)
            if event.getKeys(keyList=["escape"]):
                if resultfile is not None:
                    resultfile.close()
                win.close()
                core.quit()

        # Ensure button is released before proceeding
        while mouse.isPressedIn(flip_button) or mouse.isPressedIn(dont_flip_button):
            pass

        n += 1

    if resultfile is not None:
        resultfile.close()


def chooseCardset(m, n):
    # Open the cards.txt file and read the cards
    with open("cards.txt", "r") as textfile:
        textlist = textfile.readlines()[1:]
        textlist = [line.strip().split(',') for line in textlist]
        textlist = [card for card in textlist if m <= int(card[2]) <= n]  # Filter cards for the current set

    # Group cards by set
    sets = {}
    for card in textlist:
        if card[2] not in sets:
            sets[card[2]] = []
        sets[card[2]].append(card)

    # Randomly choose all sets from m to n and shuffle them
    chosen_sets = list(sets.keys())
    random.shuffle(chosen_sets)

    # For each set, randomly choose 5 cards
    chosen_cards = []
    for set in chosen_sets:
        chosen_cards.extend(random.sample(sets[set], 5))

    # Create a temporary file and write the chosen cards
    with open("temp.txt", "w") as temp_file:
        temp_file.write("cardText, flip, set\n")
        for card in chosen_cards:
            temp_file.write(",".join(card) + "\n")

    # Call the cardset function with the temporary file
    cardset("temp")

    # Remove the temporary file
    os.remove("temp.txt")


def display_intro():
    # Open the intro.txt file and read the introduction text
    introfile = open("intro.txt", "r")
    introtext = introfile.read().strip()
    introfile.close()

    # Display the introduction text
    introvisual = visual.TextStim(win=win, text=introtext, pos=(0, 0), color='black')
    introvisual.draw()
    start_button.draw()
    start_label.draw()
    win.flip()

    # Wait for a button press
    while True:
        if mouse.isPressedIn(start_button):
            while mouse.isPressedIn(start_button):
                pass
            break


display_intro()
# Main loop
cardset("testcards")

chooseCardset(1, 14)
chooseCardset(15, 29)
chooseCardset(30, 44)

# Close the window
win.close()

# Exit PsychoPy
core.quit()