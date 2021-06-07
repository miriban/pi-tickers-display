from client.manager import Manager


if __name__ == '__main__':
    manager = Manager()
    manager.start()
    manager.watch(with_gui=False)