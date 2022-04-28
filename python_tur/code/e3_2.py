#2.1 寫文字檔:
def out_txt(msg):
    print(msg)
    with open(f"./news_title.txt", 'a',encoding='utf-8') as the_file:
        the_file.write(str(msg))
        the_file.write('\n')

out_txt("a")        
out_txt("b")        
out_txt("c")        

