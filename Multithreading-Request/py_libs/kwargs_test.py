def func(**kwargs):
    print(kwargs)


a = {
    'a' : 1,
    'b' : 2
    }

func(**a)
def func2(*args):
    print args

a = [1,2,3]

func2(*a)
