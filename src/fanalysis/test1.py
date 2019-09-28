

class chk_1():

    def __init__(self, my_int):
        self.my_int = self.chk_int(my_int)
        try:
            self.chk_evendd(self.my_int)
        except:
            pass

    def chk_int(self, my_int):
        try:
            my_int  = int(my_int)
            if my_int >=1 and my_int <= 10:
                return my_int
            else:
                print('not between 1 and 10')
        except:
            print('must be integer') 

    
    def chk_evendd(self, x: int):
        if self.my_int % 2 == 0:
            print('even')
        elif self.my_int % 2 !=0:
            print('odd')
        else:
            print('wow what is goign on')




while 1==1:
    int_in = input('please input an integer from 1 to 10: ')
    chk_1(int_in)



