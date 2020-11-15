import sys

def bRem(string):
    if string.endswith("\n"):
        string = string[:-2]
    if string.startswith("\""):
        string = string[1:]
    if string.endswith("\""):
        string = string[:-1]
    return string


class ReadmeParser:
    def __init__(self, content):
        self.__content = content.split("\n")

        self.title = None
        self.video_number = None
        self.video_id = None
        self.date = None
        self.contributions = []

    def parse(self):
        for i, line in enumerate(self.__content):
            if line.startswith("title"):
                self.title = bRem(line.split("title: ")[1].replace("\n", ""))
            elif line.startswith("video_number"):
                self.video_number = bRem(line.split("video_number: ")[1])
            elif line.startswith("date"):
                self.date = bRem(line.split("date: ")[1])
            elif line.startswith("video_id"):
                self.video_id = bRem(line.split("video_id: ")[1])
            elif line.startswith("contributions:"):
                for j in range(i+1, len(self.__content)):
                    if self.__content[j].lstrip().startswith("- title:"):
                        index = j+1
                        curLine = self.__content[index]

                        c = {
                            "title": bRem(self.__content[index - 1].lstrip().replace("- title: ", "")),
                            "author": {
                                "name": "",
                                "url": ""
                            },
                            "url": "",
                            "video_id": "",
                            "source": ""
                        }

                        while not curLine.lstrip().startswith("- title:"):
                            curLine = self.__content[index]

                            if curLine.lstrip().startswith("author"):
                                whiteSpaces = len(curLine) - len(curLine.lstrip())

                                index += 1
                                curLine = self.__content[index]

                                while len(curLine) - len(curLine.lstrip()) != whiteSpaces:
                                    curLine = self.__content[index]

                                    if len(curLine) - len(curLine.lstrip()) != whiteSpaces:
                                        if curLine.lstrip().startswith("name"):
                                            c["author"]["name"] = bRem(curLine.lstrip().split("name: ")[1].replace("\n", ""))
                                        elif curLine.lstrip().startswith("url"):
                                            c["author"]["url"] = bRem(curLine.lstrip().split("url: ")[1].replace("\n", ""))

                                        index += 1

                                index -= 1

                            elif curLine.lstrip().startswith("url"):
                                c["url"] = bRem(curLine.lstrip().split("url: ")[1].replace("\n", ""))
                            elif curLine.lstrip().startswith("video_id"):
                                c["video_id"] = bRem(curLine.lstrip().split("video_id: ")[1].replace("\n", ""))
                            elif curLine.lstrip().startswith("source"):
                                c["source"] = bRem(curLine.lstrip().split("source: ")[1].replace("\n", ""))
                            else:
                                break

                            index += 1

                        self.contributions.append(c)
                break

if __name__ == '__main__':
    filename = sys.argv[1]
    
    with open(filename, "r") as fh:
        content = fh.read()
    
    r = ReadmeParser(content)
    r.parse()