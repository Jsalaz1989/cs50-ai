import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, words in self.domains.items():
            for word in words.copy():
                if len(word) != variable.length: self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        print(f'Revising variables {x=} and {y=}')
        revised = False
        # print(f'{self.domains=}')
        # print(f'{self.crossword.overlaps=}')
        try:                overlap = self.crossword.overlaps[(x,y)]
        except KeyError:    overlap = None
        # print(f'{overlap=}')

        if overlap:
            print(f'{self.domains[y]=}')
            for x_word in self.domains[x].copy():
                print(f'{x_word=}')
                if not any([x_word[overlap[0]] == y_word[overlap[1]] for y_word in self.domains[y]]):                    
                    print(f'Inconsistent arc between {x_word[overlap[0]]=} and {self.domains[y]=} at {overlap[1]=}. Removing {x_word} from x.domain...')
                    self.domains[x].remove(x_word)
                    revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # queue = arcs if arcs else [(x,y) for x in self.domains for y in self.domains if x != y]
        queue = arcs if arcs else [(x,y) for x in self.domains for y in self.crossword.neighbors(x)]
        while queue:
            (x, y) = queue.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains)
        # return all([value is not None for value in assigment.values()])

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(assignment.values()) != len(set(assignment.values())): return False
        if not all([var.length == len(val) for var, val in assignment.items() if type(val) == str]): return False
        
        for x in self.domains:
            for y in self.crossword.neighbors(x):
                if self.revise(x,y): return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return [val for val in self.domains[var]]

        # num_eliminated = dict()
        # neighbors = self.crossword.neighbors(var)
        # if var not in assignment:
        #     for neighbor in neighbors:
        #         overlap = self.crossword.overlaps[(var,neighbor)]
        #         for val in self.domains[var]:
        #             num_eliminated[val] = 0
        #             for val_neighbor in self.domains[neighbor]:
        #                 if val[overlap[0]] != val_neighbor[overlap[1]]: 
        #                     num_eliminated[val] += 1 
        # # return sorted([val for val in num_eliminated.values()], key=lambda x: abs(0.5 - x[1]), reverse=True))
        # return [v for k,v in sorted(num_eliminated.items(), key=lambda item: item[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # return [var for var in self.domains if var not in assignment][0]

        unassigned_vars = {
            var: {'remaining':len(self.domains[var]), 'degree':len(self.crossword.neighbors(var))} 
            for var in self.domains if var not in assignment
        }

        min_remaining = min([rem_deg['remaining'] for var,rem_deg in unassigned_vars.items()])
        min_remaining_vars = [var for var, rem_deg in unassigned_vars.items() if rem_deg['remaining'] == min_remaining]
        if len(min_remaining_vars) == 1: 
            return min_remaining_vars[0]
        else:
            max_degree = max([rem_deg['degree'] for var, rem_deg in unassigned_vars.items()])
            max_degree_vars = [var for var, rem_deg in unassigned_vars.items() if rem_deg['degree'] == max_degree]
            return max_degree_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment): return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = val
                result = self.backtrack(assignment)
                if result: return result
            try:                del assignment[var]
            except KeyError:    pass
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
