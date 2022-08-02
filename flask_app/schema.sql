DROP TABLE IF EXISTS endpoint;
DROP TABLE IF EXISTS user;

CREATE TABLE endpoint (
	id TEXT PRIMARY KEY,
	username TEXT NOT NULL,
	name TEXT UNIQUE NOT NULL,
	description TEXT,
	mac TEXT UNIQUE NOT NULL,
	category TEXT NOT NULL,
	register_date TEXT NOT NULL,
	FOREIGN KEY(username) REFERENCES user(username)

);


CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);