\set db_name `echo $GIDEON_DATABASE`
\set db_user `echo $GIDEON_USER`
DROP DATABASE IF EXISTS :db_name;
CREATE DATABASE :db_name WITH OWNER :db_user;
\c :db_name

BEGIN;

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  description TEXT NOT NULL
);
CREATE INDEX categories_name_index ON categories(name);

CREATE TABLE tags (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL
);
CREATE INDEX tags_name_index ON tags(name);

CREATE TABLE movements (
  id SERIAL PRIMARY KEY,
  type VARCHAR(20) NOT NULL,
  category_id INTEGER REFERENCES categories NOT NULL,
  date DATE NOT NULL,
  value NUMERIC(10, 2) NOT NULL CONSTRAINT movements_value_check CHECK (value > 0),
  note TEXT
);
CREATE INDEX movements_type_index ON movements(type);
CREATE INDEX movements_category_index ON movements(category_id);
CREATE INDEX movements_date_index ON movements(date);


CREATE TABLE movements_tags (
  id SERIAL PRIMARY KEY,
  tag_id INTEGER REFERENCES tags NOT NULL,
  movement_id INTEGER REFERENCES movements NOT NULL
);

COMMIT;
