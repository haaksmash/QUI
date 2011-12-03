 $ python -i FileModel.py
 >>> f = FileModel.create(
 ... title="Greenboy",
 ... size=100,)
 >>> f
 <QUI Model: FileModel>
 >>> f.title
 'Greenboy'
 >>> f.size
 100
 >>> f.size = "really big"
 Traceback (most recent call last):
 ...
 ...
 fields.ValidationError: Could not convert to int: really big
 >>>