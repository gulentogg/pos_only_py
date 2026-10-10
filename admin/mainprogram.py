import module

def main():
    message = 'admin management menu.\n1. check bill\n2. manage Overview\n3. report\n\nEnter choice...'
    try:
        while True:
            choice = input(message)
            if choice == '1' : module.bill()
            elif choice == '2' : module.admin_menu()
            elif choice == '3' : module.report()
    except KeyboardInterrupt : print('End program...') 

if __name__ == '__main__' :
    main()