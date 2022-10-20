create database user_details
use user_details
create table details
(
userID int primary key,
username varchar(50),
password varchar(50),
email varchar(50),
rollno int
)
insert into details values (1,'Udhayakumar','udhayasiva9524','udhayasiva9524@gmail.com',711319CS170);
insert into details values (2,'Sarvesh','sarvesh22032002','sarvesh22032002@gmail.com',711319CS142);
insert into details values (3,'Shanmugasundaram','shanmugasundaram2910','shanmugasundaram2910@gmail.com',711319CS147);
insert into details values (4,'Vaishnavi','Vaishnavi','Vaishnavi@gmail.com',711319CS171);
select * from details