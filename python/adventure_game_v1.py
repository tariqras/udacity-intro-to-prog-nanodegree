# intro to programming nanodegree
# project:adventure game  tariq rashid

import time
import random

SHORT_DELAY = 1.5
LONG_DELAY = 4


def print_pause(msg, delay):
    print(msg)
    time.sleep(delay)


def intro():

    print("=================================================")
    print_pause("A violent earthquake has just ended.", SHORT_DELAY)
    print_pause("You are sitting in a vehicle stopped at a crossroads."
                "\n", SHORT_DELAY)
    print("Your partner Claudia, who is driving, says,\n")
    print_pause('"We\'d better get going...'
                'We need to get north to Nothyp.', SHORT_DELAY)
    print_pause('Maybe we will find some useful cargo '
                'on the way.', SHORT_DELAY)
    print_pause('Nothyp urgently needs medicine and critical components.',
                SHORT_DELAY)
    print_pause('But protective shielding may alse be useful."\n', LONG_DELAY)
    print("=================================================")


def at_crossroads(items):

    routes = ["(n)Main Road", "(e)Ravenholm", "(w)Mirkwood bypass"]

    print_pause("You are at a crossroads, there isn't much here.", SHORT_DELAY)
    print_pause("The road south is blocked by a wide chasm.\n", SHORT_DELAY)

    show_status(items)

    drive(items, routes)


def at_main_road(items):

    routes = ["(n)Nothyp", "(s)Crossroads"]

    print_pause("You are on the Nothyp-Crossroads highway.",
                SHORT_DELAY)
    print_pause("The road appears mostly undamaged.\n",
                SHORT_DELAY)

    # Determine if a bridge shifts causing some item to be lost with d10
    if random.random() <= 0.5:
        print_pause("A bridge shifts while you are crossing it.", SHORT_DELAY)
        if items:
            lost_item = items.pop()
            print_pause(f"Some {lost_item} fall in to a river!", SHORT_DELAY)

    show_status(items)

    drive(items, routes)


def at_mirkwood_bypass(items):

    routes = ["(e)Nothyp", "(s)Crossroads"]

    print_pause("You reached Mirkwood bypass.", SHORT_DELAY)
    print_pause("You are on a road that runs through a dense forest.",
                SHORT_DELAY)
    print_pause("There are signs of a recent storm.\n", SHORT_DELAY)

    check_for_hazard(items, 0.4)  # check for danger

    find_random_map_item(items, 0.4)  # check for goodies

    show_status(items)

    drive(items, routes)


def at_ravenholm(items):

    routes = ["(w)Crossroads"]

    print_pause("You are in Ravenholm.", SHORT_DELAY)
    print_pause("You drive slowly through an abandoned "
                "warehouse district.", SHORT_DELAY)
    print_pause("The road does not lead anywhere beyond this area.",
                SHORT_DELAY)
    print_pause("You hear a stange, ominous buzzing sound...\n", SHORT_DELAY)

    find_random_map_item(items, 0.6)

    check_for_hazard(items, 0.7)  # Ravenholm is dangerous

    print_pause("You continue exploring.", SHORT_DELAY)
    find_random_map_item(items, 0.4)  # But there are many useful items here

    show_status(items)

    drive(items, routes)


def at_nothyp(items):

    routes = ["(s)Main Road", "(w)Mirkwood Bypass"]

    print_pause("You made it to Nothyp!", SHORT_DELAY)
    print_pause("The earthquake has caused major damage.\n", SHORT_DELAY)

    show_status(items)

    if items:
        if "medicine" in items:
            print_pause("The medical team thanks you profusely "
                        "for the medicine!\n", SHORT_DELAY)

        if "critical components" in items:
            print_pause("The engineering team can use these critical "
                        "components to repair the Nothyp power station!\n",
                        SHORT_DELAY)

        if "protective shielding" in items:
            print_pause("This protective shielding will be useful against "
                        "manna storms!\n", SHORT_DELAY)

        print_pause("Your cargo will be a great help!\n", SHORT_DELAY)
        print_pause("Great work!", SHORT_DELAY)

        play_again()

    else:
        print_pause("You failed to deliver any useful cargo!", SHORT_DELAY)
        print_pause("Conditions will deteriorate quickly without aid.\n",
                    SHORT_DELAY)
        print_pause("You must go back and find some useful cargo!\n",
                    LONG_DELAY)

        drive(items, routes)


