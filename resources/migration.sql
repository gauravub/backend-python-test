BEGIN TRANSACTION;

DROP TABLE IF EXISTS _todos_old;
ALTER TABLE todos RENAME TO _todos_old;

CREATE TABLE todos
( id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INT(11) NOT NULL,
  description VARCHAR(255) NOT NULL,
  complete INT(1) NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO todos (user_id, description)
  SELECT user_id, description
  FROM _todos_old;

DROP TABLE _todos_old;

COMMIT;
