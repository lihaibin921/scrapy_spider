/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80021
Source Host           : localhost:3306
Source Database       : bili

Target Server Type    : MYSQL
Target Server Version : 80021
File Encoding         : 65001

Date: 2023-11-04 20:50:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for bili_user_fail
-- ----------------------------
DROP TABLE IF EXISTS `bili_user_fail`;
CREATE TABLE `bili_user_fail` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uid` int unsigned NOT NULL,
  `re_status` int NOT NULL DEFAULT '0' COMMENT '重试状态, 0 未重抓, 1 重抓成功',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=35796 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
SET FOREIGN_KEY_CHECKS=1;
