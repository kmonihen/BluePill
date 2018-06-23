# BluePill
# Author: Keith Monihen, 2018
#
# An expanded decorator class for using Placebo when unit testing boto3 calls.
#
# Provides:
#  BluePill class
import placebo
import boto3

class BluePill(object):

    # Set these as defaults in the TestCase setUp.
    RECORD=False # Default is playback, recording toggled off.
    SESSION = None # A boto3 session that Placebo attaches to.
    CLIENT_TYPE=None # The boto3 client type. 
    FOLDER_PATH=None # The path of the placebo data folder

    # __init__
    #
    # Optional Parameters:
    #  client_type (String) - The boto3 client type.
    #  folder_path (String) - The path of the placebo data folder.
    #  session (boto3.Session) - A boto3 session that Placebo attaches to.
    #  record (Boolean) - Switch to record mode.
    def __init__(self, client_type=None, folder_path=None, session=None, record=None):
        self.session = session
        self.clientType = client_type
        self.folderPath = folder_path
        self.record = record

    # setOptions
    #  Options can change between __init__ and __call__ so check the variables and set them.
    def _setOptions(self):
        if not self.session: self.session = self.SESSION
        if not self.clientType: self.clientType = self.CLIENT_TYPE
        if not self.folderPath: self.folderPath = self.FOLDER_PATH
        if not isinstance(self.record, bool): self.record = self.RECORD

        # Raise exception if none of the required variables are provided
        if not self.clientType: raise ValueError("You must provide 'client_type' parameter or set the 'CLIENT_TYPE' class variable.")
        if not self.folderPath: raise ValueError("You must provide 'folder_path' parameter or set the 'FOLDER_PATH' class variable.")
        if not self.session: raise ValueError("You must provide the 'session' parameter or set the 'SESSION' class variable.")
        if not isinstance(self.record, bool): raise TypeError("You must provide a boolean value for the 'record' parameter or 'RECORD' class variable")
        return True
    
    # __call__
    #
    def __call__(self, function, *args, **kwargs):
        def placeboTest(*args, **kwargs):
            self._setOptions()
            # Attach to session
            pill = placebo.attach(self.session, data_path=self.folderPath)

            # Set the client for use in the unit test
            kwargs['client'] = self.session.client(self.clientType)
            
            if self.record: pill.record() # Record calls if record has been toggled on
            else: pill.playback() # Otherwise play back existing calls

            return function(*args, **kwargs)
        return placeboTest
