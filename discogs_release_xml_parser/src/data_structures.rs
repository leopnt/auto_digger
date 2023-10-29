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