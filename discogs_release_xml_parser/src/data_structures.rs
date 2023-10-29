use mysql::prelude::*;
use mysql::*;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Artists {
    #[serde(default)]
    artist: Vec<Artist>,
}

#[derive(Debug, Deserialize)]
struct Artist {
    id: usize,
    name: String,
}

#[derive(Debug, Deserialize)]
struct Labels {
    #[serde(default)]
    label: Vec<Label>,
}

#[derive(Debug, Deserialize)]
struct Label {
    #[serde(rename = "@id")]
    id: usize,
    #[serde(rename = "@catno")]
    catno: String,
    #[serde(rename = "@name")]
    name: String,
}

#[derive(Debug, Deserialize)]
struct Formats {
    #[serde(default)]
    format: Vec<Format>,
}

#[derive(Debug, Deserialize)]
struct Format {
    #[serde(rename = "@name")]
    name: String,
    #[serde(rename = "@qty")]
    qty: usize,
}

#[derive(Debug, Deserialize)]
struct Genres {
    #[serde(default)]
    genre: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct Styles {
    #[serde(default)]
    style: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct Tracklist {
    #[serde(default)]
    track: Vec<Track>,
}

#[derive(Debug, Deserialize)]
struct Track {
    title: String,
}

#[derive(Debug, Deserialize)]
struct Videos {
    #[serde(default)]
    video: Vec<Video>,
}

#[derive(Debug, Deserialize)]
struct Video {
    title: String,
    #[serde(rename = "@duration")]
    duration: usize,
    #[serde(rename = "@src")]
    src: String,
}

#[derive(Debug, Deserialize)]
pub struct Release {
    #[serde(rename = "@id")]
    id: usize,
    #[serde(rename = "@status")]
    status: String,
    data_quality: String,
    title: String,
    country: Option<String>,
    #[serde(rename = "released")]
    date: Option<String>,
    artists: Artists,
    labels: Labels,
    formats: Formats,
    genres: Option<Genres>,
    styles: Option<Styles>,
    tracklist: Tracklist,
    videos: Option<Videos>,
}

impl Release {
    pub fn insert_into_db(&self, conn: &mut PooledConn) -> std::result::Result<(), mysql::Error> {
        let result: Result<Vec<usize>> = conn.exec(
            r"INSERT INTO MusicRelease (release_id, title, status, data_quality, year, country)
            VALUES (:release_id, :title, :status, :data_quality, :year, :country)",
            params! {
                "release_id" => self.id,
                "title" => &self.title,
                "status" => &self.status,
                "data_quality" => &self.data_quality,
                "year" => match &self.date {
                    Some(date) => Some(&date[0..4]), // extract year from date
                    None => None
                },
                "country" => &self.country
            },
        );
        if let Err(e) = result {
            return Err(e);
        }

        self.insert_tracks(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_genres(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_styles(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_artists(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_labels(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_formats(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        self.insert_videos(conn).or_else(|e| {
            self.undo_insert(conn);
            Err(e)
        })?;

        Ok(())
    }

    fn insert_tracks(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        conn.exec_batch(
            r"INSERT INTO Tracklist (title, release_id)
              VALUES (:title, :release_id)",
            self.tracklist.track.iter().map(|track| {
                params! {
                    "title" => &track.title,
                    "release_id" => self.id
                }
            }),
        )
    }

    fn insert_genres(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        if let Some(genres) = &self.genres {
            conn.exec_batch(
                r"INSERT INTO MusicGenre (name, release_id)
                VALUES (:name, :release_id)",
                genres.genre.iter().map(|name| {
                    params! {
                        "name" => &name,
                        "release_id" => self.id
                    }
                }),
            )?;
        }

        Ok(())
    }

    fn insert_styles(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        if let Some(styles) = &self.styles {
            conn.exec_batch(
                r"INSERT INTO MusicStyle (name, release_id)
                VALUES (:name, :release_id)",
                styles.style.iter().map(|name| {
                    params! {
                        "name" => &name,
                        "release_id" => self.id
                    }
                }),
            )?;
        }

        Ok(())
    }

    fn insert_artists(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        conn.exec_batch(
            r"INSERT INTO Artist (artist_id, name, release_id)
              VALUES (:artist_id, :name, :release_id)",
            self.artists.artist.iter().map(|artist| {
                params! {
                    "artist_id" => artist.id,
                    "name" => &artist.name,
                    "release_id" => self.id
                }
            }),
        )
    }

    fn insert_labels(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        conn.exec_batch(
            r"INSERT INTO MusicLabel (label_id, name, catno, release_id)
              VALUES (:label_id, :name, :catno, :release_id)",
            self.labels.label.iter().map(|label| {
                params! {
                    "label_id" => label.id,
                    "name" => &label.name,
                    "catno" => &label.catno,
                    "release_id" => self.id
                }
            }),
        )
    }

    fn insert_formats(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        conn.exec_batch(
            r"INSERT INTO MusicFormat (name, qty, release_id)
              VALUES (:name, :qty, :release_id)",
            self.formats.format.iter().map(|format| {
                params! {
                    "name" => &format.name,
                    "qty" => &format.qty,
                    "release_id" => self.id
                }
            }),
        )
    }

    fn insert_videos(&self, conn: &mut PooledConn) -> Result<(), mysql::Error> {
        if let Some(videos) = &self.videos {
            conn.exec_batch(
                r"INSERT INTO Video (title, duration, url, release_id)
              VALUES (:title, :duration, :url, :release_id)",
                videos.video.iter().map(|video| {
                    params! {
                        "title" => &video.title,
                        "duration" => video.duration,
                        "url" => &video.src,
                        "release_id" => self.id
                    }
                }),
            )?
        }

        Ok(())
    }

    fn undo_insert(&self, conn: &mut PooledConn) {
        // Undo temporary inserts. Since there is a Foreign Key on the
        // release on every table, we simply delete the current release
        // and it will cascade/propagate to other tables
        let result: Result<Vec<usize>> = conn.exec(
            r"DELETE FROM MusicRelease
                        WHERE release_id = :release_id",
            params! {
                "release_id" => self.id
            },
        );

        if let Err(e) = result {
            panic!(
                "Couldn't revert temporary Release inserts on release_id={}: {}",
                self.id, e
            );
        }
    }
}
