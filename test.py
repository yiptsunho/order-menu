import requests

BASE = "http://127.0.0.1:5000/"

# data = [
#     {'likes': 100, 'name': 'first video', 'views': 1000},
#     {'likes': 150, 'name': 'second video', 'views': 150},
#     {'likes': 1500, 'name': 'third video', 'views': 1500}
# ]
# for i in range(len(data)):
#     response = requests.post(BASE + "/video/" + str(i), data[i])
#     print(response.json())
# # response = requests.get(BASE + "/helloworld/jacky")
# # response = requests.post(BASE + "/video/1", {'likes': 100, 'name': 'first video', 'views': 1000})
# input()
# response = requests.delete(BASE + "/video/10")
# print(response.json())
# input()
# response = requests.get(BASE + "/video/1")
# print(response.json())
response = requests.get(BASE + "/records")
print(response.json())