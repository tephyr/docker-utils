import sys

import docker

def show_current_containers():

    client = docker.from_env(version='auto')
    
    last_name = None
    
    for container in client.containers.list():
        #print(container)
        #print(container.attrs)
        name = container.attrs['Name']
        last_name = name
        imagePrimary = container.attrs['Image']
        imageAttr = container.attrs['Config']['Image']
        print(f"{container}: {name}, {imageAttr}, {imagePrimary}")

    if last_name is not None:
        container = client.containers.get(last_name)
        print(container.attrs.keys())

def manage_container(args):
    print(args)


def main(args):

    show_current_containers()
    manage_container(args)
    
if __name__ == '__main__':
    main(sys.argv[1:])
