
CREATE TABLE users(
    user_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_code CHAR(12) UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);

INSERT INTO users(user_code, email)
    VALUES ('admin_user00', 'admin');

CREATE TABLE workout_log(
    workout_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id SMALLINT NOT NULL,
    "date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exercise VARCHAR(60) NOT NULL,
    "time" SMALLINT,
    "weight" SMALLINT,
    "sets" SMALLINT,
    reps SMALLINT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);