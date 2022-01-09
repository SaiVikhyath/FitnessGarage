create table GymMembers
(
regNo varchar(255) primary key,
memberName varchar(255) not null,
phoneNumber varchar(255) not null unique,
email varchar(255),
startDate varchar(255) not null,
subscription varchar(255) not null
);

drop view GymStats;
create view GymStats as
select (select count(*) from GymMembers) as totalmembers,
(select count(*) from GymMembers where personaltraining='Yes') as personaltraining,
(select count(*) from GymMembers where subscriptiontype='Cardio') as cardiomembers,
(select count(*) from GymMembers where subscriptiontype='Weights') weightsmembers;


insert into GymStats values (0,0,0,0);

update GymMembers set startdate='1635300000' where regno='123456';

alter table GymMembers
add column subscriptionType varchar(255),
add column personalTraining varchar(255);



select * from GymMembers;
select * from PersonalTraining;
select * from CardioMembers;
select * from WeightMembers;
select * from GymStats;

select startdate from GymMembers;
select extract(epoch from now());


update GymMembers 
set personalTraining='No' where regNo='100';

delete from GymMembers
where membername='Fitness Garage';
rollback;

drop view PersonalTraining;
create view PersonalTraining as
select * from GymMembers
where personaltraining='Yes';

drop view CardioMembers;
create view CardioMembers as
select * from GymMembers
where subscriptiontype='Cardio';

drop view WeightMembers;
create view WeightMembers as
select * from GymMembers
where subscriptiontype='Weights';




insert into GymMembers values
('1', 'Praveen Yadav', '9997778889', 'praveen@gmail.com', extract(epoch from current_date), '6');

insert into GymMembers values
('2', 'Praveen', '9997778879', 'praveen@gmail.com', extract(epoch from current_date), '6');

insert into GymMembers values
('3', 'PY', '9967778879', 'praveen2@gmail.com', extract(epoch from current_date), '9');

insert into GymMembers values
('4', 'PY', '9967778679', 'praveen3@gmail.com', extract(epoch from current_date), '3');

insert into GymMembers values
('5', 'PY', '9967778479', 'praveen4@gmail.com', extract(epoch from current_date), '12');

insert into GymMembers values
('6', 'PY', '9967778459', 'praveen5@gmail.com', extract(epoch from current_date) - 24*60*60*600, '1');

insert into GymMembers values
('7', 'PY', '9967718459', 'praveen6@gmail.com', '1629763200', '2');

insert into GymMembers values
('8', 'PY', '9963778459', 'praveen8@gmail.com', extract(epoch from current_date) - 3*24*60*60, '1');

insert into GymMembers values
('9', 'PY', '9963778439', 'praveen8@gmail.com', extract(epoch from current_date) - 2*30*24*60*60, '1');

insert into GymMembers values
('10', 'PY', '9963775459', 'praveen8@gmail.com', extract(epoch from current_date) - 1*30*24*60*60, '1');

insert into GymMembers values
('11', 'PY', '9963775569', 'praveen8@gmail.com', extract(epoch from current_date) - 1*31*24*60*60, '1');

insert into GymMembers values
('12', 'PY', '9963475569', 'praveen8@gmail.com', extract(epoch from current_date) - 1*29*24*60*60, '1');

insert into GymMembers values
('0', 'Vikhyath', '7893744257', 'vikhyath456@gmail.com', '1638190478', '1');

insert into GymMembers values
('13', 'Test', '9390109846', 'vikhyath456@gmail.com', '1635107420', '2');

insert into GymMembers values
('14', 'Test1', '1233744257', 'vikhyath456@gmail.com', '1637519606', '1');


update GymMembers
set email = 'tmptmptmptmtp@tmpt.com'
where email = 'praveen@gmail.com';


update GymMembers
set startdate = '1634928471'
where regno='0';


delete from GymMembers
where phonenumber='7893744257';