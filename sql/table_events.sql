create table Events (
    id integer not null auto_increment,
    name varchar(255) not null,
    date date not null,
    host varchar(255),
    primary key (id)
)