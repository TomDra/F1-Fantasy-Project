from scripts import login as lg
from scripts import main_menu as mm
def main():
    result = lg.login()  # get login result
    if result:
        print('logged in')
        mm.main(result)  # call main menu

if __name__ == '__main__':
    main()