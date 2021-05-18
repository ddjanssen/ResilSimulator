import dataloader

def main():

    setup()



    pass



def setup():
    base_stations = dataloader.load()
    links = create_links(base_stations)
    fail(base_stations)




    pass





def create_links(base_stations):
    link = base_stations[0] + base_stations[1]
    print(link)
    pass

def fail(base_stations):
    pass


def simulate(base_stations,links):
    pass


if __name__ == '__main__':
    main()