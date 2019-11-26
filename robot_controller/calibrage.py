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
# coordonnées
x = 0
y = -800
z = 100

RDK = Robolink()

# sélection du robot
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception('No robot selected or available')

# début du programme
print("------- Calibrage -------")
    
# move the robot to reference point:
print(Pose_2_TxyzRxyz(target_ref))
robot.MoveJ([90,-100,80,-70,-90,180])
robot.MoveJ(target_ref)

# paramètres du robot
robot.setPoseFrame(robot.PoseFrame())
robot.setPoseTool(robot.PoseTool())
robot.setZoneData(10)
robot.setSpeed(100)


target_i = Mat(target_ref)
pos_i = target_i.Pos()
            
# on se place au dessus du déchet
pos_i[0] = x
pos_i[1] = y
pos_i[2] = z
target_i.setPos(pos_i)
print(str(Pose_2_TxyzRxyz(target_i)))
robot.MoveL(target_i)

input("Press Enter to continue...")

# on pousse
pos_i[1] = -sqrt(R_2 - x*x - z*z)
target_i.setPos(pos_i)
print(str(Pose_2_TxyzRxyz(target_i)))
robot.MoveL(target_i)

input("Press Enter to continue...")

# on remonte
robot.MoveL(target_ref)

print('Done')