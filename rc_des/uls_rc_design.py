import pandas as pd
from data_mod import mod_file as mod

gamma_s = 1.15

def calc_d_main(vars: list[float])-> float:
                
    h = vars[0]
    c = vars[1]
    link_bar_dia = vars[2]
    sec_bar_dia = vars[3]
    main_bar_dia = vars[4]

    return h-c-link_bar_dia-sec_bar_dia-(main_bar_dia/2)

def calcbatch_d(filename: str) -> list[float]:

    d_main_inputs = ['h','c','link_bar_dia','sec_bar_dia','main_bar_dia']

    df = pd.read_csv(filename)
    
    dict_list = []

    for i in range(len(df)): 
        data_dict = {key: float(df.loc[i, key]) for key in d_main_inputs}
        dict_list.append(data_dict)

    res_list = []
    for dict_data in dict_list:

        d = calc_d_main([dict_data[key] for key in d_main_inputs])
        res_list.append(d)

    return res_list

def update_d(df: pd.DataFrame, filename: str) -> None:

    d_res = calcbatch_d(filename)
    df['d'] = d_res
    df_new = mod.overwrite(df,filename)

    return df_new

def calc_K(vars: list[float]) -> float:
    
    M_Ed = vars[0]
    b = vars[1]
    d = vars[2]
    f_ck = vars[3]
    return (M_Ed*(10**6))/(b*(d**2)*f_ck)

def calcbatch_K(filename: str) -> list[float]:

    K_inputs = ['M_Ed','b','d','f_ck']

    df = pd.read_csv(filename)
    
    dict_list = []

    for i in range(len(df)):
        data_dict = {key: float(df.loc[i, key]) for key in K_inputs}
        dict_list.append(data_dict)

    res_list = []
    for dict_data in dict_list:
        K = calc_K([dict_data[key] for key in K_inputs])
        res_list.append(K)

    return res_list

def update_K(df: pd.DataFrame, filename: str) -> None:

    K_res = calcbatch_K(filename)
    df['K'] = K_res
    df_new = mod.overwrite(df,filename)

    return df_new

def check_comp_reinft(vars: list[float]) -> str:
    K = vars[0]
    if K<=0.167:
        return "Not required"
    else:
        return "Required"

def checkbatch_check_comp_reinft(filename: str) -> list[str]:

    inp = ['K']

    df = pd.read_csv(filename)
    
    dict_list = []

    for i in range(len(df)):
        data_dict = {key: float(df.loc[i, key]) for key in inp}
        dict_list.append(data_dict)

    res_list = []
    for dict_data in dict_list:
        check_res = check_comp_reinft([dict_data[key] for key in inp])
        res_list.append(check_res)

    return res_list

def update_check_comp_reinft(df: pd.DataFrame, filename: str) -> None:

    res = checkbatch_check_comp_reinft(filename)
    df['Comp. reinft. rqd?'] = res
    df_new = mod.overwrite(df,filename)

    return df_new

def calc_z(vars: list[float]) -> float:
        
    d = vars[0]
    K = vars[1]
    
    return d*(0.5+((0.25-(K/1.134))**0.5))

def calcbatch_z(filename:str) -> list[float]:

    z_inp = ['d', 'K']

    df = pd.read_csv(filename)
    
    dict_list = []

    for i in range(len(df)):
        data_dict = {key: float(df.loc[i, key]) for key in z_inp}
        dict_list.append(data_dict)

    res_list = []
    for dict_data in dict_list:
        z = calc_z([dict_data[key] for key in z_inp])
        res_list.append(z)

    return res_list

def update_z(df: pd.DataFrame, filename: str) -> None:

    z_res = calcbatch_z(filename)
    df['z'] = z_res
    df_new = mod.overwrite(df,filename)

    return df_new

def calc_As_req(vars: list[float],gamma_s: float) -> float:
        
    M_Ed = vars[0]
    f_yk = vars[1]
    z = vars[2]
    
    return M_Ed*(10**6)/(f_yk/gamma_s*z)

def calcbatch_As_req(filename:str) -> list[float]:

    As_req_inp = ['M_Ed', 'f_yk', 'z']

    df = pd.read_csv(filename)
    
    dict_list = []

    for i in range(len(df)):
        data_dict = {key: float(df.loc[i, key]) for key in As_req_inp}
        dict_list.append(data_dict)

    res_list = []
    for dict_data in dict_list:
        As_req = calc_As_req([dict_data[key] for key in As_req_inp],gamma_s)
        res_list.append(As_req)

    return res_list

def update_As_req(df: pd.DataFrame, filename: str) -> None:

    As_req_res = calcbatch_As_req(filename)
    df['As_req'] = As_req_res
    df_new = mod.overwrite(df,filename)

    return df_new
