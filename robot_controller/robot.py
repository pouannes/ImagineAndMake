from robolink import *
from robodk import *

# position de départ
target_ref = TxyzRxyz_2_Pose([165, -550, 835, 3.141592653589793, 0, 0])
pos_ref = target_ref.Pos()
x_ref = pos_ref[0]
y_ref = pos_ref[1]
z_ref = pos_ref[2]
# rayon de la boule
R = 1300
R_2 = R * R
# rayon du cylindre central
C = 450
C_2 = C * C
# hauteur du tapis
z_tapis = 0
# rayon du demi-disque accessible
r_acces = sqrt((R_2 - z_tapis*z_tapis) / 2)

def ini_robot() :
    RDK = Robolink()

    # sélection du robot
    robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
    if not robot.Valid():
        raise Exception('No robot selected or available')
    
    return robot
    
def tri_dechet(dechets) :
    robot = ini_robot()
    
    # début du programme
    print("------- Tri des déchets -------")
    
    # move the robot to reference point:
    print(Pose_2_TxyzRxyz(target_ref))
    robot.MoveJ([90,-100,80,-70,-90,180])
    robot.MoveJ(target_ref)

    # paramètres du robot
    robot.setPoseFrame(robot.PoseFrame())
    robot.setPoseTool(robot.PoseTool())
    robot.setZoneData(10)
    robot.setSpeed(100)

    # nombre de déchets à traiter
    nbr = len(dechets)

    for i in range(nbr):
        
        print("Traitement du déchet ", i)
        
        traitable = False
        x1 = dechets[i][0]
        y1 = dechets[i][1]
        x2 = dechets[i][2]
        y2 = dechets[i][3]
        cat = dechets[i][4]
        x = (x1 + x2)/2
        y = (y1 + y2)/2
        z = z_ref
        longueur = abs(y1 - y2)
        benne = 0
        
        if (cat == 1) : # béton
            benne = 1
            y = y + longueur
        elif (cat == 2) : # acier
            benne = 2
            y = y - longueur
        else :
            benne = 3
        
        if (abs(y) > C and abs(y) < r_acces and abs(x) < r_acces and y < 0) :
            # on se trouve dans la bande accessible
            traitable = True
            z_sphere = sqrt(R_2 - x*x - y*y)
            if (z_sphere < z) :
                # on diminue la position z avant descente
                z = z_sphere
        
        if (benne > 2) :
            traitable = False
        
        if (traitable) :
            target_i = Mat(target_ref)
            pos_i = target_i.Pos()
            
            # on se place au dessus du déchet
            pos_i[0] = x
            pos_i[1] = y
            pos_i[2] = z
            target_i.setPos(pos_i)
            print(str(Pose_2_TxyzRxyz(target_i)))
            robot.MoveL(target_i)
            
            # on descend
            pos_i[2] = z_tapis
            target_i.setPos(pos_i)
            print(str(Pose_2_TxyzRxyz(target_i)))
            robot.MoveL(target_i)
            
            # on pousse le déchet
            if (benne == 1) :
                y_benne = -sqrt(R_2 - x*x - z_tapis*z_tapis)
            else :
                y_benne = -C
            pos_i[1] = y_benne
            target_i.setPos(pos_i)
            print(str(Pose_2_TxyzRxyz(target_i)))
            robot.MoveL(target_i)
            
            # on remonte
            robot.MoveL(target_ref)
        else :
            if (benne > 2) :
                print("-> Ce déchet va dans la benne en bout de tapis")
            else :
                print("-> Ce déchet n'est pas accessible")

    print('Done')