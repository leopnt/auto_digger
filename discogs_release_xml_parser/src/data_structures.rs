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
    pub fn insert_into_db(
        &self,
        conn: &mut PooledConn,
    ) -> std::result::Result<(), Box<dyn std::error::Error>> {
        // Insert tracks to the database
        let result: Result<Vec<usize>> = conn.exec(
            r"INSERT INTO MusicRelease (release_id, title, status, data_quality, date, country)
            VALUES (:release_id, :title, :status, :data_quality, :date, :country)",
            params! {
                "release_id" => self.id,
                "title" => &self.title,
                "status" => &self.status,
                "data_quality" => &self.data_quality,
                "date" => &self.date,
                "country" => &self.country
            },
        );

        match result {
            Err(e) => return Err(Box::new(e)),
            _ => (),
        };

        // Insert tracks to the database
        let result = conn.exec_batch(
            r"INSERT INTO Tracklist (title, release_id)
              VALUES (:title, :release_id)",
            self.tracklist.track.iter().map(|track| {
                params! {
                    "title" => &track.title,
                    "release_id" => self.id
                }
            }),
        );

        match result {
            Ok(_) => Ok(()),
            Err(e) => {
                // Revert temporary inserts. Since there is a Foreign Key on the
                // release on every table, we simply delete the current release
                // and it will cascade/propagate to other tables
                let result: Result<Vec<usize>> = conn.exec(
                    r"DELETE FROM MusicRelease
                    WHERE release_id = :release_id",
                    params! {
                        "release_id" => self.id
                    },
                );

                match result {
                    Err(e) => eprintln!("Couldn't revert temporary Release inserts ! {}", e),
                    _ => (),
                };

                // Return the source of the error
                Err(Box::new(e))
            }
        }
    }
}
