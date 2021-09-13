create table Attendees (
    id integer not null auto_increment,
    event_id integer not null,
    name varchar(255) not null,
    email varchar(255),
    comment text,
    primary key (id),
    constraint fk_event foreign key (event_id) references Events(id)
) 
character set utf8mb4
collate utf8mb4_unicode_ci