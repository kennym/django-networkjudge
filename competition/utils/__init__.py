import re

def are_equal(problem_output, solution_output):
    """
    Compare the outputs of two string objects.

     - Ignore case
     - Ignore white space
     - Ignore blank lines
    """
    problem_output = re.sub("\s", "", problem_output.lower())
    solution_output = re.sub("\s", "", solution_output.lower())

    if problem_output == solution_output:
        return True
    return False

