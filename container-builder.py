import json
import pprint
import sys

import click
import docker

client = None

def _prep_client():
    global client
    client = docker.from_env(version='auto')

def show_current_containers():

    global client
    
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

@click.command()
@click.option('-n', '--name', required=True, help='which docker container to use')
@click.argument('data', type=click.File('r'))
def manage_container(name, data):
    # print(data)
    config = json.loads(data.read())
    # print(f'Is recursive? {pprint.isrecursive(config)}; type? {type(config)}')
    # pprint.pprint(config)

    if name not in config['systems']:
        raise KeyError(f'System not found: [{name}]')

    pull_latest(config['systems'][name]['image'], config['systems'][name].get('tag', 'latest'))

# @click.command()
# @click.option('-i', '--image_name', required=True, help='Name of Docker image to pull')
def pull_latest(image_name, tag):
    global client
    print(f'Will pull {image_name}:{tag}')
    image = client.images.pull(image_name, tag=tag)
    print(f'Image: {image}')

def main(args):
    _prep_client()
    show_current_containers()
    manage_container(args)
    
if __name__ == '__main__':
    main(sys.argv[1:])
