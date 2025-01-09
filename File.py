def get_filetype(name):
    a=list(name)
    a.reverse()
    a=a[:a.index('.')]
    a.reverse()
    a= "".join(a)
    return f'.{a}'

print(get_filetype("hola.com.app"))


