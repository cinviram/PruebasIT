from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def verificar_num_likes(like):
  try:
    like = int(like)
  except Exception as e:
    like = 0
  return like

def get_id_father(href):
  split = href.split("/")
  return split[6]

driver = webdriver.Firefox()
driver.get("https://www.instagram.com/p/B166OkVBPJR/")

load_more_comment = driver.find_element_by_class_name('dCJp8')
load_more_comment.click()
# print(load_more_comment)
# content = driver.find_element_by_css_selector(".P9YgZ div.C4VMK>span").text
# caption = content.replace('\n', ' ').strip().rstrip()

id_post = "B166OkVBPJR"
data = []
def extraer_comentarios(driver, data, comment_origin = True):
  if comment_origin:
    comments = driver.find_elements_by_class_name('Mr508')
  else:
    comments = driver.find_elements_by_class_name('ZyFrc')

  for c in comments:
    container = c.find_element_by_class_name('C4VMK')
    username = container.find_element_by_class_name('_6lAjh').text
    content = container.find_element_by_tag_name('span').text
    content = content.replace('\n', ' ').strip().rstrip()
    status_container = container.find_element_by_class_name('_7UhW9')
    date = status_container.find_element_by_css_selector('a.gU-I7>time').get_attribute("title")
    likes = status_container.find_element_by_css_selector('button.FH9sR').text.split(" ")[0]
    like = verificar_num_likes(likes)
    id_father_container = status_container.find_element_by_css_selector("a.gU-I7").get_attribute("href")
    id_father = get_id_father(id_father_container)

    try:
      button_reply = c.find_element_by_css_selector("button.yWX7d")
      button_reply.click()
      replies_container = c.find_element_by_css_selector("ul.TCSYW")
      extraer_comentarios(replies_container, data, comment_origin = False)
      print("SI hay replies")
    except Exception as e:
      print("NO TIENE REPLIES")

    data_comment = [id_post, content, date, like, id_father, 0, username]
    data.append(data_comment)

    # user_id_father.append(id_father)
    # user_names.append(name)
    # user_comments.append(content)
    # user_dates.append(date)
    # user_likes.append(like)

extraer_comentarios(driver, data)
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ['Post', 'Caption', 'Date', 'likes', 'id_father', 'id_child', 'username']) 
  
# print dataframe.
print(df)

driver.close()





