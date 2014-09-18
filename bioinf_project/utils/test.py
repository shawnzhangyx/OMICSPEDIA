from django.test import TestCase

# Create your tests here.

string = u'[TOC]\r\n\r\n# section 1\r\n## section 1.1\r\nPlease enter something here.\r\n# section 2'

pat = re.compile(u'(^|\r\n)(#\s+section 2(.|\n)*?)(\r\n#[^#]|$)') # stop when reach next section, the end of file,or higher level of section. 

m = re.search(pat, string)
m.group(0)
m.group(1)
m.group(2)
m.group(3)

m = re.search(pat, string)
m.group(0)
m.group(1)
m.group(2)
m.group(3)

string2 = re.sub(pat, u'\r\n'+'# section 2 \r\n this is just a test'+m.group(3), string)

