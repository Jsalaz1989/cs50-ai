# decorater used to block function printing to the console
def blockPrinting(func):

    import os
    import contextlib

    def func_wrapper(*args, **kwargs):
        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            print("This won't be printed.")
            value = func(*args, **kwargs)
        return value

    return func_wrapper