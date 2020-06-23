#!/usr/bin/env python
import datetime
import json

import youtube_dl
import slugify


DEFAULT_LANGUAGE = "rus"
DEFAULT_SILENT_MODE = False
DEFAULT_URLS_LIST_FILENAME = "urls.list"


JSON_FORMAT_KWARGS = {
    "indent": 2,
    "separators": (",", ": "),
    "sort_keys": True,
    "ensure_ascii": False,
}


def main():
    list_filename = DEFAULT_URLS_LIST_FILENAME
    urls = filter(None, map(str.strip, open(list_filename).readlines()))
    videos_meta = filter(None, sum((get_entries(u) for u in urls), []))
    for meta in videos_meta:
        prepared_meta = get_prepared_meta(meta)
        filename = generate_filename(meta)
        with open(filename, "w", encoding="utf8") as json_file:
            json.dump(prepared_meta, json_file, **JSON_FORMAT_KWARGS)


def get_entries(url):
    youtube = youtube_dl.YoutubeDL({"ignoreerrors": True})
    data = youtube.extract_info(url, download=False)
    return data.get("entries") or [data]


def get_prepared_meta(data):
    meta = {
        "copyright_text": data["license"],
        "description": extract_decsription(data),
        "duration": data["duration"],
        "language": DEFAULT_LANGUAGE,
        "recorded": extract_date_recorded(data),
        "related_urls": [
            {"label": "GitHub", "url": "https://github.com/minskpython"},
        ],
        "speakers": list(extract_speakers(data)),
        "tags": ["minsk", "belarus"],
        "thumbnail_url": extract_thumbnail_url(data),
        "title": extract_title(data),
        "videos": [{"type": "youtube", "url": data["webpage_url"]}],
    }
    return meta


def generate_filename(data):
    filename = "%s-%s-%s.json" % (
        extract_date_recorded(data),
        slugify.slugify(extract_title(data)),
        slugify.slugify("-".join(extract_speakers(data))),
    )
    return filename


def extract_decsription(data):
    separator = "Присоединяйся к нам!"
    return sanitize(data["description"].split(separator)[0])


def extract_date_recorded(data):
    # date detection logic needs improvement
    splitter = "Python Meetup"
    title = data["title"]
    date_str = title.split(splitter)[-1].split("]")[0].strip()
    year, month, day = date_str[-4:], date_str[3:5], date_str[:2]
    upload_date = datetime.date(*map(int, (year, month, day)))
    return upload_date.isoformat()


def extract_title(data):
    # TODO: use smart regex here
    raw_title = data["title"]
    title_parts = raw_title.split("/")
    title_position_index = 0
    if len(title_parts) > 1:
        extracted_title = title_parts[title_position_index]
        return sanitize(extracted_title)
    return sanitize(raw_title)


def extract_speakers(data):
    # TODO: use smart regex here
    speaker_names = []
    title = data["title"]
    title_parts = title.split("/")
    speaker_name_position_index = 1
    if len(title_parts) > 1:
        speaker_names.append(
            sanitize(title_parts[speaker_name_position_index])
        )
    return speaker_names


def extract_thumbnail_url(data):
    thumbnail_candidate = data["thumbnail"]
    if "hqdefault" in thumbnail_candidate:
        if "?sqp" not in thumbnail_candidate:
            # hqdefault image without '?sqp' modifier isn't so good
            # trying to get more suitable thumbnail...
            thumbnail_candidate = data["thumbnails"][-1]["url"]
    return thumbnail_candidate


def sanitize(title_substring):
    return title_substring.replace("\u200b", "").strip()


if __name__ == "__main__":
    main()
