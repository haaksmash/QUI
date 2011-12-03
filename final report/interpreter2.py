 $ python -i FileModel.py
 >>> f = FileModel()
 >>> f.size = "really big"
 Traceback (most recent call last):
 ...
 ...
 fields.ValidationError: Could not convert to int: really big
 >>> f.size = 100
 >>> f.size
 100
 >>>