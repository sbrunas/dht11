import ftplib
session = ftplib.FTP('201.215.167.63', 'pi', '_4oYiEmqVUFl')
file = open('/home/pi/log/iot/2019-09-23_dht.log','rb')                  # file to send
session.storbinary('/home/pi/log/iot/2019-09-23_dht.log', file)     # send the file
file.close()                                    # close file and FTP
session.quit()