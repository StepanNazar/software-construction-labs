from controllers import Controller
from view import View


def main():
    controller = Controller(View())
    controller.run()


if __name__ == "__main__":
    main()
