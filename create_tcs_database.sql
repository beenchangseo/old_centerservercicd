-- --------------------------------------------------------
-- 호스트:                          192.168.1.182
-- 서버 버전:                        10.5.12-MariaDB - MariaDB Server
-- 서버 OS:                        Linux
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- tcs_database 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `tcs_database` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tcs_database`;

-- 테이블 tcs_database.camera 구조 내보내기
CREATE TABLE IF NOT EXISTS `camera` (
  `idx` int(11) DEFAULT NULL COMMENT '자동증가 값',
  `id` int(11) DEFAULT NULL COMMENT '교차로번호',
  `num` int(11) DEFAULT NULL COMMENT '검지기번호',
  `camera_x` int(11) DEFAULT NULL COMMENT 'X축 px값',
  `camera_y` int(11) DEFAULT NULL COMMENT 'Y축 px값',
  `angle` int(11) DEFAULT NULL COMMENT 'Angle px값',
  `url` varchar(500) DEFAULT NULL COMMENT '영상처리 스트림',
  `camUrl` varchar(500) DEFAULT NULL COMMENT '카메라스트림',
  KEY `FK_camera_local` (`id`),
  CONSTRAINT `FK_camera_local` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 테이블 데이터 tcs_database.camera:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `camera` DISABLE KEYS */;
INSERT INTO `camera` (`idx`, `id`, `num`, `camera_x`, `camera_y`, `angle`, `url`, `camUrl`) VALUES
	(1, 1, 1, 102, -20, -93, 'http://14.51.232.239:3300/stream/mjpeg?id=1&num=1', 'http://14.51.232.239:3300/stream/camera?id=1&num=1');
/*!40000 ALTER TABLE `camera` ENABLE KEYS */;

-- 테이블 tcs_database.center_config 구조 내보내기
CREATE TABLE IF NOT EXISTS `center_config` (
  `server_id` int(11) unsigned NOT NULL COMMENT 'server_number',
  `server_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'server_name',
  `public_ip` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'public_ip',
  `private_ip` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'private_ip',
  PRIMARY KEY (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 테이블 데이터 tcs_database.center_config:~3 rows (대략적) 내보내기
/*!40000 ALTER TABLE `center_config` DISABLE KEYS */;
INSERT INTO `center_config` (`server_id`, `server_name`, `public_ip`, `private_ip`) VALUES
	(1, '장흥 서버1', '14.51.232.239', '192.168.1.181'),
	(2, '장흥 서버2', '14.51.232.239', '192.168.1.182'),
	(3, '장흥 서버3', '14.51.232.239', '192.168.1.183');
/*!40000 ALTER TABLE `center_config` ENABLE KEYS */;

-- 테이블 tcs_database.crossNodeApi 구조 내보내기
CREATE TABLE IF NOT EXISTS `crossNodeApi` (
  `link_id` int(11) unsigned NOT NULL COMMENT '유니티 도로 링크아이디',
  `COMMENT` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT '추가설명'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 테이블 데이터 tcs_database.crossNodeApi:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `crossNodeApi` DISABLE KEYS */;
/*!40000 ALTER TABLE `crossNodeApi` ENABLE KEYS */;

-- 테이블 tcs_database.cycle_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `cycle_log` (
  `log_no` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` varchar(50) DEFAULT NULL COMMENT '로그 시간',
  `id` int(11) DEFAULT NULL COMMENT '교차로 번호',
  `cycle` int(11) DEFAULT 0 COMMENT '주기',
  `offset` int(11) DEFAULT 0 COMMENT '연동값',
  `split_1` int(11) DEFAULT 0,
  `split_2` int(11) DEFAULT 0,
  `split_3` int(11) DEFAULT 0,
  `split_4` int(11) DEFAULT 0,
  `split_5` int(11) DEFAULT 0,
  `split_6` int(11) DEFAULT 0,
  `split_7` int(11) DEFAULT 0,
  `split_8` int(11) DEFAULT 0,
  `ped_1` int(11) DEFAULT 0,
  `ped_2` int(11) DEFAULT 0,
  `ped_3` int(11) DEFAULT 0,
  `ped_4` int(11) DEFAULT 0,
  `ped_5` int(11) DEFAULT 0,
  `ped_6` int(11) DEFAULT 0,
  `ped_7` int(11) DEFAULT 0,
  `ped_8` int(11) DEFAULT 0,
  PRIMARY KEY (`log_no`),
  KEY `id` (`id`),
  CONSTRAINT `cycle_log_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1548915 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.cycle_log:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `cycle_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `cycle_log` ENABLE KEYS */;

-- 테이블 tcs_database.detect_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `detect_log` (
  `log_no` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` varchar(50) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `vol_1` int(11) DEFAULT 0,
  `occ_1` int(11) DEFAULT 0,
  `vol_2` int(11) DEFAULT 0,
  `occ_2` int(11) DEFAULT 0,
  `vol_3` int(11) DEFAULT 0,
  `occ_3` int(11) DEFAULT 0,
  `vol_4` int(11) DEFAULT 0,
  `occ_4` int(11) DEFAULT 0,
  `vol_5` int(11) DEFAULT 0,
  `occ_5` int(11) DEFAULT 0,
  `vol_6` int(11) DEFAULT 0,
  `occ_6` int(11) DEFAULT 0,
  `vol_7` int(11) DEFAULT 0,
  `occ_7` int(11) DEFAULT 0,
  `vol_8` int(11) DEFAULT 0,
  `occ_8` int(11) DEFAULT 0,
  PRIMARY KEY (`log_no`),
  KEY `id` (`id`),
  KEY `idx_id_log_time` (`id`,`log_time`),
  KEY `id_2` (`id`,`log_time`),
  CONSTRAINT `detect_log_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1548915 DEFAULT CHARSET=utf8;

-- 테이블 데이터 tcs_database.detect_log:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `detect_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `detect_log` ENABLE KEYS */;

-- 테이블 tcs_database.detect_sensor 구조 내보내기
CREATE TABLE IF NOT EXISTS `detect_sensor` (
  `d_no` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `id` int(11) NOT NULL COMMENT '교차로번호',
  `video_link` varchar(200) DEFAULT NULL COMMENT '스트리밍URL',
  `ogCamera_link` varchar(200) DEFAULT NULL,
  `device_ip` varchar(20) DEFAULT NULL COMMENT '장치 IP',
  `Detect_Number` int(11) DEFAULT NULL COMMENT '검지기 번호',
  `device_type` int(11) NOT NULL DEFAULT 1 COMMENT '장치 타입',
  PRIMARY KEY (`d_no`),
  KEY `id` (`id`),
  KEY `detect_sensor_ibfk_2` (`device_type`),
  CONSTRAINT `detect_sensor_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`),
  CONSTRAINT `detect_sensor_ibfk_2` FOREIGN KEY (`device_type`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.detect_sensor:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `detect_sensor` DISABLE KEYS */;
INSERT INTO `detect_sensor` (`d_no`, `name`, `id`, `video_link`, `ogCamera_link`, `device_ip`, `Detect_Number`, `device_type`) VALUES
	(1, '용진삼거리 1번', 1, 'http://14.51.232.120:7777/', 'http://admin:dongbuict0@223.171.56.51:1080/streaming/channels/http/0', '14.51.232.120', 1, 4);
/*!40000 ALTER TABLE `detect_sensor` ENABLE KEYS */;

-- 테이블 tcs_database.device 구조 내보내기
CREATE TABLE IF NOT EXISTS `device` (
  `id` int(11) NOT NULL COMMENT '장치 번호',
  `NAME` varchar(10) DEFAULT NULL COMMENT '장치 이름',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.device:~12 rows (대략적) 내보내기
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` (`id`, `NAME`) VALUES
	(1, '서버'),
	(2, '제어기'),
	(3, '검지기'),
	(4, '1번 NANO'),
	(5, '1번 CAMERA'),
	(6, '2번 NANO'),
	(7, '2번 CAMERA'),
	(8, '3번 NANO'),
	(9, '3번 CAMERA'),
	(10, '4번 NANO'),
	(11, '4번 CAMERA'),
	(12, '라우터');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;

-- 테이블 tcs_database.event_code 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_code` (
  `event_code` int(11) NOT NULL,
  `event_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`event_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.event_code:~29 rows (대략적) 내보내기
/*!40000 ALTER TABLE `event_code` DISABLE KEYS */;
INSERT INTO `event_code` (`event_code`, `event_name`) VALUES
	(0, '제어기 통신상태'),
	(1, 'CAN 상태'),
	(2, 'LTE 통신상태'),
	(3, '예비_03'),
	(4, '예비_04'),
	(5, '조광제어'),
	(6, 'SCU 통신'),
	(7, 'Power Fail'),
	(8, 'DATABASE'),
	(9, '점멸'),
	(10, '소등'),
	(11, '모순'),
	(12, '소등 스위치'),
	(13, '점멸 스위치'),
	(14, '수동 스위치'),
	(15, '수동진행 스위치'),
	(16, 'DOOR'),
	(17, '모순검지'),
	(18, '수동제어'),
	(19, '시차제'),
	(20, '예비_20'),
	(21, '예비_21'),
	(22, '예비_22'),
	(23, '푸쉬버튼'),
	(24, '예비_24'),
	(25, '검지기 1번'),
	(26, '예비_26'),
	(27, '검지기 2번'),
	(99, 'RESTART');
/*!40000 ALTER TABLE `event_code` ENABLE KEYS */;

-- 테이블 tcs_database.event_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_log` (
  `log_no` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` varchar(50) DEFAULT NULL,
  `device` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `event_code` int(11) NOT NULL,
  `event_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`log_no`),
  KEY `event_code` (`event_code`),
  KEY `device` (`device`),
  CONSTRAINT `event_log_ibfk_1` FOREIGN KEY (`event_code`) REFERENCES `event_code` (`event_code`),
  CONSTRAINT `event_log_ibfk_2` FOREIGN KEY (`device`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21276 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.event_log:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `event_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_log` ENABLE KEYS */;

-- 테이블 tcs_database.event_status 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_status` (
  `event_code` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  KEY `event_code` (`event_code`),
  CONSTRAINT `event_status_ibfk_1` FOREIGN KEY (`event_code`) REFERENCES `event_code` (`event_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.event_status:~58 rows (대략적) 내보내기
/*!40000 ALTER TABLE `event_status` DISABLE KEYS */;
INSERT INTO `event_status` (`event_code`, `value`, `status`) VALUES
	(0, 0, '통신on'),
	(0, 1, '통신off'),
	(1, 0, 'CAN_정상'),
	(1, 1, 'CAN_고장'),
	(2, 0, 'ONLINE'),
	(2, 1, 'OFFLINE'),
	(3, 0, '0'),
	(3, 1, '1'),
	(4, 1, '1'),
	(4, 0, '0'),
	(5, 1, 'ON'),
	(5, 0, 'OFF'),
	(6, 1, '이상'),
	(6, 0, '정상'),
	(7, 0, '정상'),
	(7, 1, '이상'),
	(8, 0, '정상'),
	(8, 1, '이상'),
	(9, 0, '점멸 종료'),
	(9, 1, '점멸 시작'),
	(10, 0, '소등 종료'),
	(10, 1, '소등 시작'),
	(11, 0, '해제'),
	(11, 1, '모순'),
	(12, 0, '수동 수등 종료'),
	(12, 1, '수동 소등 시작'),
	(13, 0, '수동 점멸 종료'),
	(13, 1, '수동 점멸 시작'),
	(14, 0, '수동 종료'),
	(14, 1, '수동 시작'),
	(15, 0, 'x'),
	(15, 1, '수동 버튼 누름'),
	(16, 0, '닫힘'),
	(16, 1, '열림'),
	(17, 0, '금지'),
	(17, 1, '허용'),
	(18, 0, '수동금지'),
	(18, 1, '수동허용'),
	(19, 0, '종료'),
	(19, 1, '시작'),
	(20, 0, '0'),
	(20, 1, '1'),
	(21, 0, '0'),
	(21, 1, '1'),
	(22, 0, '0'),
	(22, 1, '1'),
	(23, 0, 'ENABLE'),
	(23, 1, 'DISABLE'),
	(24, 0, '0'),
	(24, 1, '1'),
	(25, 0, '0'),
	(25, 1, '1'),
	(26, 0, '0'),
	(26, 1, '1'),
	(27, 0, '0'),
	(27, 1, '1'),
	(99, 0, '0'),
	(99, 1, '1');
/*!40000 ALTER TABLE `event_status` ENABLE KEYS */;

-- 테이블 tcs_database.group_table 구조 내보내기
CREATE TABLE IF NOT EXISTS `group_table` (
  `group_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`group_no`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COMMENT='교차로 그룹 테이블';

-- 테이블 데이터 tcs_database.group_table:~1 rows (대략적) 내보내기
/*!40000 ALTER TABLE `group_table` DISABLE KEYS */;
INSERT INTO `group_table` (`group_no`, `group_name`) VALUES
	(1, '1번 그룹');
/*!40000 ALTER TABLE `group_table` ENABLE KEYS */;

-- 테이블 tcs_database.local 구조 내보내기
CREATE TABLE IF NOT EXISTS `local` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL DEFAULT '192.168.0.101',
  `name` varchar(50) NOT NULL,
  `Ver_2004` int(11) DEFAULT NULL COMMENT '동부모뎀 유무',
  `latitude` varchar(50) NOT NULL,
  `longitude` varchar(50) NOT NULL,
  `group_id` int(11) unsigned DEFAULT NULL,
  `traffic_x` int(11) DEFAULT NULL,
  `traffic_y` int(11) DEFAULT NULL,
  `maps` varchar(100) DEFAULT NULL,
  `markers` varchar(200) DEFAULT NULL,
  `offline` varchar(200) DEFAULT NULL,
  `online` varchar(200) DEFAULT NULL,
  `cross_type` int(10) unsigned DEFAULT NULL COMMENT '현시 갯수',
  `detector_count` int(11) NOT NULL DEFAULT 1 COMMENT '검지기 갯수',
  `prevNode_distance` int(11) NOT NULL DEFAULT 0 COMMENT '전 교차로 와의 거리',
  PRIMARY KEY (`id`),
  KEY `FK_local_group_table` (`group_id`),
  CONSTRAINT `FK_local_group_table` FOREIGN KEY (`group_id`) REFERENCES `group_table` (`group_no`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.local:~2 rows (대략적) 내보내기
/*!40000 ALTER TABLE `local` DISABLE KEYS */;
INSERT INTO `local` (`id`, `ip`, `name`, `Ver_2004`, `latitude`, `longitude`, `group_id`, `traffic_x`, `traffic_y`, `maps`, `markers`, `offline`, `online`, `cross_type`, `detector_count`, `prevNode_distance`) VALUES
	(1, '192.168.1.203', '회사1', 0, '126.96944239470625', '37.390796490308624', 1, -29, -28, 'map_1.png', 'marker-default_1.png', 'marker-offline_1.png', 'marker-online_1.png', 3, 1, 0),
	(2, '192.168.1.42', '회사2', 0, '126.96886149246555', '37.396017763471434', 1, -50, -50, 'map_2.png', 'marker-default_2.png', 'marker-offline_2.png', 'marker-online_2.png', 3, 1, 0);
/*!40000 ALTER TABLE `local` ENABLE KEYS */;

-- 테이블 tcs_database.network_report 구조 내보내기
CREATE TABLE IF NOT EXISTS `network_report` (
  `no` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` varchar(30) NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
  `id` int(11) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `device` varchar(15) DEFAULT NULL,
  `device_num` int(11) DEFAULT NULL,
  `online` int(2) NOT NULL COMMENT '통신 상태',
  `PS_RUN` int(2) DEFAULT -1 COMMENT '검지프로그램 동작 상태',
  `CAN_STS` int(2) DEFAULT -1 COMMENT 'CAN 동작 상태',
  `LMB_STS` int(2) DEFAULT -1 COMMENT 'LMB 동작 상태',
  `DET_MODE` int(2) DEFAULT -1 COMMENT '검지 모드(0:정상, 1:강제 감응, 2:강제 미감응)',
  PRIMARY KEY (`no`),
  KEY `id` (`id`),
  CONSTRAINT `network_report_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12528111 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.network_report:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `network_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `network_report` ENABLE KEYS */;

-- 테이블 tcs_database.network_report_console 구조 내보내기
CREATE TABLE IF NOT EXISTS `network_report_console` (
  `log_time` varchar(30) NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
  `id` int(11) DEFAULT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `device` varchar(15) DEFAULT NULL,
  `device_num` int(11) DEFAULT NULL,
  `online` int(2) NOT NULL,
  `PS_RUN` int(2) DEFAULT -1,
  `CAN_STS` int(2) DEFAULT -1,
  `LMB_STS` int(2) DEFAULT -1,
  `DET_MODE` int(2) DEFAULT -1,
  KEY `id` (`id`),
  CONSTRAINT `network_report_console_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.network_report_console:~0 rows (대략적) 내보내기
/*!40000 ALTER TABLE `network_report_console` DISABLE KEYS */;
/*!40000 ALTER TABLE `network_report_console` ENABLE KEYS */;

-- 테이블 tcs_database.traffic 구조 내보내기
CREATE TABLE IF NOT EXISTS `traffic` (
  `id` int(11) NOT NULL,
  `phase` int(11) NOT NULL,
  `arrow` varchar(500) DEFAULT NULL,
  `angle` int(11) NOT NULL,
  `top` int(11) NOT NULL,
  `left` int(11) DEFAULT NULL,
  `unityX` int(11) NOT NULL COMMENT 'unity x축',
  `unityY` int(11) NOT NULL COMMENT 'unity y축',
  `unityZ` int(11) NOT NULL COMMENT 'unity z축',
  KEY `FK_traffic_local` (`id`),
  CONSTRAINT `FK_traffic_local` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 테이블 데이터 tcs_database.traffic:~4 rows (대략적) 내보내기
/*!40000 ALTER TABLE `traffic` DISABLE KEYS */;
INSERT INTO `traffic` (`id`, `phase`, `arrow`, `angle`, `top`, `left`, `unityX`, `unityY`, `unityZ`) VALUES
	(1, 1, 'detour.png', -92, 35, 36, 180, 0, 0),
	(1, 2, 'left.png', -93, 35, 36, 180, 0, -90),
	(1, 3, 'updown.png', -99, 35, 36, 180, 0, 0),
	(1, 4, 'detour.png', -77, 35, 36, 180, 0, 0);
/*!40000 ALTER TABLE `traffic` ENABLE KEYS */;

-- 테이블 tcs_database.user 구조 내보내기
CREATE TABLE IF NOT EXISTS `user` (
  `no` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(50) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `ip` varchar(50) DEFAULT NULL,
  `role` varchar(10) DEFAULT NULL,
  `date_created` varchar(50) DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `date_modify` varchar(50) DEFAULT NULL,
  `modifier` varchar(50) DEFAULT NULL,
  `note` varchar(50) DEFAULT '',
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4;

-- 테이블 데이터 tcs_database.user:~2 rows (대략적) 내보내기
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`no`, `id`, `pass`, `ip`, `role`, `date_created`, `created_by`, `date_modify`, `modifier`, `note`) VALUES
	(1, 'superadmin', 'bdd277ea549604930717f20f4ca96d1753ad9d9b55d26c05519c061c3d584c7721d5e82312040eaff91b4924d85dc69e1f272878f1f261405eba3b93d7aa7076', '*', 'admin', NULL, 'superadmin', NULL, NULL, ''),
	(57, 'police', 'bdd277ea549604930717f20f4ca96d1753ad9d9b55d26c05519c061c3d584c7721d5e82312040eaff91b4924d85dc69e1f272878f1f261405eba3b93d7aa7076', '*', 'user', '2021-10-05 14:10:40', 'superadmin', '2021-10-13 13:44:15', 'superadmin', '경찰 모니터링 계정');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
