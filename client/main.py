from scripts import login as lg
from scripts import main_menu as mm
def main():
    result = lg.login()
    if result:
        print('logged in')
        mm.main(result)

if __name__ == '__main__':
    main()