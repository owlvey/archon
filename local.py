import os
from engine.components.ShellComponent import ShellComponent
import logging

if __name__ == "__main__":    
    level = os.environ.get('LOGLEVEL', 'ERROR')
    logging.basicConfig(level=level)
    value = os.environ.get("OWLVEY_CONFIG", '/Users/Gregory/owlvey/archon/system.yaml')
    logging.info(f" value config {value}")    
    #logging.getLogger('sqlalchemy.engine').setLevel(level)
    shell = ShellComponent()
    shell.run()
