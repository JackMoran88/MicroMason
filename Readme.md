#Backend


###First start

```
docker exec -it micromason_django_1 /bin/sh
```

```
python manage.py load_settings
python manage.py load_data
python manage.py load_filters
python manage.py load_sliders
python manage.py load_np
```


######Other
File to hosting
```
pscp -P 22 C:\MICROMASON\backend\data\product.csv root@194.67.112.229:/root
```
Start FTP(+restart)
```
service vsftpd start
```
Docker clean
```
docker system prune
```
Права на изменения
```
chmode -R 777 MICROMASON/   
```


Файлы, в которых нужно изменить ip и прочее
./.env
./backend/private_settings.py
./frontend/.env
./backend/settings *WSGI ASGI*





