import math
import pandas as pd
from data_mod import mod_file as mod

def calc_reinf_area(d: float, n: int) -> float:

    return math.pi*(d**2)/4*n

def calc_Ec(f_ck: float, creep: float) -> float:

    return (22000*(((f_ck+8)/10)**0.3))/(1+creep)

def calc_neutral_axis(
        area_list: list[float],
        d_list: list[float], 
        b: float, 
        Es: float,
        f_ck: float,
        creep: float
    ) -> float:

    Ec = calc_Ec(f_ck, creep)
    alpha_e = Es/Ec

    tot_area = 0
    reinf_lev_arm = 0
    for i in range(len(area_list)):
        tot_area += area_list[i]
        reinf_lev_arm =  reinf_lev_arm + d_list[i]*area_list[i]
    
    d_ave = reinf_lev_arm/tot_area

    return ((-alpha_e*tot_area) + ((((alpha_e*tot_area)**2)+(2*b*alpha_e*tot_area*d_ave))**0.5))/b

def calculate_bar_stresses(M_inp,bar_diameters, effective_depths, b, Es, x_init,num_bars,creep):
    area_list=[]
    for i in range(len(bar_diameters)):
        area_list.append(calc_reinf_area(bar_diameters[i],num_bars[i]))
    tot_area = 0
    reinf_lev_arm = 0
    for i in range(len(area_list)):
        tot_area += area_list[i]
        reinf_lev_arm =  reinf_lev_arm + effective_depths[i]*area_list[i]
    
    d_ave = reinf_lev_arm/tot_area
    f_cc = M_inp*1000000*2/b/(d_ave-(x_init/3))/x_init
    print(f"f_c = {f_cc}")
    Ec = calc_Ec(f_cc, creep)
    epsilon_c_max = f_cc/Ec  # Max concrete strain at extreme fiber
    stresses = []
    for i in range(len(bar_diameters)):
        # Calculate concrete strain using triangular distribution
        epsilon_c = epsilon_c_max
        
        # Relate concrete strain to steel strain
        epsilon_steel = (effective_depths[i]-x_init)/x_init*epsilon_c
        # print(f"alpha_e = {Es / Ec}")
        print(f"Epsilon_s {i+1} = {epsilon_steel}")
        stress = Es * epsilon_steel 
        # if epsilon_steel < f_yk / 1.15 / Es else f_yk / 1.15  # Cap at yield stress
        stresses.append(stress)
    
    print(f"Epsilon_c = {epsilon_c}")
    
    return stresses

# Function to calculate the moment and verify equilibrium
def verify_equilibrium(M_inp,bar_diameters, num_bars, effective_depths, b, x, f_c,f_yk,Es, creep):
    C = 0.5 * f_c * b * x / 1000  # Concrete compressive force
    T = 0
    for i in range(len(bar_diameters)):
        stresses = calculate_bar_stresses(M_inp,bar_diameters,effective_depths,b,Es,x,num_bars, creep)
        area = calc_reinf_area(bar_diameters[i], num_bars[i])  # Total area of reinforcement
        T += area * stresses[i]/1000  # Tension force from steel
        print(f"T_{i+1} = {area * stresses[i]/1000} kN")
    
    M = 0
    for i in range(len(bar_diameters)):
        area = calc_reinf_area(bar_diameters[i], num_bars[i])  # Total area of reinforcement
        M += area * stresses[i] * (effective_depths[i] - x/3)/1000000  # Moment contribution from steel
        print(f"M_add_{i+1} = {area * stresses[i] * (effective_depths[i] - x/3)/1000000 } kNm")
    
    return C, T, M

