import numpy as np
from . import winddes_creator as wdc

WindStrClassEnum = wdc.WindStrClassEnum
WindStrClass = wdc.WindStrClass

def calc_c_prob(p: float) -> float:
    K = 0.2
    n = 0.5
    return ((1-(K*np.log(-1*(np.log(1-p)))))/(1-(K*np.log(-1*(np.log(0.98))))))**n

def calc_c_r_z(type: WindStrClassEnum, z: float) -> float:
    z_0 = WindStrClass(type).get_z_vals()[0]
    z_min = WindStrClass(type).get_z_vals()[1]
    k_r = 0.19*(((z_0)/0.05)**0.07)
    if z >= z_min:
        return k_r*np.log(z/z_0)
    else:
        return k_r*np.log(z_min/z_0)


def calc_vm(
        type: WindStrClassEnum, 
        z: float,
        p: float = 0.02, 
        v_b: float = 20
        ) -> float:
    
    c_r_z = calc_c_r_z(type, z)
    c_o = 1.0
    return c_r_z*c_o*v_b*calc_c_prob(p)

def calc_qp_z(
        type: WindStrClassEnum, 
        z: float,
        p: float = 0.02, 
        v_b: float = 20
        ) -> float:
    
    z_0 = WindStrClass(type).get_z_vals()[0]
    z_min = WindStrClass(type).get_z_vals()[1]
    c_o = 1.0
    k_l = 1.0
    rho = 1.194
    if z >= z_min:
        I_v_z = k_l/(c_o*np.log(z/z_0))
        return (1+(7*I_v_z))*0.5*rho*((calc_vm(type,z,p,v_b))**2)/1000
    else:
        I_v_z = k_l/(c_o*np.log(z_min/z_0))
        return (1+(7*I_v_z))*0.5*rho*((calc_vm(type,z,p,v_b))**2)/1000

"""
Refer to EN1991-1-4 Chapter 7.4.1 Table 7.9.
"""

def calc_freewall_cpnet_solidity_1(l: float, h: float, corner: str) -> dict:
    """
    Corner input shall be either:\n
    Y: Yes, return corner is present;\n
    N: No, return corner is not present;\n
    \n
    When the corner length is less than h, "N" should be inputted.
    """
    walls_cpnet = [
    [2.3, 1.4, 1.2, 1.2],
    [2.9, 1.8, 1.4, 1.2],
    [3.4, 2.1, 1.7, 1.2],
    [2.1, 1.8, 1.4, 1.2],
    [1.2, 1.2, 1.2, 1.2]
    ]

    zone_no = {"A": 1, "B": 2, "C": 3, "D": 4}
    val_dict = {}

    l_h = l/h
    data = [l_h, corner]
    match data:
        case [l_h, "N"] if l_h <= 3:
            val_dict[zone_no["A"]] = walls_cpnet[0][0]
            val_dict[zone_no["B"]] = walls_cpnet[0][1]
            val_dict[zone_no["C"]] = walls_cpnet[0][2]
            val_dict[zone_no["D"]] = walls_cpnet[0][3]
        case [l_h, "N"] if l_h == 5:
            val_dict[zone_no["A"]] = walls_cpnet[1][0]
            val_dict[zone_no["B"]] = walls_cpnet[1][1]
            val_dict[zone_no["C"]] = walls_cpnet[1][2]
            val_dict[zone_no["D"]] = walls_cpnet[1][3]
        case [l_h, "N"] if l_h >= 10:
            val_dict[zone_no["A"]] = walls_cpnet[2][0]
            val_dict[zone_no["B"]] = walls_cpnet[2][1]
            val_dict[zone_no["C"]] = walls_cpnet[2][2]
            val_dict[zone_no["D"]] = walls_cpnet[2][3]
        case [l_h, "Y"]:
            val_dict[zone_no["A"]] = walls_cpnet[3][0]
            val_dict[zone_no["B"]] = walls_cpnet[3][1]
            val_dict[zone_no["C"]] = walls_cpnet[3][2]
            val_dict[zone_no["D"]] = walls_cpnet[3][3]
        case [l_h, "N"] if l_h > 3 and l_h < 5:
            val_dict[zone_no["A"]] = walls_cpnet[0][0]+ ((walls_cpnet[1][0] - walls_cpnet[0][0])*(l_h-3)/2)
            val_dict[zone_no["B"]] = walls_cpnet[0][1]+ ((walls_cpnet[1][1] - walls_cpnet[0][1])*(l_h-3)/2)
            val_dict[zone_no["C"]] = walls_cpnet[0][2]+ ((walls_cpnet[1][2] - walls_cpnet[0][2])*(l_h-3)/2)
            val_dict[zone_no["D"]] = walls_cpnet[0][3]
        case [l_h, "N"] if l_h > 5 and l_h < 10:
            val_dict[zone_no["A"]] = walls_cpnet[1][0]+ ((walls_cpnet[2][0] - walls_cpnet[1][0])*(l_h-5)/5)
            val_dict[zone_no["B"]] = walls_cpnet[1][1]+ ((walls_cpnet[2][1] - walls_cpnet[1][1])*(l_h-5)/5)
            val_dict[zone_no["C"]] = walls_cpnet[1][2]+ ((walls_cpnet[2][2] - walls_cpnet[1][2])*(l_h-5)/5)
            val_dict[zone_no["D"]] = walls_cpnet[0][3]
    
    return val_dict

