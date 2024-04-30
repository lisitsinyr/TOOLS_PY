import sys


def say_hello(name='World'):
    return f'Hello {name}!'


if __name__ == "__main__":

    try:
        your_name = sys.argv[1]
        print(say_hello(your_name))
    except IndexError:
        print('Please enter your name.')