# Function to iteratively adjust the neutral axis based on given moment
def adjust_neutral_axis_tension_only(bar_diameters, num_bars, effective_depths, b, f_ck, f_yk, Es, M_inp,creep, tol, inc, max_iter=10000):
    area_list=[]
    for i in range(len(bar_diameters)):
        area_list.append(calc_reinf_area(bar_diameters[i],num_bars[i]))
    tot_area = 0
    reinf_lev_arm = 0
    for i in range(len(area_list)):
        tot_area += area_list[i]
        reinf_lev_arm =  reinf_lev_arm + effective_depths[i]*area_list[i]
    
    d_ave = reinf_lev_arm/tot_area
    area_list=[]
    for i in range(len(bar_diameters)):
        area_list.append(calc_reinf_area(bar_diameters[i],num_bars[i]))
    print(f"Area = {area_list[i]} mm2")
    x_init = calc_neutral_axis(area_list,effective_depths,b,Es,f_ck, creep)  # Initial guess for neutral axis depth
    print(f"x = {x_init} mm")
    f_c = M_inp*1000000*2/b/(d_ave-(x_init/3))/x_init
    f_c_ori = f_c
    f_c_new = f_c
    while abs(f_c_ori - f_c_new) > 0.1:
        f_c_ori = f_c_new
        f_c_new = f_c_new + 0.1 
        x_init = calc_neutral_axis(area_list,effective_depths,b,Es,f_c_new, creep)  # Initial guess for neutral axis depth
        print(x_init)
        f_c_new = M_inp*1000000*2/b/(d_ave-(x_init/3))/x_init
        print(f_c_new)
    # print(f"fc = {f_c_new} MPa")


    iteration = 0
    last_x = x_init  # Store the last value of x to track convergence

    while iteration < max_iter and f_c <= f_ck:
        # Loop over concrete compressive strengths from 10 MPa to f_ck with increments of 1 MPa
        print("")
        print("Calculating neutral axis: ")
        print("")
        stresses = calculate_bar_stresses(M_inp,bar_diameters, effective_depths, b, Es, x_init,num_bars,creep)
        print(f"Iteration {iteration+1}: Stresses with f_c = {f_c} MPa: {stresses}")  # Debug print
        print(f"x = {x_init} mm")
        
        # Calculate equilibrium of forces and moments
        print("")
        print("Verifying forces: ")
        print("")
        C, T, M = verify_equilibrium(M_inp, bar_diameters, num_bars, effective_depths, b, x_init, f_c,f_yk,Es, creep)
        print(f"Iteration {iteration+1}: C = {C:.2f} kN, T = {T:.2f} kN, M = {M:.2f} kNm")  # Debug print
        
        # Check if the moment and force are close to the target values
        moment_balance = abs(M - M_inp)
        force_balance = abs(C - T)
        
        print(f"Iteration {iteration+1}: Moment balance = {moment_balance:.2f}, Force balance = {force_balance:.2f}")
        
        # Check for equilibrium
        if moment_balance < tol and force_balance < tol:
            print(f"Equilibrium achieved at x = {x_init:.2f} mm, f_c = {f_c} MPa")
            return x_init, M, stresses  # Return neutral axis and moment if equilibrium is achieved
        
        # Adjust the neutral axis based on the moment difference
        if M > M_inp:
            x_init += inc  # Finer adjustment
            print(f"x = {x_init}")
        else:
            x_init -= inc  # Finer adjustment
            print(f"x = {x_init}")
        
        # Prevent x from going beyond the maximum possible depth (d/2 or other limits)
        x_init = min(x_init, max(effective_depths))
        x_init = max(x_init, 0)  # Ensure x doesn't go below 0
        
        # Check if the neutral axis depth is oscillating or converging
        if abs(x_init - last_x) < 0.01:
            print(f"Converging: x is stable at {x_init:.2f} mm")
        
        last_x = x_init  # Update the last value of x
        
        iteration += 1
        
        # # Increment concrete strength f_c by 1 MPa
        # f_c = C*1000/(0.5*b*last_x)

    # After f_c reaches f_ck, if no equilibrium is achieved, return the last values
    if iteration >= max_iter:
        print(f"\nMax iterations reached, Moment balance = {moment_balance:.2f}, Force balance = {force_balance:.2f}")
        print(f"Last values: x = {x_init:.2f} mm, C = {C:.2f} kN, T = {T:.2f} kN, M = {M:.2f} kNm, f_c = {f_c:.2f} MPa")
        return x_init, M, stresses