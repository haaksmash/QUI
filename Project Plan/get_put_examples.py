 >>> from models import File
 >>> f = File.get(pk=100)
 >>> f
 <Model_File: JigglyBits.jpg>
 >>> f.name
 'JigglyBits.jpg'
 >>> type(f)
 <type 'File'>
 >>> f.my_size()
 '1MB'
 >>> f.host
 <Model_Host: 134.173.63.80>
 >>> f.notes = " NSFW! "
 >>> f.put()
 >>> g = File.get(pk=100)
 >>> g
 <Model_File: JigglyBits.jpg>
 >>> g.notes
 ' NSFW! '