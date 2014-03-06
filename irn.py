irn = 1234
str_irn = ''
if (irn < 1000):
	str_irn = str(irn)
	while (len(str_irn) < 3):
		str_irn = '0' + str_irn
	str_irn = "0" + "/" + str_irn
else:
	str_irn=str(irn)[0:len(str_irn)-3]+'/'+str(irn)[len(str_irn)-3:]
print str_irn