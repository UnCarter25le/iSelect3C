

import pymssql
          
conn = pymssql.connect(server="172.17.0.4", user="SA",
                  password="---", database="iSelect3C")

cursor = conn.cursor()

cursor.execute("SELECT top(1)* FROM observation_stations")

row = cursor.fetchone()  


print(row)

cursor.close()
conn.close()




