from read_data import view_mesh


def yes_or_no(question):
    reply = str(input(question + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


again = True

while again:
    again = False
    path = input("Please enter the path of the mesh you want to visualize: ")
    view_mesh(path)
    print("A window opened with the visualisation of mesh " + path)
    again = yes_or_no("Do you want to visualize another mesh?")
