# Global modules
import subprocess

# PYPX modules
from .base import Base


class Move(Base):
    """docstring for Move."""
    def __init__(self, arg):
        super(Move, self).__init__(arg)

    def command(self):
        command = '--move ' + self.arg['aet_listener']
        command += ' --timeout 5'

        # Increase log level for debugging
        if self.arg['verbose_count'] <= 10:
            command += ' --log-level DEBUG'

        # Run a StoreSCP server with the move command to retrieve files locally
        if self.arg.get('store_local', False):
            command += ' --port ' + self.arg['storescp_port']

        # Support for dicom query files
        if self.arg.get('query_files', False):
            query_files = ' ' + self.arg['query_files']
        else:
            query_files = ''
            command += ' -k QueryRetrieveLevel=SERIES'
            command += ' -k SeriesInstanceUID=' + self.arg['series_uid']

        return self.executable + ' ' + command + ' ' + self.commandSuffix() + query_files

    def run(self):
        command = self.command()
        print('verbose_count ', self.arg['verbose_count'])
        if self.arg['verbose_count'] <= 20:
            print(command)

        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        return self.handle(response)
