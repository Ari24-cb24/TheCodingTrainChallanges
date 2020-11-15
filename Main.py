from ReadmeReader import ReadmeParser
from pymongo import MongoClient
import requests

client = MongoClient("mongodb://localhost:27017/")
db = client.shiffman_challanges
challange_data = db.challange_data

def get_challange_most_contributions():
    elements = challange_data.find({}).sort("contributions")

    challanges = []
    for elem in elements:
        obj = elem.copy()
        obj["contributions"] = len(obj["contributions"])
        del obj["_id"]
        challanges.append(obj)

    challanges.sort(key=lambda elem: elem["contributions"], reverse=True)
    return challanges

def update_db():
    challange_data.delete_many({})

    r = requests.get("https://api.github.com/repos/CodingTrain/website/contents/_CodingChallenges")
    r2 = requests.get("https://api.github.com/repos/CodingTrain/website/contents/_challenges/coding-in-the-cabana")
    data = r.json()
    data2 = r2.json()

    data += data2

    del r
    del r2

    download_urls = []
    for challange in data:
        if not challange["name"] == "index.md":
            download_urls.append(challange["download_url"])

    del data
    del data2

    with requests.Session() as session:
        for i, url in enumerate(download_urls):
            print(i, "/", len(download_urls))
            r = session.get(url)
            data = r.text

            r = ReadmeParser(data)
            r.parse()

            challange_data.insert_one({
                "title": r.title,
                "video_number": r.video_number,
                "video_id": r.video_id,
                "youtube_url": "https://youtube.com/watch?v=" + r.video_id,
                "date": r.date,
                "contributions": r.contributions
            })


if __name__ == '__main__':
    # update_db()
    get_challange_most_contributions()