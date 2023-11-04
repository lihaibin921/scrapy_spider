/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80021
Source Host           : localhost:3306
Source Database       : bili

Target Server Type    : MYSQL
Target Server Version : 80021
File Encoding         : 65001

Date: 2023-11-04 20:50:12
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for bili_user
-- ----------------------------
DROP TABLE IF EXISTS `bili_user`;
CREATE TABLE `bili_user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `uid` int unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  `sex` varchar(45) NOT NULL,
  `follower` int unsigned NOT NULL DEFAULT '0' COMMENT '粉丝数',
  `face` varchar(255) NOT NULL,
  `sign` varchar(255) DEFAULT NULL,
  `rank` varchar(45) DEFAULT '0',
  `level` varchar(45) DEFAULT '0',
  `jointime` timestamp NULL DEFAULT NULL,
  `coins` int unsigned DEFAULT '0',
  `birthday` varchar(45) DEFAULT NULL,
  `vipType` varchar(45) DEFAULT NULL,
  `vipStatus` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `vipDueDate` timestamp NULL DEFAULT NULL,
  `vipLabel` varchar(45) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `officialRole` varchar(45) DEFAULT NULL,
  `officialTitle` varchar(255) DEFAULT NULL,
  `officialDesc` varchar(255) DEFAULT NULL,
  `officialType` varchar(45) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1231506 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
