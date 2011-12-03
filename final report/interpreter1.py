 $ python -i FileModel.py
 >>> f = FileModel()
 >>> f
 <QUI Model: FileModel>
 >>> isinstance(f, FileModel)
 True
 >>> f.size
 >>> f.my_size()
 'None bytes'
 >>> f.size = 100
 >>> f.my_size()
 '100 bytes'
 >>>