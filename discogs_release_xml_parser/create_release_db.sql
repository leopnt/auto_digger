CREATE TABLE IF NOT EXISTS MusicRelease (
    release_id INT PRIMARY KEY,
    title VARCHAR(255),
    status VARCHAR(255),
    data_quality VARCHAR(255),
    year INT,
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Artist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    artist_id INT,
    release_id INT,
    name VARCHAR(255),
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS MusicLabel (
    id INT PRIMARY KEY AUTO_INCREMENT,
    label_id INT,
    release_id INT,
    catno VARCHAR(255),
    name VARCHAR(255),
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS MusicGenre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    release_id INT,
    name VARCHAR(255),
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS MusicStyle (
    id INT PRIMARY KEY AUTO_INCREMENT,
    release_id INT,
    name VARCHAR(255),
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS MusicFormat (
    id INT PRIMARY KEY AUTO_INCREMENT,
    release_id INT,
    name VARCHAR(255),
    qty INT,
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS Tracklist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    release_id INT,
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS Video (
    id INT PRIMARY KEY AUTO_INCREMENT,
    release_id INT,
    title VARCHAR(255),
    duration INT,
    url VARCHAR(255),
    FOREIGN KEY (release_id) REFERENCES MusicRelease(release_id) ON DELETE CASCADE ON UPDATE RESTRICT
);