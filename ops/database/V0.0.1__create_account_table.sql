use account;
create table ACCOUNT (
    id int not null auto_increment,
    EMAIL varchar(100) not null,
    FIRST_NAME varchar(100) not null,
    LAST_NAME varchar(100) not null,
    PASSWORD varchar(129) not null,
    BIRTH_DATE datetime not null,
    CREATED_AT datetime not null,
    UPDATED_AT datetime not null,
    PRIMARY KEY (id)
);
