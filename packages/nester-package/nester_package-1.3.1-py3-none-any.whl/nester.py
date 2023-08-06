"""This is the "nester.py" module, and it provides one function called print_list_items()
 which prints lists that may or may not include nested lists."""


def print_list_items(the_list, indent=False, level=0):
    """This function takes a positional arguments called "the_list","indent" and "level", 'the_list' is
any Python list (of - possibly - nested lists). Each data item in the
provided list is (recursively) printed to the screen on it's own line.
A second argument 'indent' is set to default value 'False', which means indentation or tab-stops are not required
by-default. If user wants to add indentation while printing the nested list it should be set to 'True'.
A Third argument 'level' is used to insert required number of tab_stops when nested list is encountered."""

    for each_item in the_list:
        if isinstance(each_item, list):
            """Each time you process a nested list, you need to increase the value of level by 1. 
            Simply increment the value of level 1, each time you recursively invoke the function."""
            print_list_items(each_item, indent, level+1)
        else:
            if indent:
                """If indent=True, print the tab-stops. by-default it's set to False"""
                # for tab_stops in range(level):
                #   print("\t", end='')
                """Above for statement can also be written as..."""
                print("\t"*level, end='')
            print(each_item)

