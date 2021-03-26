create user 'atcs02'@'%' identified by 'xhdtlsqhdks1';
grant all privileges on tcs_database.* to 'atcs02'@'%';
grant all privileges on *.* to 'root'@'%' identified by 'xhdtlsqhdks1';
FLUSH privileges;