def check_cargo(items):

    if not items:
        print_pause('Claudia says, "We don\'t have any useful cargo.\n'
                    'Maybe we can find some in Ravenholm or Mirkwood"\n', 0.5)


def drive(items, routes):

    available_directions = []
    direction = ""

    check_cargo(items)

    print_pause("You can choose one of the following directions:",
                SHORT_DELAY)
    for route in routes:
        print_pause(route, 0.5)
        available_directions.append(route[1].lower())

    if items:
        print('\nClaudia says, "We have to get to Nothyp"')

    while not is_valid_response(direction, available_directions):
        print("Enter one of the following letters to choose a direction:")
        for d in available_directions:
            print(d + " ", end="")

        direction = input("\nChoose an available direction:\n").lower()

        print("You chose " + direction.lower())

    selection_index = available_directions.index(direction)

    print_pause("\n=================================================",
                SHORT_DELAY)

    if "crossroads" in routes[selection_index].lower():
        at_crossroads(items)

    elif "main road" in routes[selection_index].lower():
        at_main_road(items)

    elif "ravenholm" in routes[selection_index].lower():
        at_ravenholm(items)

    elif "mirkwood bypass" in routes[selection_index].lower():
        at_mirkwood_bypass(items)

    elif "nothyp" in routes[selection_index].lower():
        at_nothyp(items)


def show_status(items):

    print_pause("------------------------------------------------",
                SHORT_DELAY)
    if items:
        print_pause("Your cargo includes:", 0.5)
        for item in items:
            print_pause(item, 0.5)
    else:
        print_pause("You have no cargo.", SHORT_DELAY)
    print("------------------------------------------------")


def check_for_hazard(items, probability):

    hazards = ['manna storm', 'deranged renegade']

    if random.random() <= probability:  # check for a hazard

        hazard_name = random.choice(hazards)

        print_pause("------------------------------------------------",
                    SHORT_DELAY)
        print_pause(f"A {hazard_name} blocks your path!!!", SHORT_DELAY)
        print_pause(f"After a short while, the {hazard_name} moves away.",
                    SHORT_DELAY)

        if "protective shielding" in items:
            print_pause("You were not harmed due to your protective shielding."
                        "\n", SHORT_DELAY)
            if random.random() <= 0.5:  # check for damage to the item
                print_pause("Your protective shielding was damaged and "
                            "is no longer useful.\n", SHORT_DELAY)
                items.remove("protective shielding")

        elif items:  # The hazard removes an item from cargo

            lost_item = random.choice(items)
            items.remove(lost_item)
            print_pause("You notice that you are missing a load of "
                        f"{lost_item}!\n", SHORT_DELAY)

        else:

            print_pause(f"The {hazard_name} was a little frightening.\n",
                        SHORT_DELAY)


def find_random_map_item(items, probability):

    if random.random() <= probability:  # check for items
        print_pause("------------------------------------------------",
                    SHORT_DELAY)
        new_item = get_random_item()
        print_pause(f"You found some {new_item}!", SHORT_DELAY)
        items.append(new_item)
        print_pause("You load it into your vehicle.\n", SHORT_DELAY)


def get_random_item():

    map_items = ['medicine', 'critical components', 'protective shielding']

    return random.choice(map_items)


def show_routes(routes):
    print_pause("There is a road sign showing available routes:", SHORT_DELAY)
    for route in routes:
        print_pause(route, SHORT_DELAY)
    print("")


def is_valid_response(response, valid_respones):

    return response in valid_respones


def play_again():
    # See if the players wants some more
    play_again = input("Would you like to play again? (enter y or n):\n")

    while not is_valid_response(play_again, ["y", "n"]):
        play_again = input("Please enter y or n:\n")

    if play_again == 'y':
        print_pause("\n\n\n", SHORT_DELAY)
        play_game()

    else:
        print_pause("Goodbye!\n", SHORT_DELAY)


def play_game():

    items = []
    intro()
    at_crossroads(items)


play_game()
