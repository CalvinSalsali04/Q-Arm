import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_idnetifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()


def pickup(): #retrieves container from pickup location
  arm.move_arm(0.532, 0.046, 0.04) #pickup location
  time.sleep(1) #time.sleep() function used throughout code to ensure the program pauses inbetween steps
  arm.control_gripper(40)
  time.sleep(1)
  arm.move_arm(0.406, 0.0, 0.483) #home coordinates


def rotate_Qbase(color): #function to rotate arm, checking potentiometer values and multiplying by full circle angle
  while arm.check_autoclave(color) == False:
    current_position = potentiometer.right()

    while potentiometer.left() == 0.5: #To rotate base we want left potentiometer to not be moving
      new_position = potentiometer.right()
      rotation_angle = 360*(current_position - new_position) # multiply the current from new postion by 360 degrees
      arm.rotate_base(rotation_angle)
      time.sleep(1)
      current_position = new_position #this allows the while loop to continue


def drop_off(color, container_id): #function checks potentiometer value matches size of container and places it accordingly
  list_coordinate = [(-0.597, 0.217, 0.282),(0.022, -0.635, 0.282), (0.0, 0.635, 0.282), (-0.387, 0.141, 0.138), (0.014, -0.411, 0.138), (0.0, 0.412, 0.138)] # list of coordinates for the different containers
  if container_id > 3:
    arm.activate_autoclaves() #autoclaves are only needed for large containers which have container_id > 3
  else:
    arm.deactivate_autoclaves() #deactivates autoclaves for small containers
    
  while arm.check_autoclave(color) == True: #only works if the arm is at the correct location
    if potentiometer.left() > 0.5 and potentiometer.left() < 1.0:

      if container_id <= 3: #moves small containers to top location between left potentiometer interval
        location = list_coordinate[container_id -1] #assigns the variable location with a coordinate
        arm.move_arm(location[0], location[1], location[2]) #arm moves the coordinate x,y,z
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        arm.home()
        break # this stops the loop and code will run to next part of the program


    elif potentiometer.left() == 1:

      if container_id <= 6: #moves large containers when left potentiometer is 1
        location = list_coordinate[container_id -1] #assigns the variable location with a coordinate
        arm.move_arm(location[0], location[1], location[2]) #arm moves the coordinate x,y,z
        arm.open_autoclave(color) #autoclave opens based off of autoclave color
        time.sleep(2)
        arm.control_gripper(-35)
        time.sleep(2)
        arm.home()
        arm.open_autoclave(color, False) #autoclave closes 
        break
       

def terminate(): #the main function that uses all previous functions and determines when program terminates 
  import random
  container_id_list = [1, 2, 3, 4, 5, 6]
  random.shuffle(container_id_list) #randomizes order of container_id_list
  for container_id in container_id_list:
    arm.home()
    arm.spawn_cage(container_id) #spawns the container
    if container_id == 1 or container_id == 4: #assigns each container_id to a color
      color = "red"
    elif container_id == 2 or container_id == 5: 
      color = "green"
    elif container_id == 3 or container_id == 6: 
      color = "blue"
    pickup()
    rotate_Qbase(color)
    drop_off(color, container_id)
  print("All containers have been placed!")
  return 
