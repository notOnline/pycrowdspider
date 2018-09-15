# from helper import db, filehelper
# from downloader import downloader
# from bs4 import BeautifulSoup
# import config, re
# import json
#
# book_ids = set()
# # all = open('D:/book_briefs.json', 'r', encoding='utf-8').readlines()
# all = list(db.book_details.find())
# i = 0
# for item in all:
#     i = i + 1
#     print(i)
#     book_id = item['book_id']
#     if book_id in book_ids:
#         db.new_book_details_1.insert_one(item)
#     else:
#         db.new_book_details.insert_one(item)
#         book_ids.add(book_id)
# #     new_book_brief = None
# #     for book_id in book_ids:
# #         if item['book_id'] == book_id:
# #             new_book_brief = item
# #             break
# #
# #     if new_book_brief is None:
# #         new_book_brief = {}
# #         new_book_brief['book_id'] = book_id
# #         new_book_brief['href'] = url
# #         new_book_brief['tags'] = []
# #         new_book_brief['pic'] = book_brief['pic']
# #         new_book_brief['name'] = book_brief['name']
# #         new_book_brief['pub'] = book_brief['pub']
# #         new_book_brief['rating_nums'] = book_brief['rating_nums']
# #         new_book_brief['comment_nums'] = book_brief['comment_nums']
# #         new_book_brief['brief_content'] = book_brief['brief_content']
# #     new_book_brief['tags'].append(book_brief['tag_name'])
# #     new_book_briefs.append(new_book_brief)
# #
# # db.new_book_briefs.insert_many(new_book_briefs)
