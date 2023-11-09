# import requests
# import json
# from bs4 import BeautifulSoup as bs
# import re
#
# response = requests.get("https://practice.geeksforgeeks.org/problem-of-the-day")
#
# soup = bs(response.content, 'html.parser')
# title_ = soup.find_all("h1")
# problem = soup.find('a', class_="problemOfTheDay_potd__zdG8c")
# my_div = soup.find(id='potd_solve_prob')
#
# print(my_div)
# # if problem:
#
#     # nested = problem.find("div", class_="problemOfTheDay_banner__jS7A7")
#     # if nested:
#     #     nested1 = nested.find("div", class_="problemOfTheDay_potd_banner__0FA1E")
#     #     if nested1:
#     #         nested2 = nested1.find("div", class_="problemOfTheDay_problem__gqINx")
#     #         # print(problem)
#
#
# # print(link)
# # title = title_[0].text
#
# # import requests
# # from bs4 import BeautifulSoup
# #
# # # Send an HTTP GET request to the URL
# # response = requests.get("https://practice.geeksforgeeks.org/problem-of-the-day")
# # soup = BeautifulSoup(response.content, 'html.parser')
# #
# # # Find the div containing the "Problem of the Day"
# # problem_divs = soup.find_all('div', class_='problemOfTheDay_banner__jS7A7')
# #
# # if problem_divs:
# #     problem_div = problem_divs[0]
# #
# #     # Extract the problem name from the h1 tag
# #     problem_name = problem_div.find('h1', class_='problemOfTheDay_potd_banner_heading__H0fpf').text.strip()
# #
# #     # Extract the problem link from the "Rulebook" link
# #     rulebook_link = problem_div.find('a', id='potd_rulebook')
# #
# #     if rulebook_link:
# #         rulebook_url = rulebook_link.get('href')
# #         print("Problem Name:", problem_name)
# #         print("Problem Link:", rulebook_url)
# #     else:
# #         print("Rulebook link not found.")
# #
# #     print("Problem Name:", problem_name)
# #     print("Problem Link:", rulebook_link)
# # else:
# #     print("Problem of the Day not found on the page")


from requests_html import HTMLSession
s = HTMLSession()
response = s.get("https://practice.geeksforgeeks.org/problem-of-the-day")
response.html.render()

print(response.content)