# Global modules
import subprocess

# PYPX modules
from .base import Base


class Move(Base):
    """docstring for Move."""
    def __init__(self, arg):
        super(Move, self).__init__(arg)

    def command(self, opt={}):
        command = '--move ' + opt['aet_listener']
        command += ' --timeout 5'

        # Run a StoreSCP server with the move command to retrieve files locally
        if opt.get('store_local', False):
            command += ' --port ' + opt['storescp_port']

        # Support for dicom query files
        if opt.get('query_files', False):
            query_files = ' ' + opt['query_files']
        else:
            query_files = ''
            command += ' -k QueryRetrieveLevel=SERIES'
            command += ' -k SeriesInstanceUID=' + opt['series_uid']

        return self.executable + ' ' + command + ' ' + self.commandSuffix() + query_files

    def run(self, opt={}):
        response = subprocess.run(
            self.command(opt), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        return self.handle(response)
