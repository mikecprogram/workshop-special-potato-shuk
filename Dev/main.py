
from time import sleep
from DomainLayer.Objects.Market import Market 
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    m = Market(None,None,None,None);
    token = m.enter()
    sleep(0.5)
    if(m.isToken(token)):
        print("success!")
    else:
        print("fail")

    token = m.enter()
    if(m.isToken(token)):
        print("success!")
    token = m.enter()
    sleep(1)
    print(m.isToken(token));

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
