drop table if exists NCAA;
CREATE TABLE NCAA
(
name varchar(30),
CB_Record varchar(20),
CB_Streak varchar(20),
CF_Record varchar(20),
CF_Streak varchar(20),
CF_PF varchar(20),
CF_PA varchar(20),
CB_PF varchar(20),
CB_PA varchar(20),
CB_PERCENT varchar(5),
CB_LINK varchar(150),
PRIMARY KEY (name)
);

drop table if exists NBA;
CREATE TABLE NBA
(
name varchar(30),
record varchar(20),
PF varchar(20),
PA varchar(20),
streak varchar(20),
last_10_record varchar(20),
percent varchar(5),
link varchar(150),
PRIMARY KEY (name)
);

drop table if exists NFL;
CREATE TABLE NFL
(
name varchar(30),
record varchar(20),
PF varchar(20),
PA varchar(20),
PRIMARY KEY (name)
);