def calc_freewall_cpnet_solidity_interpolate(l: float, h: float, corner: str, solidity: float) -> dict:
    """
    Corner input shall be either:\n
    Y: Yes, return corner is present;\n
    N: No, return corner is not present;\n
    \n
    When the corner length is less than h, "N" should be inputted.\n
    Solidity shall be more than equal to 0.8, max. is 1.0.
    """
    res_dict= {}
    cpnet_init = calc_freewall_cpnet_solidity_1(l,h,corner)
    for i in range(1,5):
        res_dict[i] = cpnet_init[i] - ((cpnet_init[i] - 1.2)*(1-solidity)/0.2)
    return res_dict

def calc_freewall_cpnet(l: float, h: float, corner: str, solidity: float) -> list:
    """
    Corner input shall be either:
    Y: Yes, return corner is present;
    N: No, return corner is not present;
    
    When the corner length is less than h, "N" should be inputted.
    
    Solidity shall be more than or equal to 0.8, and the max is 1.0.
    """
    if not (0.8 <= solidity <= 1.0):
        raise ValueError("Solidity must be between 0.8 and 1.0.")
    
    # Call to external function for interpolating cpnet values
    cpnet_res = calc_freewall_cpnet_solidity_interpolate(l, h, corner, solidity)
    
    res_zone_dict_1 = {}
    res_zone_dict_2 = {}

    # Logic for populating res_zone_dict_1 and res_zone_dict_2
    if l >= 4 * h:
        res_zone_dict_1[0] = cpnet_res[1]
        res_zone_dict_1[0.3 * h] = cpnet_res[1]
        res_zone_dict_1[2 * h] = cpnet_res[2]
        res_zone_dict_1[4 * h] = cpnet_res[3]
        res_zone_dict_1["remaining"] = cpnet_res[4]

        res_zone_dict_2[l] = cpnet_res[1]
        res_zone_dict_2[l - 0.3 * h] = cpnet_res[1]
        res_zone_dict_2[l - 2 * h] = cpnet_res[2]
        res_zone_dict_2[l - 4 * h] = cpnet_res[2]
        res_zone_dict_2["remaining"] = cpnet_res[4]
    elif l > 2*h:
        res_zone_dict_1[0] = cpnet_res[1]
        res_zone_dict_1[0.3 * h] = cpnet_res[1]
        res_zone_dict_1[2 * h] = cpnet_res[2]
        res_zone_dict_1["remaining"] = cpnet_res[3]

        res_zone_dict_2[l] = cpnet_res[1]
        res_zone_dict_2[l - 0.3 * h] = cpnet_res[1]
        res_zone_dict_2[l - 2 * h] = cpnet_res[2]
        res_zone_dict_2["remaining"] = cpnet_res[3]
    elif l <= 2 * h:
        res_zone_dict_1[0] = cpnet_res[1]
        res_zone_dict_1[0.3 * h] = cpnet_res[1]
        res_zone_dict_1["remaining"] = cpnet_res[2]

        res_zone_dict_2[l] = cpnet_res[1]
        res_zone_dict_2[l - 0.3 * h] = cpnet_res[1]
        res_zone_dict_2["remaining"] = cpnet_res[2]

    # Returning both dictionaries inside a list
    return [res_zone_dict_1, res_zone_dict_2]

def calc_rectbuild_cpe10(h: float, d: float) -> dict:
    walls_cpe10 = [
    [-1.2, -0.8, -0.5, 0.8, -0.7],
    [-1.2, -0.8, -0.5, 0.7, -0.3]
    ]

    zone_no = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    val_dict = {}

    h_d = h/d
    match h_d:
        case h_d if h_d > 0.25:
            val_dict[zone_no["A"]] = walls_cpe10[0][0]
            val_dict[zone_no["B"]] = walls_cpe10[0][2]
            val_dict[zone_no["C"]] = walls_cpe10[0][2]
            val_dict[zone_no["D"]] = walls_cpe10[0][3]
            val_dict[zone_no["E"]] = walls_cpe10[0][4]
        case h_d if h_d <= 0.25:
            val_dict[zone_no["A"]] = walls_cpe10[1][0]
            val_dict[zone_no["B"]] = walls_cpe10[1][2]
            val_dict[zone_no["C"]] = walls_cpe10[1][2]
            val_dict[zone_no["D"]] = walls_cpe10[1][3]
            val_dict[zone_no["E"]] = walls_cpe10[1][4]
    
    return val_dict

