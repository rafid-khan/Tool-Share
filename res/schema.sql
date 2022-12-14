-- Set the timezone
set timezone = 'America/New_york';

create table if not exists ts_user
(
    user_id          serial primary key,
    first_name       varchar(255),
    last_name        varchar(255),
    username         varchar(64),
    password         varchar(64),
    email            varchar(255),
    creation_date    date default now(),
    last_access_date date
);

create table if not exists ts_ownership
(
    ownership_id   serial primary key,
    username       varchar(64),
    barcode        bigint,
    purchase_price decimal,
    purchase_date  date
--     primary key (username, barcode)
);

create table if not exists ts_tool
(
    tool_id     serial primary key,
    barcode     bigint,
    category    varchar(100),
    shareable   boolean,
    name        varchar(100),
    description varchar(255)
);
