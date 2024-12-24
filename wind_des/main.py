from . import winddes_processor as wd

def main():
    # print(wd.calc_qp_z(wd.WindStrClassEnum.TYPE_1, 10))
    # print(wd.calc_qp_z(wd.WindStrClassEnum.TYPE_2, 10))
    # print(wd.calc_freewall_cpnet_solidity_1(10,2,"N"))
    # print(wd.calc_freewall_cpnet(10,2,"N",1))
    print(wd.calc_rectbuild_cpe_angle_0_or_180(10,5,2,10))

if __name__ == "__main__":
    main()