def calc_rectbuild_cpe1(h: float, d: float) -> dict:
    walls_cpe1 = [
    [-1.4, -1.1, -0.5, 1.0, -0.7],
    [-1.4, -1.1, -0.5, 1.0, -0.3]
    ]

    zone_no = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    val_dict = {}

    h_d = h/d
    match h_d:
        case h_d if h_d > 0.25:
            val_dict[zone_no["A"]] = walls_cpe1[0][0]
            val_dict[zone_no["B"]] = walls_cpe1[0][2]
            val_dict[zone_no["C"]] = walls_cpe1[0][2]
            val_dict[zone_no["D"]] = walls_cpe1[0][3]
            val_dict[zone_no["E"]] = walls_cpe1[0][4]
        case h_d if h_d <= 0.25:
            val_dict[zone_no["A"]] = walls_cpe1[1][0]
            val_dict[zone_no["B"]] = walls_cpe1[1][2]
            val_dict[zone_no["C"]] = walls_cpe1[1][2]
            val_dict[zone_no["D"]] = walls_cpe1[1][3]
            val_dict[zone_no["E"]] = walls_cpe1[1][4]
    
    return val_dict

def calc_rectbuild_cpe_interpolate(h: float, d: float, loaded_area: float) -> dict:
    res_dict={}
    if loaded_area <=1:
        cpe = calc_rectbuild_cpe1(h,d)
        for i in range(1,6):
            res_dict[i] = cpe[i]
    elif loaded_area <10:
        cpe_1 = calc_rectbuild_cpe1(h,d)
        cpe_10 = calc_rectbuild_cpe10(h,d)
        for i in range(1,6):
            res_dict[i] = cpe_10[i]+((10-loaded_area)/9*(cpe_1[i]-cpe_10[i]))
    elif loaded_area >=10:
        cpe = calc_rectbuild_cpe10(h,d)
        for i in range(1,6):
            res_dict[i] = cpe[i]
    return res_dict

def calc_rectbuild_cpe_angle_0_or_180(h: float, d: float, b: float, loaded_area: float) -> dict:
    zone_no = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    res_dict = calc_rectbuild_cpe_interpolate(h,d,loaded_area)
    res_side_dict = {}
    e = min(b, (2*d))

    res_side_dict[1] = res_dict[zone_no["D"]]
    if e >= 5*d:
        res_side_dict[2] = res_dict[zone_no["A"]]
    elif e <d:
        res_side_dict[2] = {
            0:res_dict[zone_no["A"]],
            0.2*e:res_dict[zone_no["A"]],
            d-e:res_dict[zone_no["C"]],
            d:res_dict[zone_no["A"]],
            d-0.2*e:res_dict[zone_no["A"]],
            e:res_dict[zone_no["C"]],
            "mid":res_dict[zone_no["B"]]
            }
    elif e >=d:
        res_side_dict[2] = {
            0:res_dict[zone_no["A"]],
            0.2*e:res_dict[zone_no["A"]],
            d:res_dict[zone_no["A"]],
            d-0.2*e:res_dict[zone_no["A"]],
            "mid":res_dict[zone_no["B"]]
            }

    res_side_dict[3] = res_dict[zone_no["E"]]
    res_side_dict[4] = res_side_dict[2]
    res_angle_dict={
        1:res_side_dict[1],
        2:res_side_dict[2],
        3:res_side_dict[3],
        4:res_side_dict[4]
        }
    return res_angle_dict

def calc_rectbuild_cpe_angle_90_or_270(h: float, d: float, b: float, loaded_area: float) -> dict:
    zone_no = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    res_dict = calc_rectbuild_cpe_interpolate(h,d,loaded_area)
    res_side_dict = {}
    e = min(b, (2*d))

    res_side_dict[2] = res_dict[zone_no["D"]]
    if e >= 5*d:
        res_side_dict[1] = res_dict[zone_no["A"]]
    elif e <d:
        res_side_dict[1] = {
            0:res_dict[zone_no["A"]],
            0.2*e:res_dict[zone_no["A"]],
            d-e:res_dict[zone_no["C"]],
            d:res_dict[zone_no["A"]],
            d-0.2*e:res_dict[zone_no["A"]],
            e:res_dict[zone_no["C"]],
            "mid":res_dict[zone_no["B"]]
            }
    elif e >=d:
        res_side_dict[1] = {
            0:res_dict[zone_no["A"]],
            0.2*e:res_dict[zone_no["A"]],
            d:res_dict[zone_no["A"]],
            d-0.2*e:res_dict[zone_no["A"]],
            "mid":res_dict[zone_no["B"]]
            }

    res_side_dict[4] = res_dict[zone_no["E"]]
    res_side_dict[3] = res_side_dict[1]
    res_angle_dict={
        1:res_side_dict[1],
        2:res_side_dict[2],
        3:res_side_dict[3],
        4:res_side_dict[4]
        }
    return res_angle_dict





    
    

    


        


