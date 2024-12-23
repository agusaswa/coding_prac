from . import winddes_processor as wd

def main():
    print(wd.calc_vm(wd.WindStrClassEnum.TYPE_1, 20))
    print(wd.calc_vm(wd.WindStrClassEnum.TYPE_2, 20,0.01))
    print(wd.calc_qp_z(wd.WindStrClassEnum.TYPE_1, 20))
    print(wd.calc_qp_z(wd.WindStrClassEnum.TYPE_2, 20))

if __name__ == "__main__":
    main()