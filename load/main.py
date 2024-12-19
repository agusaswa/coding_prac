import load_calculator as lc

def main():
    sw = lc.SelfWeight(25,200)
    dl = lc.DeadLoad(25,250)
    ll = lc.LiveLoad(5)
    sdl_data1 = lc.SDL_Data(category_name="SDL Blanket",predef_magnitude=10)
    sdl_data2 = lc.SDL_Data("Screed",25,150)
    sdl = lc.SDL([sdl_data1,sdl_data2])
    load_rec1 = lc.LoadRecord(sw,dl,ll,sdl)
    lt = lc.LoadType
    print(lc.calculate_load(load_rec1,[lt.DEAD_LOAD,lt.SDL]))
    print(lc.calculate_load(load_rec1))

if __name__ == "__main__":
    main()
