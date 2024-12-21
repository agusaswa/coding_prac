import uls_des

def main():
    print(uls_des.calc_Vcap(500, 100))
    print(uls_des.calc_Mcap(500,10000,100,uls_des.calc_Vcap(500,100)))

if __name__ == "__main__":
    main()