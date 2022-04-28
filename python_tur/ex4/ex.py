import re
continue_link=re.search("\d+", "javascrt:abc(123,456);").group(0)
print(continue_link)