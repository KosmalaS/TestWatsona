from psychopy import visual, core, event, gui, monitors
import os
import random


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

m1 = monitors.getAllMonitors()
mon = monitors.Monitor(m1[0])  # Adjust the monitor name as needed
screen_size = mon.getSizePix()

# Create a window
win = visual.Window(
    size=screen_size,
    fullscr=True,
    screen=0,
    monitor="testMonitor",  # Use the retrieved monitor
    color=[1, 1, 1],  # Background color (black in this case)
    units="height"  # Use pixel units
)

colors = ["blue", "green", "red"]

# Define button dimensions and positions
button_width = 0.2
button_height = 0.1
spacing = 0.04

# Define card dimensions and position
card_width = 0.8
card_height = 0.6
card_pos = (0, 0)

# Calculate the positions for the buttons in the bottom right corner
flip_button_pos = (0.5 - button_width / 2 - spacing, -0.5 + button_height / 2 + spacing)
dont_flip_button_pos = (0.5 - 1.5 * button_width - 2 * spacing, -0.5 + button_height / 2 + spacing)

# Create the card
card = visual.Rect(win=win, width=card_width, height=card_height, fillColor=colors[0], lineColor=colors[0],
                   pos=card_pos)
cardlabel = visual.TextStim(win=win, pos=card_pos, color='white', height=0.05)

# Create the flip button
flip_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                          pos=flip_button_pos)
flip_label = visual.TextStim(win=win, text="Odwroc", pos=flip_button_pos, color='white', height=0.02)

start_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                           pos=flip_button_pos)
start_label = visual.TextStim(win=win, text="Start", pos=flip_button_pos, color='white', height=0.02)

next_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                           pos=flip_button_pos)
next_label = visual.TextStim(win=win, text="Next", pos=flip_button_pos, color='white', height=0.02)

# Create the don't flip button
dont_flip_button = visual.Rect(win=win, width=button_width, height=button_height, fillColor='blue', lineColor='blue',
                               pos=dont_flip_button_pos)
dont_flip_label = visual.TextStim(win=win, text="Nie odwracaj", pos=dont_flip_button_pos, color='white', height=0.02)

testtext = visual.TextStim(win=win, text="test", pos=(0, 0), color='black')
testblock = ("testowy napis wprowadzający", ("testowa karta 0", "testowa karta 1", "testowa karta 2"))

prompt_visual = visual.TextStim(win=win, text="", pos=(0, 0), color='black', height=0.075)
# Create a mouse object to detect clicks
mouse = event.Mouse(win=win)


# Function to draw the card
def draw_card(text):
    card.fillColor = 'gray'
    card.lineColor = "gray"
    cardlabel.text = text
    card.draw()
    cardlabel.draw()


# Create the space prompt
space_prompt = visual.TextStim(win=win, text="Wcisnij spacje by kontynuowac", pos=(0, -0.4), color='black', height=0.06)


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


def display_intro(pth):
    # Open the intro.txt file and read the introduction text
    introfile = open(pth, "r")
    introtext = introfile.read().strip()
    introfile.close()

    # Display the introduction text
    introvisual = visual.TextStim(win=win, text=introtext, pos=(0, 0), color='black', height=0.025)
    introvisual.draw()

    # Check which file is being displayed and show the appropriate button
    if pth == "intro_eksperyment_1.txt":
        next_button.draw()
        next_label.draw()
    else:
        start_button.draw()
        start_label.draw()

    win.flip()

    # Wait for a button press
    while True:
        if pth == "intro_eksperyment_1.txt" and mouse.isPressedIn(next_button):
            while mouse.isPressedIn(next_button):
                pass
            break
        elif mouse.isPressedIn(start_button):
            while mouse.isPressedIn(start_button):
                pass
            break


display_intro("intro.txt")
# Main loop
cardset("testcards")
display_intro("intro_eksperyment_1.txt")
display_intro("intro_eksperyment_2.txt")
chooseCardset(1, 14)
chooseCardset(15, 29)
chooseCardset(30, 44)

# Close the window
win.close()

# Exit PsychoPy
core.quit()
