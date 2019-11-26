inversion_axe = False
neg_x = True
neg_y = True
x_diff = 141
y_diff = -568
rapport = 0,38

def conversion_to_robot(dechets):
	
    t = []
    nbr = len(dechets)
    for i in range(nbr):
    
        t.append([])
        
        print("Traitement du déchet ", i)
        
        x1 = dechets[i][0]
        y1 = dechets[i][1]
        x2 = dechets[i][2]
        y2 = dechets[i][3]
        
        x1 = rapport * x1
        x2 = rapport * x2
        y1 = rapport * y1
        y2 = rapport * y2
        
        if (inversion_axe) :
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if (neg_x) :
            x1 = -1 * x1
            x2 = -1 * x2
        
        if (neg_y) :
            y1 = -1 * y1
            y2 = -1 * y2
            
        x1 = x1 + x_diff
        x2 = x2 + x_diff
        y1 = y1 + y_diff
        y2 = y2 + y_diff
        
        
        
        
        
            
        t[i].append(x1)
        t[i].append(y1)
        t[i].append(x2)
        t[i].append(y1)
        
    return t