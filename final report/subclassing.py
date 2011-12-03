from filemodel import FileModel

class ImageFile(FileModel):
    pass
    
class TextFile(FileModel):
    word_count = IntegerField
    txt_file_count = 100
    
class RemoteFile(FileModel):
    _port = 91711

    def __init__(self, host):
        super(Remote_File, self).__init__(self)
        self._host = host