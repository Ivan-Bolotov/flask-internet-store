CREATE TABLE IF NOT EXISTS Users
(
    id       INT  NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL CHECK (username != ''),
    password TEXT NOT NULL CHECK (password != '')
);