// Thanks to https://github.com/capnfabs/trackscan

use quick_xml::de::Deserializer;
use quick_xml::events::{BytesStart, Event};
use quick_xml::reader::Reader;
use quick_xml::writer::Writer;
use serde::Deserialize;
use std::env;
use std::io::BufRead;
use time::Instant;

fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let mut reader = Reader::from_file(&file_path).unwrap();

    let mut buf = Vec::new();
    let mut junk_buf: Vec<u8> = Vec::new();
    let mut count = 0;

    println!("Start");
    let start_time = Instant::now();

    loop {
        match reader.read_event_into(&mut buf) {
            Err(e) => panic!("Error at position {}: {:?}", reader.buffer_position(), e),
            Ok(Event::Eof) => break,
            Ok(Event::Start(e)) => match e.name().as_ref() {
                b"release" => {
                    let release_bytes =
                        read_to_end_into_buffer(&mut reader, &e, &mut junk_buf).unwrap();
                    let str = std::str::from_utf8(&release_bytes).unwrap();
                    let mut deserializer = Deserializer::from_str(str);
                    let release = Release::deserialize(&mut deserializer).unwrap();

                    process_release(&release);

                    count += 1;
                    if count % 10_000 == 0 {
                        println!("checked {} records\telapsed: {}", count, start_time.elapsed());
                    }
                }
                _ => (),
            },
            _ => (),
        }


        // clear buffer to avoid leaking memory
        buf.clear();
    }

    println!("End");

    println!("checked {} records. elapsed: {}", count, start_time.elapsed());

    Result::Ok(())
}

fn read_to_end_into_buffer<R: BufRead>(
    reader: &mut Reader<R>,
    start_tag: &BytesStart,
    junk_buf: &mut Vec<u8>,
) -> Result<Vec<u8>, quick_xml::Error> {
    let mut depth = 0;
    let mut output_buf: Vec<u8> = Vec::new();
    let mut w = Writer::new(&mut output_buf);
    let tag_name = start_tag.name();
    w.write_event(Event::Start(start_tag.clone()))?;
    loop {
        junk_buf.clear();
        let event = reader.read_event_into(junk_buf)?;
        w.write_event(&event)?;

        match event {
            Event::Start(e) if e.name() == tag_name => depth += 1,
            Event::End(e) if e.name() == tag_name => {
                if depth == 0 {
                    return Ok(output_buf);
                }
                depth -= 1;
            }
            Event::Eof => {
                panic!("oh no")
            }
            _ => {}
        }
    }
}

fn process_release(release: &Release) {
    //dbg!(release);
}

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
struct Release {
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
