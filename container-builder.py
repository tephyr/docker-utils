import json
import pprint
import sys

import click
import docker
import plumbum

app_state = {
    'client': None,
    'verbosity': 0,
    'debug': False
}

def _prep_client():
    global app_state
    app_state['client'] = docker.from_env(version='auto')

@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('--debug', is_flag=True)
def cli(verbose, debug):
    global app_state
    app_state['verbosity'] = verbose
    app_state['debug'] = debug

    if (verbose > 0):
        debug_state = 'on' if debug else 'off'
        click.echo(f'Debug mode is {debug_state}, verbosity=={verbose}')

    _prep_client()

@cli.command(name="show")
def show_current_containers():
    """Show the current containers"""
    global app_state

    last_name = None
    container_count = 0;

    for container in app_state['client'].containers.list():
        container_count += 1
        #print(container)
        #print(container.attrs)
        name = container.attrs['Name']
        last_name = name
        imagePrimary = container.attrs['Image']
        imageAttr = container.attrs['Config']['Image']
        print(f"{container}: {name}, {imageAttr}, {imagePrimary}")

    if last_name is not None:
        container = app_state['client'].containers.get(last_name)
        print(container.attrs.keys())

    print(f'Current number of containers: {container_count}')

@cli.command(name="manage")
@click.option('-n', '--name', required=True, help='which docker container to use')
@click.option('--data', type=click.File('r'))
def manage_container(name, data):
    """Refresh a container start-to-finish: pull latest image, shut down if running, create container"""
    global app_state
    config = json.loads(data.read())
    # pprint.pprint(config)

    if name not in config['systems']:
        raise KeyError(f'System not found: [{name}]')

    if not app_state['debug']:
        if app_state['verbosity'] > 0:
            print(f"Pull {config['systems'][name]['image']} using tag {config['systems'][name].get('tag', 'latest')}")
        pull_image_with_output(config['systems'][name]['image'], config['systems'][name].get('tag', 'latest'))

@cli.command(name="pull")
@click.option('-i', '--image_name', required=True, help='Name of Docker image to pull')
@click.option('-t', '--tag', default='latest', show_default=True, help='Tag to pull')
def pull(image_name, tag):
    """Pull the latest image; default to latest tag"""
    # pull_image(image_name, tag)
    pull_image_with_output(image_name, tag)

def pull_image(image_name, tag):
    global app_state
    print(f'Will pull {image_name}:{tag}')
    image = app_state['client'].images.pull(image_name, tag=tag)
    print(f'Image: {image}')

def pull_image_with_output(image_name, tag):
    """Pull image using plumbum to show progress."""
    dckr = plumbum.local['docker']
    dckr['image', 'pull', f'{image_name}:{tag}'] & plumbum.FG

if __name__ == '__main__':
    cli()
