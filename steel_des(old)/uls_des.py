def calc_Vcap(fy: float, shear_area: float) -> float:
    return ((3**0.5)*fy*shear_area/1000)

def calc_Mcap(fy: float, mod: float, v_ed: float, v_cap:float) -> float:
    if v_ed/v_cap > 0.5:
        return (1-((2*v_ed/v_cap-1)**2))*fy*mod/(10**6)
    else:
        return fy*mod/(10**6)