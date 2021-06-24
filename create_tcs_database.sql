-- --------------------------------------------------------
-- 호스트:                          58.72.35.74
-- 서버 버전:                        10.5.9-MariaDB - MariaDB Server
-- 서버 OS:                        Linux
-- HeidiSQL 버전:                  11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


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
  `url` varchar(500) DEFAULT NULL COMMENT '카메라 URL(http)',
  KEY `FK_camera_local` (`id`),
  CONSTRAINT `FK_camera_local` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.center_config 구조 내보내기
CREATE TABLE IF NOT EXISTS `center_config` (
  `server_id` int(11) unsigned NOT NULL COMMENT 'server_number',
  `server_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'server_name',
  `public_ip` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'public_ip',
  `private_ip` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL COMMENT 'private_ip',
  PRIMARY KEY (`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.console_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `console_log` (
  `NO` int(11) NOT NULL AUTO_INCREMENT,
  `TIME` varchar(50) NOT NULL DEFAULT 'CURRENT_TIMESTAMP',
  `device` varchar(15) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `log` varchar(50) NOT NULL,
  PRIMARY KEY (`NO`),
  KEY `id` (`id`),
  CONSTRAINT `console_log_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

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
) ENGINE=InnoDB AUTO_INCREMENT=947559 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

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
) ENGINE=InnoDB AUTO_INCREMENT=947559 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.detect_sensor 구조 내보내기
CREATE TABLE IF NOT EXISTS `detect_sensor` (
  `d_no` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `id` int(11) NOT NULL COMMENT '교차로번호',
  `video_link` varchar(200) DEFAULT NULL COMMENT '스트리밍URL',
  `map_link` varchar(200) DEFAULT NULL,
  `device_ip` varchar(20) DEFAULT NULL COMMENT '장치 IP',
  `Detect_Number` int(11) DEFAULT NULL COMMENT '검지기 번호',
  `device_type` int(11) NOT NULL DEFAULT 1 COMMENT '장치 타입',
  PRIMARY KEY (`d_no`),
  KEY `id` (`id`),
  KEY `detect_sensor_ibfk_2` (`device_type`),
  CONSTRAINT `detect_sensor_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`),
  CONSTRAINT `detect_sensor_ibfk_2` FOREIGN KEY (`device_type`) REFERENCES `device` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.det_error 구조 내보내기
CREATE TABLE IF NOT EXISTS `det_error` (
  `seq` int(11) NOT NULL AUTO_INCREMENT,
  `log_time` varchar(50) DEFAULT NULL,
  `log_name` varchar(50) DEFAULT NULL,
  `lcid` varchar(50) DEFAULT NULL,
  `det_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`seq`)
) ENGINE=MyISAM AUTO_INCREMENT=197 DEFAULT CHARSET=utf8;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.device 구조 내보내기
CREATE TABLE IF NOT EXISTS `device` (
  `id` int(11) NOT NULL COMMENT '장치 번호',
  `NAME` varchar(10) DEFAULT NULL COMMENT '장치 이름',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.event_code 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_code` (
  `event_code` int(11) NOT NULL,
  `event_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`event_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

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
) ENGINE=InnoDB AUTO_INCREMENT=17532 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.event_status 구조 내보내기
CREATE TABLE IF NOT EXISTS `event_status` (
  `event_code` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  KEY `event_code` (`event_code`),
  CONSTRAINT `event_status_ibfk_1` FOREIGN KEY (`event_code`) REFERENCES `event_code` (`event_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.group_table 구조 내보내기
CREATE TABLE IF NOT EXISTS `group_table` (
  `group_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`group_no`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COMMENT='교차로 그룹 테이블';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.local 구조 내보내기
CREATE TABLE IF NOT EXISTS `local` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(50) NOT NULL DEFAULT '192.168.0.101',
  `name` varchar(50) NOT NULL,
  `Ver_2004` int(11) DEFAULT NULL COMMENT '동부모뎀 유무',
  `latitude` varchar(50) NOT NULL,
  `longitude` varchar(50) NOT NULL,
  `group_id` int(11) unsigned DEFAULT NULL,
  `traffic_latitude` varchar(50) DEFAULT NULL,
  `traffic_longitude` varchar(50) DEFAULT NULL,
  `traffic_x` int(11) DEFAULT NULL,
  `traffic_y` int(11) DEFAULT NULL,
  `maps` varchar(100) DEFAULT NULL,
  `markers` varchar(200) DEFAULT NULL,
  `offline` varchar(200) DEFAULT NULL,
  `online` varchar(200) DEFAULT NULL,
  `cross_type` int(10) unsigned DEFAULT NULL COMMENT '현시 갯수',
  `detector_count` int(11) NOT NULL DEFAULT 1 COMMENT '검지기 갯수',
  PRIMARY KEY (`id`),
  KEY `FK_local_group_table` (`group_id`),
  CONSTRAINT `FK_local_group_table` FOREIGN KEY (`group_id`) REFERENCES `group_table` (`group_no`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.local_status 구조 내보내기
CREATE TABLE IF NOT EXISTS `local_status` (
  `id` int(11) NOT NULL,
  `status` varchar(500) DEFAULT NULL,
  `control_info` varchar(500) DEFAULT NULL,
  KEY `id` (`id`),
  CONSTRAINT `local_status_ibfk_1` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

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
) ENGINE=InnoDB AUTO_INCREMENT=2110143 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

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

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.traffic 구조 내보내기
CREATE TABLE IF NOT EXISTS `traffic` (
  `id` int(11) NOT NULL,
  `phase` int(11) NOT NULL,
  `arrow` varchar(500) DEFAULT NULL,
  `angle` int(11) NOT NULL,
  `top` int(11) NOT NULL,
  `left` int(11) DEFAULT NULL,
  KEY `FK_traffic_local` (`id`),
  CONSTRAINT `FK_traffic_local` FOREIGN KEY (`id`) REFERENCES `local` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tcs_database.user 구조 내보내기
CREATE TABLE IF NOT EXISTS `user` (
  `no` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(50) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `ip` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
