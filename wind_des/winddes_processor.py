import numpy as np
import winddes_creator as wdc

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