USE blog;

-- 登录用户表 --
CREATE TABLE IF NOT EXISTS `user` (
    `u_id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `username` varchar(64) NOT NULL,
    `password` varchar(64) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`u_id`)

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 博客文章表 --
CREATE TABLE IF NOT EXISTS `paper` (
    `p_id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `u_id` bigint unsigned NOT NULL,
    `title` varchar(128) NOT NULL,
    `path` varchar(128) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`p_id`),
    FOREIGN KEY(`u_id`) references user(`u_id`) on delete cascade on update cascade

)ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 博客评论表 --
CREATE TABLE IF NOT EXISTS `comment` (
    `c_id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `u_id` bigint unsigned NOT NULL,
    `p_id` bigint unsigned NOT NULL,
    `content` varchar(200) NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(`c_id`),
    FOREIGN KEY(`u_id`) references user(`u_id`) on delete cascade on update cascade,
    FOREIGN KEY(`p_id`) references paper(`p_id`) on delete cascade on update cascade
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `session` (
    `session_id` VARCHAR(128) NOT NULL,
    `expires` int NOT NULL,
    `data` JSON,
    PRIMARY KEY(`session_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

