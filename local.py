import os
from engine.components.ShellComponent import ShellComponent


if __name__ == "__main__":
    value = os.environ.get("OWLVEY_CONFIG")
    print(value)
    shell = ShellComponent()
    shell.run()
