import os
from os import path as osp
import numpy as np
import matplotlib.pyplot as plt
import cv2
from renderer.DepthRender import TacRender


if __name__ == "__main__":
    # load object
    # YCB
    obj_name = "006_mustard_bottle"
    obj_path = osp.join("..", "data", obj_name, "google_512k", "nontextured.stl")
    # Google Scan
    # obj_name = "Threshold_Porcelain_Pitcher_White"
    # obj_path = osp.join("..", "data", obj_name, "meshes", "model.obj")

    # load digit
    gel_path = osp.join("..", "calibs_digit", "gel_surface_m.thin.obj")
    # load calibration for taxim
    calib_path = osp.join("..", "calibs_digit")
    # save results
    save_path = osp.join("..", "results", "tests")

    # whether use live render or offline render
    live = True
    # live = False

    tacRender = TacRender(obj_path, gel_path, calib_path, 'digit')
    # define pressing depth
    press_depth = 0.0010 # in meter
    # define contact orientation range
    shear_range = 15.0
    # define contact vertex
    vertex_idx = 242768

    theta = np.radians(shear_range)
    z = np.random.uniform(low=np.cos(theta),high=1.0,size=(1,))[0]
    phi = np.random.uniform(low=0.0,high=2*np.pi,size=(1,))[0]
    z_axis = np.array([np.sqrt(1-z**2)*np.cos(phi), np.sqrt(1-z**2)*np.sin(phi), z])

    tacRender.update_pose(vertex_idx, press_depth, z_axis)
    if live == True:
        tacRender.live_render()
    else:
        depth = tacRender.offline_render()
        print(type(depth))
        height_map, contact_mask, tactile_img = tacRender.taxim_render(depth, press_depth)
        cv2.imwrite(save_path+"/height_"+str(press_depth*1000)+"_"+obj_name+".jpg", height_map)
        cv2.imwrite(save_path+"/contact_mask_"+str(press_depth*1000)+"_"+obj_name+".jpg", 255*contact_mask.astype("uint8"))
        cv2.imwrite(save_path+"/tactile_"+str(press_depth*1000)+"_"+obj_name+".jpg", tactile_img)
