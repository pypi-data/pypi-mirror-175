"""This is the "nester.py" module, and it provides one function called print_list_items()
 which prints lists that may or may not include nested lists."""


def print_list_items(the_list, level):
    """This function takes a positional argument called "the_list", which
     is any Python list (of - possibly - nested lists). Each data item in the
     provided list is (recursively) printed to the screen on it's own line.
     A second argument 'level' is used to insert tab_stops when nested list is encountered"""

    for each_item in the_list:
        if isinstance(each_item, list):
            """Each time you process a nested list, you need to increase the value of level by 1. 
            Simply increment the value of level 1, each time you recursively invoke the function.S"""
            print_list_items(each_item, level+1)
        else:
            for tab_stops in range(level):
                print("\t", end='')
            print(each_item)
