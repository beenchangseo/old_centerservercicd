create user 'atcs01'@'%' identified by 'xhdtlsqhdks1';
grant all privileges on tcs_database.* to 'atcs01'@'%';
grant all privileges on *.* to 'root'@'%' identified by 'xhdtlsqhdks1';
FLUSH privileges;