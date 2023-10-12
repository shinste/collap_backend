-- CREATE TABLE base_user (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username VARCHAR(100),
--     password VARCHAR(100)
-- );

-- CREATE TABLE base_Event (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     event_id VARCHAR(8),
--     primary_date DATE,
--     name VARCHAR(100),
--     host_id INTEGER,
--     FOREIGN KEY (host_id) REFERENCES user(id)
-- );

-- CREATE TABLE base_EventDate (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     date DATE
-- );


CREATE TABLE base_user (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(100)
);

CREATE TABLE base_Event (
    event_id VARCHAR(8) PRIMARY KEY,
    primary_date DATE,
    name VARCHAR(100),
    host_id INTEGER,
    FOREIGN KEY (host_id) REFERENCES user(username)
);

CREATE TABLE base_Eventdate (
    event_id VARCHAR(8),
    date DATE,
    PRIMARY KEY (event_id, date),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);
DROP TABLE base_user;
DROP TABLE base_Event;
DROP TABLE base_EventDate;
DROP TABLE base_userevent;
-- SELECT * FROM base_Eventdate;

.tables


-- CREATE TABLE base_userevent (
--     event_id VARCHAR(8),
--     user_id INTEGER,
--     PRIMARY KEY (event_id, user_id),
--     FOREIGN KEY (event_id) REFERENCES event(event_id),
--     FOREIGN KEY (user_id) REFERENCES user(id)
-- );

CREATE TABLE base_userevent (
    event_id_id INTEGER,
    username_id VARCHAR(100),
    PRIMARY KEY (event_id_id, username_id),
    FOREIGN KEY (event_id_id) REFERENCES event(event_id),
    FOREIGN KEY (username_id) REFERENCES user(username)
);