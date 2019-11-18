use account;
create table ACCOUNT (
    EMAIL varchar(100) not null,
    FIRST_NAME varchar(100) not null,
    LAST_NAME varchar(100) not null,
    PASSWORD varchar(129) not null,
    BIRTH_DATE varchar(8) not null
);
