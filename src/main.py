import dataloader

def main():

    setup()



    pass



def setup():
    base_stations = dataloader.load()
    links = create_links(base_stations)
    fail(base_stations)




    pass


def fail(base_stations):
    pass


def create_links(base_stations):
    pass


def simulate(base_stations,links):
    pass


if __name__ == '__main__':
    main()