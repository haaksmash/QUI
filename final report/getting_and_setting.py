 $ python -i FileModel.py
 >>> f = FileModel.create(
 ... name="arrow.jpg",
 ... size=100,
     title="Greenboy")
 >>> f
 <FileModel: arrow.jpg>
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