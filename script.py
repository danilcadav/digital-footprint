from datetime import datetime
my_date = datetime.now()
f = open ('/var/www/html/students/damolchanov.html','w')
f.write(my_date.isoformat())
f.close()