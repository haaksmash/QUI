from filemodel import FileModel
from qui.decorators.storage_decorators import subclass
from qui.decorators.field_decorators import class_field

class ImageFile(FileModel):
    pass
    

class TextFile(FileModel):
    word_count = IntegerField
    txt_file_count = 100

@subclass
class MoreClassFields(FileModel):
    special_count = class_field(IntegerField)
    
class RemoteFile(FileModel):
    _port = 91711

    def __init__(self, host):
        super(Remote_File, self).__init__(self)
        self._host = host