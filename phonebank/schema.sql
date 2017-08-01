drop table if exists contacts;
create table contacts (
       id integer primary key autoincrement,
       name text not null,
       address text,
       phone_number bigint not null,
       notes text 
);
