-- Data prepared by Weixi Cheng, weixi@ualberta.ca
-- Published on Nov 1, 2020

drop table if exists answers;
drop table if exists questions;
drop table if exists votes;
drop table if exists tags;
drop table if exists posts;
drop table if exists ubadges;
drop table if exists badges;
drop table if exists privileged;
drop table if exists users;

PRAGMA foreign_keys = ON;

create table users (
  uid		char(4),
  name		text,
  pwd		text,
  city		text,
  crdate	date,
  primary key (uid)
);
create table privileged (
  uid		char(4),
  primary key (uid),
  foreign key (uid) references users
);
create table badges (
  bname		text,
  type		text,
  primary key (bname)
);
create table ubadges (
  uid		char(4),
  bdate		date,
  bname		text,
  primary key (uid,bdate),
  foreign key (uid) references users,
  foreign key (bname) references badges
);
create table posts (
  pid		char(4),
  pdate		date,
  title		text,
  body		text,
  poster	char(4),
  primary key (pid),
  foreign key (poster) references users
);
create table tags (
  pid		char(4),
  tag		text,
  primary key (pid,tag),
  foreign key (pid) references posts
);
create table votes (
  pid		char(4),
  vno		int,
  vdate		text,
  uid		char(4),
  primary key (pid,vno),
  foreign key (pid) references posts,
  foreign key (uid) references users
);
create table questions (
  pid		char(4),
  theaid	char(4),
  primary key (pid),
  foreign key (theaid) references answers
);
create table answers (
  pid		char(4),
  qid		char(4),
  primary key (pid),
  foreign key (qid) references questions
);

--test data
--Privileged users

INSERT INTO users VALUES ('u100','Davood Rafiei','123456','Edmonton','2020-01-10');
INSERT INTO users VALUES ('u200','Bingran Huang','111','Edmonton','2020-01-10');
INSERT INTO privileged VALUES ('u100');
INSERT INTO privileged VALUES ('u200');


INSERT INTO posts VALUES ('p100','2020-02-10','CMPUT291 is a good course.','Davood is a very nice prof.','u100');
INSERT INTO posts VALUES ('p200','2020-03-10','I agree.','Mini project make us learn a lot.','u200');
INSERT INTO posts VALUES ('p300','2020-04-10','CMPUT301 is a little difficult.','Database is useful.','u100');
INSERT INTO posts VALUES ('p400','2020-02-10','Prof who teaches CMPUT340 is really nice.','He helps us a lot.','u100');
INSERT INTO posts VALUES ('p500','2020-02-10','CMPUT301 is a little difficult.','Since we need to learn Android Studio.','u100');
INSERT INTO posts VALUES ('p600','2020-02-10','Agree above!','The project is hard!','u100');
INSERT INTO posts VALUES ('p700','2020-02-10','300 level cs course is not easy.','Such as 301, 340.','u100');
INSERT INTO posts VALUES ('p800','2020-02-11','I agree above.','Database is useful.','u100');

INSERT INTO questions VALUES ('p100',null);
INSERT INTO questions VALUES ('p300',null);
INSERT INTO questions VALUES ('p400',null);
INSERT INTO questions VALUES ('p500',null);

INSERT INTO answers VALUES ('p200','p100');
INSERT INTO answers VALUES ('p600','p300');
INSERT INTO answers VALUES ('p700','p400');
INSERT INTO answers VALUES ('p800','p100');

UPDATE questions SET
theaid = 'p200'
WHERE pid = 'p100';

UPDATE questions SET
theaid = 'p600'
WHERE pid = 'p300';

INSERT INTO tags VALUES ('p100','CS');
