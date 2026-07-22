sport = str(input("Enter the sport you are playing: "))
match sport:
    case "basketball":
        print(f'The sport is Basketball')
    case "football":
        print(f'The sport is football')
    case _ :
        print("Unknown sport")