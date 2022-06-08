-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS category_post;
DROP TABLE IF EXISTS navigation;
DROP TABLE IF EXISTS navigation_post;
DROP TRIGGER IF EXISTS update_post_updated;
DROP TABLE IF EXISTS welcode;
DROP TABLE IF EXISTS uploadfile;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TRIGGER update_post_updated UPDATE OF updated ON post 
  BEGIN
    UPDATE post SET updated = CURRENT_TIMESTAMP WHERE id = old.id;
  END;
  
  
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE category_post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post (id),
    FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE navigation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL
);

CREATE TABLE navigation_post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    navigation_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post (id),
    FOREIGN KEY (navigation_id) REFERENCES navigation (id)
);

CREATE TABLE welcode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    welcode TEXT NOT NULL 
);

CREATE TABLE uploadfile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fpath TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE plugin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    script TEXT NOT NULL
);
create TABLE use_plugin(
    id INTEGER PRIMARY KEY AUTOINCREMENT,    
    post_id INTEGER NOT NULL,
    plugin_id INTEGER NOT NULL,    
    use INTEGER CHECK(use >=0 AND use <=1),
    FOREIGN KEY (post_id) REFERENCES post (id),
    FOREIGN KEY (plugin_id) REFERENCES plugin (id)
);
