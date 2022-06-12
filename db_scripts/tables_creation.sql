
drop table if exists user_auth;
create table user_auth(
	user_id int primary key,
	user_password varchar(30) not null
);

drop table if exists user_details;
create table user_details(
	user_id int primary key,
	username varchar(30) not null,
	full_name varchar(50)
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
	num_examples int default 1,
	time_limit real default 1.0, -- in seconds
	memory_limit int default 256, -- in Megabytes
	source_limit int default 50000-- in Bytes
);

drop table if exists problem_languages;
create table problem_languages(
	problem_id int not null,
	language varchar(20) not null
);
-- create index for efficience cause, there is no primary key
create index problem_id_index on problem_languages(problem_id);

drop table if exists problem_dynamic_data;
create table problem_dynamic_data(
	problem_id int primary key,
	num_submissions int default 0,
	num_accepted int default 0,
	num_uniq_user_accepted int default 0
);

-- default dummy data insertion
-- dummy user, admin user
insert into user_auth 
values
	(0, 'dummy_password'),
	(1, 'admin_password') ;

insert into user_details
values
	(0, 'dummy', 'Mr. Dummy dumbledore'),
	(1, 'admin01', 'Mr. Admin First');

-- 1 problems in the Database
insert into problems
values
	(1, 'Max Matrix Row', '/1', 1, 1, 1.0, 256, 50000); 

-- the problem can be accepted in C++ 14, Java 11 python  only
insert into problem_languages
values 
	(1, 'C++ 14'),
	(1, 'Java 8'),
	(1, 'Python 3.8');

insert into problem_dynamic_data 
values 
	(1, 2, 1, 1);

-- 1 submission made by dummy user which was Wrong Answer
-- and one which was AC
insert into submissions
values
	(1, 1, 0, '/data1/1.cpp', 353, 'WA', 2, 'C++ 14', '2000-01-01 00:00:01'),
	(2, 1, 0, '/data1/2.cpp', 353, 'AC', 2, 'C++ 14', '2000-01-01 00:01:01'); 