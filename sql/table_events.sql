create table Events (
    id integer not null auto_increment,
    name varchar(255) not null,
    date date not null,
    host varchar(255),
    description text,
    primary key (id)
)
character set utf8mb4
collate utf8mb4_unicode_ci