CREATE DATABASE inventoryDB;
USE inventoryDB;

CREATE TABLE `user` (
  `user_id` int(15) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email_id` varchar(100) NOT NULL,
  `created_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `user_role` (
  `user_role_id` int(15) NOT NULL AUTO_INCREMENT,
  `user_role_name` varchar(100) NOT NULL,
  `created_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`user_role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `user_role_map` (
  `user_role_map_id` int(15) NOT NULL AUTO_INCREMENT,
  `user_id` int(15) NOT NULL,
  `user_role_id` int(15) NOT NULL,
  `created_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`user_role_map_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`),
  FOREIGN KEY (`user_role_id`) REFERENCES user_role(`user_role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `product` (
  `product_id` int(15) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `vendor_name` varchar(100) NOT NULL,
  `mrp` float NOT NULL,
  `batch_num` varchar(100) NOT NULL,
  `batch_date` varchar(100) NOT NULL,
  `quantity` int(50) NOT NULL,
  `user_id` int(15) NOT NULL,
  `status` ENUM("active", "inactive") NOT NULL,
  `created_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `update_request` (
  `request_id` int(15) NOT NULL AUTO_INCREMENT,
  `user_id` int(15) NOT NULL,
  `request_type` ENUM("new_product", "update_product", "remove_product") NOT NULL,
  `status` ENUM("approved", "pending", "rejected") NOT NULL,
  `update_data` TEXT DEFAULT NULL,
  `created_datetime` DATETIME NOT NULL,
  PRIMARY KEY (`request_id`),
  FOREIGN KEY (`user_id`) REFERENCES user(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into user values(1, "user1", "user1pass", "user@gmail.com", now());
insert into user values(2, "user2", "user2pass", "user2@gmail.com", now());
insert into user values(3, "user3", "user3pass", "user3@gmail.com", now());
insert into user_role values(1, "Store Manager", now());
insert into user_role values(2, "Depart Manager", now());
insert into user_role_map values(1,1,1,now());
insert into user_role_map values(2,1,2,now());
insert into user_role_map values(3,2,1,now());
