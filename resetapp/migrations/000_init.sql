create schema resetapp;

create table resetapp.task (
  "id"      serial not null constraint task_pk primary key,
  "uid"     integer not null,
  "title"   varchar(64) not null,
  "desc"    text,
  "status"  varchar(16),
  "weight"  smallint not null default 0,
  "created" timestamp with time zone default now(),
  "updated" timestamp with time zone
);
