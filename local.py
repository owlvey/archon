import os
from engine.components.ShellComponent import ShellComponent
import logging

if __name__ == "__main__":    
    level = os.environ.get('LOGLEVEL', 'error')
    logging.basicConfig(level=level)
    value = os.environ.get("OWLVEY_CONFIG")
    logging.info(f" value config {value}")    
    shell = ShellComponent()
    shell.run()
