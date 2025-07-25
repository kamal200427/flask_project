word="donkey"
with open("kamal.txt") as f:
    s=f.read()
content=s.replace(word,"****")
with open("kamal.txt","w") as f:
   f.write(s)
 