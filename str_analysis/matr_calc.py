import numpy as np
class ElemLoadInp:

    def __init__(
            self,
            RV1: float,
            load_info: list,
            load_counter: int = 0
            ) -> None:
        
        self.RV1 = RV1
        self.load_info = load_info
        self.load_counter = load_counter

        return None
    
    def anlz_V_Pload(self, ind: int, x: float) -> list:

        self.load_counter += 1
        print(f"load_counter = {self.load_counter}")
    
        V_Pcalc = []

        if self.load_counter == 1:
            V_Pcalc.extend([self.RV1,self.RV1])
        else:
            self.RV1 = 0
            V_Pcalc.extend([self.RV1,self.RV1])


        if self.load_info[ind][2] < x:
            V_Pcalc[0] -= self.load_info[ind][1]

        if self.load_info[ind][2] <= x:
            V_Pcalc[1] -= self.load_info[ind][1]

        return V_Pcalc
    
    def anlz_V_wload(self, ind: int, x: float) -> list:

        self.load_counter += 1
        print(f"load_counter = {self.load_counter}")

        V_wcalc = []

        if self.load_counter == 1:
            V_wcalc.extend([self.RV1,self.RV1])
        else:
            self.RV1 = 0
            V_wcalc.extend([self.RV1,self.RV1])

        if self.load_info[ind][4] < x:
            V_wcalc[0] -= (self.load_info[ind][1] + self.load_info[ind][3])*(self.load_info[ind][4] - self.load_info[ind][2])/2

        if self.load_info[ind][2] < x:
            w_proj = (1 - (self.load_info[ind][4]-x)/(self.load_info[ind][4]-self.load_info[ind][2]))*self.load_info[ind][3]
            V_wcalc[0] -= (self.load_info[ind][1] + w_proj)*(self.load_info[ind][4] - self.load_info[ind][2])/2

        V_wcalc[1] = V_wcalc[0]

        return V_wcalc

    def anlz_total(self, x: float) -> list:

        V_res = [0,0]
        for i in range(len(self.load_info)):
            if self.load_info[i][0] == 'w':
                V_res = np.add(V_res, self.anlz_V_wload(i,x))
            if self.load_info[i][0] == 'P':
                V_res = np.add(V_res, self.anlz_V_Pload(i,x))

        self.load_counter=0
        print(f"load_counter = {self.load_counter}")

        return V_res