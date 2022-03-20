-- Set the timezone
set timezone = 'America/New_york';

create table if not exists ts_user
(
    user_id          serial primary key,
    name             varchar(255),
    username         varchar(64),
    password         varchar(64),
    creation_date    date default now(),
    last_access_date date
);

create table if not exists ts_email
(
    username varchar(64),
    email    varchar(255),
    primary key (username, email)
);

create table if not exists ts_ownership
(
    username       varchar(64),
    barcode        integer,
    purchase_price decimal,
    purchase_date  date,
    primary key (username, barcode)
);

create table if not exists ts_tool
(
    barcode     integer primary key,
    category    varchar(100),
    shareable   boolean,
    name        varchar(100),
    description varchar(255)
);
