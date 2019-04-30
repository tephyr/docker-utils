import docker

def main():

    client = docker.from_env(version='auto')
    
    for container in client.containers.list():
        #print(container)
        #print(container.attrs)
        name = container.attrs['Name']
        image = container.attrs['Config']['Image']
        print(f"{container}: {name!s} from {image!s}")

if __name__ == '__main__':
    main()
