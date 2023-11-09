import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup as bs
from pytz import timezone
import re
import discord


def make_contest_embed(contest_name, contest_platform, contest_url, contest_time):
    embed = discord.Embed(url=contest_url, color=0xffd500)
    embed.add_field(name="Contest", value=contest_name, inline=False)
    embed.add_field(name="Platform", value=contest_platform, inline=False)
    embed.add_field(name="URL", value=contest_url, inline=False)
    embed.add_field(name="Time", value=contest_time, inline=False)
    return embed


def get_codeforces_contests():
    response = requests.get("https://codeforces.com/api/contest.list")
    codeforcesContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse["result"]
        for contest in contests:
            if contest["phase"] == "BEFORE":
                codeforcesContest = {"platform": "CodeForces", "contestName": contest["name"],
                                     "contestLink": "https://codeforces.com/contests/" + str(contest["id"]),
                                     "startTime": datetime.strftime(datetime.fromtimestamp(
                                         contest["startTimeSeconds"]), '%Y-%m-%dT%H:%M:%S') + '+0530',
                                     "contestDuration": "0" + \
                                                        str(contest["durationSeconds"] // 3600) + ":00 hours."}
                codeforcesContests.append(codeforcesContest)
    return [make_contest_embed(contest_name=contest["contestName"], contest_platform=contest["platform"], contest_url=contest["contestLink"], contest_time=contest["startTime"]) for contest in codeforcesContests]


def get_codechef_contests():
    response = requests.get("https://www.codechef.com/contests/")
    codechefContests = []
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        contests = soup.select(".content-wrapper > div")[0].find_all("tr")
        contests.pop(0)
        for contest in contests:
            elements = contest.select("td")
            elements.pop(0)
            codechefContest = {}
            codechefContest["platform"] = "CodeChef"
            codechefContest["contestName"] = elements[0].text.strip()
            codechefContest["contestLink"] = "https://www.codechef.com" + elements[0].select("a")[0].get("href")
            codechefContest["startTime"] = elements[1].get(
                "data-starttime").replace('+05:30', '+0530')
            start = datetime.strptime(
                codechefContest["startTime"][0: codechefContest["startTime"].index('+')], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(elements[2].get(
                "data-endtime")[0:elements[2].get("data-endtime").index("+")], '%Y-%m-%dT%H:%M:%S')
            td = (end - start)
            totalSeconds = td.total_seconds()
            days = int(totalSeconds // 86400)
            remainingSeconds = totalSeconds % 86400
            hours = int(remainingSeconds // 3600)
            remainingSeconds = remainingSeconds % 3600
            minutes = int(remainingSeconds // 60)
            dayPresent = False
            hourPresent = False
            contestDuration = ""
            if days:
                dayPresent = True
                contestDuration += str(days) + " Days"
            if hours:
                if dayPresent:
                    contestDuration += ", "
                contestDuration += str(hours) + " Hours"
                hourPresent = True
            if minutes:
                if hourPresent or dayPresent:
                    contestDuration += ", "
                contestDuration += str(minutes) + " Minutes"
            contestDuration += "."
            codechefContest["contestDuration"] = contestDuration

            codechefContests.append(codechefContest)
    return [make_contest_embed(contest_name=contest["contestName"], contest_platform=contest["platform"], contest_url=contest["contestLink"], contest_time=contest["startTime"]) for contest in codechefContests]


def get_at_coder_contests():
    response = requests.get("https://atcoder.jp/contests/")
    atCoderContests = []
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        contests = soup.select("#contest-table-upcoming tbody tr")
        for contest in contests:
            elements = contest.find_all("td")
            atCoderContest = {"platform": "AtCoder",
                              "contestName": elements[1].text.strip()[elements[1].text.strip().index(
                                  "\n") + 1:],
                              "contestLink": "https://atcoder.jp" + elements[1].select("a")[0].get("href"),
                              "startTime": datetime.strptime(elements[0].text.replace(
                                  " ", "T"), '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Asia/Kolkata')).strftime(
                                  '%Y-%m-%dT%H:%M:%S%z'), "contestDuration": elements[2].text + " hours."}
            atCoderContests.append(atCoderContest)
    return [make_contest_embed(contest_name=contest["contestName"], contest_platform=contest["platform"], contest_url=contest["contestLink"], contest_time=contest["startTime"]) for contest in atCoderContests]


def get_hackerearth_contests():
    response = requests.get(
        "https://www.hackerearth.com/chrome-extension/events/")
    hackerearthContests = []
    if response.status_code == 200:
        jsonResponse = json.loads(response.text)
        contests = jsonResponse["response"]
        for contest in contests:
            hackerearthContest = {}
            hackerearthContest["platform"] = "HackerEarth"
            if contest["status"] == "UPCOMING":
                hackerearthContest["contestName"] = contest["title"]
                hackerearthContest["contestLink"] = contest["url"]
                start = contest["start_tz"][0: contest["start_tz"].rindex(
                    ':')] + contest["start_tz"][contest["start_tz"].rindex(':') + 1:]
                start = start.replace(" ", "T")
                end = contest["end_tz"].replace(" ", "T")
                try:
                    hackerearthContest["startTime"] = datetime.strptime(
                        start, '%Y-%m-%dT%H:%M:%S%z').astimezone(timezone('Asia/Kolkata')).strftime(
                        '%Y-%m-%dT%H:%M:%S%z')
                    td = datetime.strptime(
                        end, '%Y-%m-%dT%H:%M:%S%z') - datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
                    if td.days and td.seconds:
                        hackerearthContest["contestDuration"] = str(
                            td.days) + " Days & " + str((td.seconds) // 3600) + " hours."
                    elif td.days:
                        hackerearthContest["contestDuration"] = str(
                            td.days) + " Days"
                    elif td.seconds and td.seconds > 3600:
                        hours = ""
                        mins = ""
                        if (td.seconds) // 3600 < 10:
                            hours = "0" + str((td.seconds) // 3600)
                        else:
                            hours = (td.seconds) // 3600
                        if ((td.seconds) // 60) % 60 < 10:
                            mins = "0" + str(((td.seconds) // 60) % 60)
                        else:
                            mins = ((td.seconds) // 60) % 60
                        hackerearthContest["contestDuration"] = hours + \
                                                                ":" + mins + " hours."
                    if hackerearthContest["contestDuration"]:
                        hackerearthContests.append(hackerearthContest)
                except:
                    continue
    return [make_contest_embed(contest_name=contest["contestName"], contest_platform=contest["platform"], contest_url=contest["contestLink"], contest_time=contest["startTime"]) for contest in hackerearthContests if contest]


def get_leetcode_contests():
    url = "https://leetcode.com/contest/"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    soup = bs(response.content, 'html.parser')
    contest_divs = soup.find_all('a', class_='h-full w-full')

    contests = []

    for contest_div in contest_divs[:2]:
        match = re.search(r'href="([^"]*)"', str(contest_div))
        if match:
            contest_link = "https://leetcode.com/" + match.group(1)
            contest_name = contest_div.text.strip()

            match_time = re.search(r'(\d+:\d+ [APM]{2})', contest_name)

            if match_time:
                start_time = match_time.group(0)
            else:
                start_time = "N/A"
            contests.append({
                "platform": "LeetCode",
                "contestName": contest_name,
                "contestLink": contest_link,
                "startTime": start_time,
            })

    return [make_contest_embed(contest_name=contest["contestName"], contest_platform=contest["platform"], contest_url=contest["contestLink"], contest_time=contest["startTime"]) for contest in contests]


if __name__ == "__main__":
    print(get_codeforces_contests())
    # print(getCodechefContests())
    print(get_at_coder_contests())
    print(get_hackerearth_contests())
    print(get_leetcode_contests())
