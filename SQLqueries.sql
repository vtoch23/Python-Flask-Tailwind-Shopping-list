use new_db;

create table prod (
	id int not null AUTO_INCREMENT,
    name varchar(255) NOT NULL, 
    price FLOAT NOT NULL, 
    discount FLOAT NOT NULL,
    primary key (id));
    
insert into prod (name, price, discount) values ('apples', 3.5, 0.20);

select * from prod;