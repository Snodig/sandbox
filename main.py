#! python3

'''
 * Date: 17-02-28
 * Desc: The entry-point of our program
 * Author: Collaboration
'''

# This is how python pulls in other modules (from other *.py-files)
import time
import traceback
from sys import argv

# from module (file) import <class|function|*>
from RadicalGame import Game


def main():
    # This is the entry-point of the program, and is the first function called.
    # This is not required by python, but it helps create understanding of other languages that require you to
    # define the function 'main', which is always called by the runtime when entering a program.
    # Scripting-languages are usually less strict than compiled languages with such semantics.
    try:
        t0 = time.localtime()
        print("Start of " + argv[0])
        ourGame = Game()  # Initialize the variable 'ourGame' with an instance of the Game class, by calling it's c'tor.
        ourGame.start()  # Start our infinite loop

    # Try-except (or try-catch) is also called exception-handling.
    # If an exception is 'thrown' inside the scope of our try-block, we 'catch' it in our except-block.
    # In this case, we only catch KeyboardInterrupt-type exceptions (ctrl+c)
    except KeyboardInterrupt:
        print("\n-- Ctrl^C ---")

    # Here we catch all exception not explicitly handled by other except-clauses.
    # For any except-clause, we could also access an exception-object (the one that was thrown), but I didn't feel like it.
    except:
        print("\n")
        traceback.print_exc()

    # Finally-clauses are entered after the try-block and the except-block (if any).
    finally:
        print("\nTime is now   " + time.strftime("%H:%M:%S"))
        totalTime = time.mktime(time.localtime()) - time.mktime(t0)
        print("Running since ", time.strftime("%H:%M:%S", t0), "(", totalTime, "seconds )")


if __name__ == "__main__":
    # This if-statement is actually the "first" line executed in our program.
    # All code before this just defines classes and functions, and imports other modules.
    # Since the C-runtime is used to run the python-interpreter, the concept of 'main' is found in the (magic) __name__ variable.
    # https://docs.python.org/3/library/__main__.html
    exit(main())
