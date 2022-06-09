from bs4 import BeautifulSoup
import urllib.request
import csv


def traveling_checker(func):
    traveled = []

    def inner(*args):
        target = args[0]
        count = args[1]
        writer = args[2]
        if target not in traveled:
            traveled.append(target)
            result = func(target, count, writer)
            return result
        return []

    return inner


@traveling_checker
def travel_link(target_link: str, write: csv.writer, count: int) -> list:
    with urllib.request.urlopen(target_link) as url:
        doc = url.read()
        soup = BeautifulSoup(doc, "html.parser")
        if not count:
            write.writerow([target_link])
            return [target_link]
        count = count - 1
        body_content = soup.find('div', id='mw-content-text')
        links = body_content.find_all('a')

        result_lists = []
        for link in links:
            if link.get('href'):
                try:
                    path = "https://en.wikipedia.org" + link['href']
                    travel_links = travel_link(path, write, count)
                    if travel_links:
                        result_lists += travel_links

                except:
                    print("wrong path", link['href'])

        return result_lists


class Craw:
    def __init__(self, depth: int = 3):
        self.target_url = ""
        self.target_name = ""
        self.depth = depth

    def set_target(self, target: str):
        self.target_name = target
        self.target_url = "https://en.wikipedia.org/wiki/" + target

    def traveling(self):
        print("travleing start")
        if self.target_url:
            with open(self.target_name + '.csv', 'w') as file:
                write = csv.writer(file)
                links = travel_link(self.target_url, write, self.depth)
                print(links)
                print(len(links))
        else:
            print("Need to set target!!")


class Worker:
    def __init__(self, depth: int, targets: list):
        self.claw = Craw(depth)
        self.targets = targets

    def working(self):
        for target in self.targets:
            print(target)
            self.claw.set_target(target)
            self.claw.traveling()


if __name__ == "__main__":
    worker = Worker(2, ["FIFA_World_Cup", "2022_FIFA_World_Cup"])
    worker.working()
