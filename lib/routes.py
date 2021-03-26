"""
In this file are the main routes of the web service.
"""

# 3rd party modules
from pathlib import Path

rootFolder = f'{Path().absolute()}/'
databaseFolder = f'{rootFolder}database/'
databaseFile = f'sqlite:///{databaseFolder}store.db'
configsFolder = f'{rootFolder}configs/'
logsFolder = f'{rootFolder}logs/'
loggingFile = f'{configsFolder}logging.conf'
swaggerFile = f'{configsFolder}swagger.yml'
Path(logsFolder).mkdir(parents=True, exist_ok=True)         # Create logs folder if it doesn't exit
Path(databaseFolder).mkdir(parents=True, exist_ok=True)         # Create logs folder if it doesn't exit
