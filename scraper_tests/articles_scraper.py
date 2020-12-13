import requests

response = requests.get("https://starofmysore.com/category/feature-articles/").text

blogs = response.split("<div class=\"standard_blog\">")[1].split("class=\"alaya_pagenavi\"")[0]

for blog in blogs.split("<article class")[1:]:
    link = blog.split("href=")[1][:blog.split("href=")[1].index("\">")].strip("\"")
    title = blog.split("title=")[2][blog.split("title=")[2].index("\">")+2:].split("</a></h4>")[0]
    date = blog.split("<span class=\"category\">")[2][:blog.split("<span class=\"category\">")[2].index("</span>")]
    thumbnail = blog.split("<img width=")[1].split("src=")[1][:blog.split("<img width=")[1].split("src=")[1].index("class=")].strip().strip("\"")
    description = blog.split("<p>")[-1].split("</p>")[0]
    print(f"""{title}
Link: {link}
Date: {date}
Image: {thumbnail}
{description}
""")    

# print(blogs)
