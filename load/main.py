import load_processor as lp

def main():
    sw = lp.SelfWeight(25,200)
    dl = lp.DeadLoad(25,250)
    ll = lp.LiveLoad(5)
    sdl_data1 = lp.SDL_Data(category_name="SDL Blanket",predef_magnitude=10)
    sdl_data2 = lp.SDL_Data("Screed",25,150)
    sdl = lp.SDL([sdl_data1,sdl_data2])
    load = lp.Load(self_weight=sw,live_load=ll,sdl=sdl, dead_load=dl)
    print(load.total_load())
    print(load.dead_load)

if __name__ == "__main__":
    main()
