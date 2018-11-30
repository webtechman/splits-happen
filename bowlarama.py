"""
    This program takes a string that represents a bowling game score and displays game results
	Sample calls:
    bowlarama("XXXXXXXXXXXX")
    bowlarama("9-9-9-9-9-9-9-9-9-9-")
    bowlarama("5/5/5/5/5/5/5/5/5/5/5")
    bowlarama("X7/9-X-88/-6XXX81")
"""
bowlarama("5/5/5/5/5/5/5/5/5/5/5")

def bowlarama(score_string):
    """
    This process takes a string that represents a bowling game score and displays game results
	Sample call:
    bowlarama("XXXXXXXXXXXX")
    """
    display_program_header()
    is_score_string_valid = validate_input(score_string)
    if is_score_string_valid == False:
        #print('score_string can only contain one or more of "x/-123456789" and must be at least 10 in length, but not more the 12')
        return
    score_string_normalized_ary = normalize_data(score_string)
    score_numbers_ary = convert_strings_ary_to_numbers_ary(score_string_normalized_ary)
    frames_ary = convert_numbers_ary_to_frames_ary(score_numbers_ary)
    display_frames(frames_ary, score_string_normalized_ary)
    print("\nYour total score is %d"%(frames_ary[9]))
    

def display_program_header():
    """
    display_program_header can be customized to display custom messages to players.
	Sample call:
    display_program_header()
    """
    print("   ___  ____ _      ____   ___   ___  ___   __  ______ ")
    print("  / _ )/ __ \ | /| / / /  / _ | / _ \/ _ | /  |/  / _ |")
    print(" / _  / /_/ / |/ |/ / /__/ __ |/ , _/ __ |/ /|_/ / __ |")
    print("/____/\____/|__/|__/____/_/ |_/_/|_/_/ |_/_/  /_/_/ |_|")
    print("\n")


def validate_input(score_string):
    """
    validate length and content
    expecting: "score_string" to possibly contain "x", "/", "-", or digits 1-9
	expecting: "score_string" length to be shorter than 23 and longer than 19 with each "x" counted as 2
	The return value will be True or False
	Sample call:
	validate_input("X7/9-X-88/-6XXX8")
    """
    score_string = score_string.lower()
    score_string_valid_chars = "x/-123456789"
    total_frame_rolls = len(score_string) + score_string.count("x")
    if total_frame_rolls < 20 or total_frame_rolls > 26:
        return False
    valid_frames = all(c in score_string_valid_chars for c in score_string)
    if valid_frames == False:
        return False
    return True


def normalize_data(score_string):
    """
    A single "x" for a strike creates an abnormality compared to the other 2 part datasets.
	This process will correct the data abnormality and convert the dataset string to an array.
	The passed in value should be similar to:
    "X7/9-X-88/-6XXX81"
	The return value will be similar to:
	['x', '-', '7', '/', '9', '-', 'x', '-', '-', '8', '8', '/', '-', '6', 'x', '-', 'x', '-', 'x', '-', '8', '1']
	Sample call:
	normalize_data("X7/9-X-88/-6XXX81")
    """
    score_string = score_string.lower()
    score_string = score_string.replace("x","x-")
    frames_data = ""
    for x in score_string:
        frames_data = frames_data  + "," + x
    frames_data = frames_data.replace(",", "", 1)
    frames_array = frames_data.split(",")
    return frames_array


def convert_strings_ary_to_numbers_ary(score_string_normalized_ary):
    """
    This process converts an array of strings to an array of numbers to support number totals
	The passed in value should be similar to:
	['x', '-', '7', '/', '9', '-', 'x', '-', '-', '8', '8', '/', '-', '6', 'x', '-', 'x', '-', 'x', '-', '8', '1']
	The return value will be similar to:
	[10, 0, 7, 3, 9, 0, 10, 0, 0, 8, 8, 2, 0, 6, 10, 0, 10, 0, 10, 0, 8, 1]
	Sample call:
	score_numbers_ary = convert_strings_ary_to_numbers_ary(['x', '-', '7', '/', '9', '-', 'x', '-', '-', '8', '8', '/', '-', '6', 'x', '-', 'x', '-', 'x', '-', '8', '1'])
    """
    score_numbers_ary = []
    i = 0
    for t in score_string_normalized_ary:
        if t == "x":
            value = 10
        elif t == "-":
            value = 0
        elif t == "/":
            value = 10 - int(score_string_normalized_ary[i-1])
        else:
            value = int(t)
        score_numbers_ary.append(value)
        i = i + 1
    return score_numbers_ary


def convert_numbers_ary_to_frames_ary(score_numbers_ary):
    """
    This process converts an array of individual numbers into frame sets with running total.
	Sample call:
	convert_numbers_ary_to_frames_ary([10, 0, 7, 3, 9, 0, 10, 0, 0, 8, 8, 2, 0, 6, 10, 0, 10, 0, 10, 0, 8, 1])
	Sample return:
    [20, 39, 48, 66, 74, 84, 90, 120, 148, 167]
    """
    frames_ary = []
    game_total = 0
    i = 0
    f = 0
    for n in score_numbers_ary:
        if i >= 20:
            break
        roll1 = score_numbers_ary[i]
        roll2 = score_numbers_ary[i+1]
        temp_score = roll1 + roll2
        if temp_score == 10 and roll1 == 10:
            nextroll1 = score_numbers_ary[i+2]
            nextroll2 = score_numbers_ary[i+3]
            if nextroll1 == 10:
                nextroll2 = score_numbers_ary[i+4]
            game_total = game_total + temp_score + nextroll1 + nextroll2
        elif temp_score == 10 and roll1 != 10:
            nextroll1 = score_numbers_ary[i+2]
            game_total = game_total + temp_score + nextroll1
        else:
            game_total = game_total + temp_score
        frames_ary.append(game_total)
        i = i + 2
    return frames_ary


def display_frames(frames_ary, score_string_normalized_ary):
    """
	This process displays the game results.
	Sample call:
	display_frames([20, 39, 48, 66, 74, 84, 90, 120, 148, 167], ['x', '-', '7', '/', '9', '-', 'x', '-', '-', '8', '8', '/', '-', '6', 'x', '-', 'x', '-', 'x', '-', '8', '1'])
    Sample return:
    	   1   2   3   4   5   6   7    8    9    10
    Frame   X  7/  9-   X  -8  8/  -6    X    X    X
    Score  20  39  48  66  74  84  90  120  148  167
    """
    bowlarama = {}
    i = 1
    j = 0
    for s in frames_ary:
        game_frame = score_string_normalized_ary[j]
        if game_frame == "x":
            game_frame = "X"
        else:
            game_frame = game_frame + score_string_normalized_ary[j+1]
        bowlarama[i] = [game_frame, s]
        i = i + 1
        j = j + 2
    import pandas as pd
    frames = pd.DataFrame(bowlarama)
    frames.index = ["Frame", "Score"]
    print(frames)
	
