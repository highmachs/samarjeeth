
with open(r'c:\MAINDOMAIN\Portfolio sites\p5\_nuxt\30d1d07.js', 'r', encoding='utf-8') as f:
    content = f.read()

index = content.find('.editorial__image')
if index != -1:
    snippet = content[index:index+300]
    with open(r'c:\MAINDOMAIN\Portfolio sites\p5\snippet.txt', 'w', encoding='utf-8') as f_out:
        f_out.write(snippet)
else:
    print("Not found")
