drop table if exists users;
drop table if exists website;
drop table if exists account;

PRAGMA foreign_keys = ON;

create table users (
    pwd             char(30),
    security_q      char(100),
    security_a      char(50),
    primary key (pwd)
);
create table website (
    site_name       char(20),
    primary key (site_name)
);
create table account (
    account_no      int,
    acc_uname       char(20),
    acc_pwd         char(20),
    site_name       char(20),
    foreign key (site_name) references website,
    primary key (account_no)
);