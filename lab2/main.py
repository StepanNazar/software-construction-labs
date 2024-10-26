import argparse


def fahrenheit_to_celsius(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 1)


def interactive():
    run = True
    while run:
        try:
            fahrenheit = int(input("Enter temperature in F: "))
            print("Temperature in C:", fahrenheit_to_celsius(fahrenheit))
            if input("Want to proceed? (Y/n): ").lower() == "n":
                run = False
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\nExiting...")
            run = False


def main():
    parser = argparse.ArgumentParser(
        description="Convert Fahrenheit to Celsius. No arguments will start interactive mode."
    )
    parser.add_argument(
        "-f", "--fahrenheit", type=int, help="Fahrenheit value to convert to Celsius"
    )
    args = parser.parse_args()
    if args.fahrenheit:
        print("Temperature in C:", fahrenheit_to_celsius(args.fahrenheit))
    else:
        interactive()


if __name__ == "__main__":
    main()
