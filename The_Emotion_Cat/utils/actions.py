'''
A set of functions that provide a set of movements corresponding to 
seven emotions. 
'''

from utils.Point import Point

def angry():
    '''
    Returns a list of movements corresponding to the "angry" emotion.
    '''
    p1 = Point(8, 6)
    p2 = Point(1, 6)
    t1 = Point(10, 2)
    t2 = Point(80, 2)
    h1 = (45, 45, 1)
    h2 = (80, 60, 1)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
        [p1, p2, p1, p1, t2, h2],
        [p1, p2, p1, p1, t1, h2],
        [p1, p2, p1, p1, t2, h2],
        [p1, p2, p1, p1, t1, h1],
            ] 
            
    return move_list

def disgusted():
    '''
    Returns a list of movements corresponding to the "disgusted" emotion.
    '''
    p1 = Point(4.5, 8.5)
    p2 = Point(2, 7)
    t1 = Point(10, 1)
    h1 = (44, 44, 1)
    h2 = (70, 62, 4)
    h3 = (70, 30, 4)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
        [p2, p2, p2, p2, t1, h1],
        [p2, p2, p2, p2, t1, h2],
        [p2, p2, p2, p2, t1, h3],
        [p2, p2, p2, p2, t1, h2],
        [p2, p2, p2, p2, t1, h3],
            ]
            
    return move_list

def fearful():
    '''
    Returns a list of movements corresponding to the "fearful" emotion.
    '''
    p1 = Point(3, 7)
    p2 = Point(1, 8)
    t1 = Point(10, 1)
    t2 = Point(60, 2)
    h1 = (45, 45, 1)
    h2 = (80, 80, 5)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
        [p2, p2, p2, p2, t2, h2],
            ] 
            
    return move_list

def happy():
    '''
    Returns a list of movements corresponding to the "happy" emotion.
    '''
    p1 = Point(2.5, 6.5)
    p2 = Point(8, 7)
    p3 = Point(1, 8)
    t1 = Point(10, 1)
    h1 = (45, 45, 1)
    h2 = (30, 45, 1)
    
    move_list = [
        [p1, p2, p1, p2, t1, h1],
        [p1, p3, p1, p2, t1, h2],
            ] 
            
    return move_list
  
def neutral():
    '''
    Returns a list of movements corresponding to the "neutral" emotion.
    '''
    p1 = Point(1, 5)
    t1 = Point(10, 1)
    h1 = (45, 45, 1)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
            ]
            
    return move_list
    
def sad():
    '''
    Returns a list of movements corresponding to the "sad" emotion.
    '''
    p1 = Point(1, 5)
    t1 = Point(10, 1)
    h1 = (45, 45, 1)
    h2 = (80, 45, 1)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
        [p1, p1, p1, p1, t1, h2],
            ]
            
    return move_list
    
def surprised():
    '''
    Returns a list of movements corresponding to the "surprised" emotion.
    '''
    p1 = Point(4.5, 8.5)
    t1 = Point(10, 1)
    t2 = Point(45, 2)
    h1 = (45, 45, 1)
    h2 = (50, 70, 5)
    
    move_list = [
        [p1, p1, p1, p1, t1, h1],
        [p1, p1, p1, p1, t2, h2],
            ]
            
    return move_list
    
