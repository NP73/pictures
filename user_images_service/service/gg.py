from datetime import datetimeй

d1 = datetime.strptime("2021-08-29T21:54:19.957900", "%%d/%m/%Y %H:%M:%S")
d2 = datetime.strptime("2021-08-29T21:54:19.957900", "%Y-%m-%d %H:%M:%S.%f")

print(d1 - d2)