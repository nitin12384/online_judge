
drop table if exists user_auth;
create table user_auth(
	user_id int primary key,
	user_password varchar(30) not null
);

drop table if exists submissions;
create table submissions(
	submission_id int primary key,
	problem_id int not null,
	user_id int not null default 0, -- 0 is the dummy user
	source_file_path varchar(30), -- relative path
	source_size int, -- in bytes
	verdict varchar(20),
	runtime int, -- in msec
	language varchar(20),
	
	-- format YYYY-MM-DD HH:MM:SS
	-- default value is when dummy user made all submissions
	submission_time timestamp 
		default '2000-01-01 00:00:01' 
);

drop table if exists problems;
create table problems(
	problem_id int primary key,
	name varchar(100) not null,
	data_dir_path varchar(50), -- Not absolute, but relative
	num_testcases int default 1,
	time_limit real default 1.0, -- in seconds
	memory_limit int default 256, -- in Megabytes
	source_limit int default 50000-- in Bytes
);

drop table if exists problem_languages;
create table problem_languages(
	problem_id int not null,
	language varchar(20) not null
);

drop table if exists problem_dynamic_data;
create table problem_dynamic_data(
	problem_id int primary key,
	num_submissions int default 0,
	num_accepted int default 0,
	num_uniq_user_accepted int default 0
);


