create user 'atcs03'@'%' identified by 'xhdtlsqhdks1';
grant all privileges on tcs_database.* to 'atcs03'@'%';
grant all privileges on *.* to 'root'@'%' identified by 'xhdtlsqhdks1';
FLUSH privileges;