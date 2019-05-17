import json
import pprint
import sys
import traceback

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

def _show_container_info(container):
    """Show basic info about a container."""
    name = container.name
    last_name = name
    imagePrimary = container.attrs['Image']
    imageAttr = container.attrs['Config']['Image']
    print(f"{container.short_id}: {name}, {imageAttr}, {imagePrimary}")

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
        _show_container_info(container)

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
    app_state['config'] = config = json.loads(data.read())
    # pprint.pprint(config)

    if name not in config['systems']:
        raise KeyError(f'System not found: [{name}]')

    if not app_state['debug']:
        if app_state['verbosity'] > 0:
            print(f"Pull {config['systems'][name]['image']} using tag {config['systems'][name].get('tag', 'latest')}")
        pull_image_with_output(config['systems'][name]['image'], config['systems'][name].get('tag', 'latest'))
        stop_container(name)
        create_container(name)

@cli.command(name="pull")
@click.option('-i', '--image_name', required=True, help='Name of Docker image to pull')
@click.option('-t', '--tag', default='latest', show_default=True, help='Tag to pull')
def pull(image_name, tag):
    """Pull the latest image; default to latest tag"""
    # pull_image(image_name, tag)
    pull_image_with_output(image_name, tag)

def pull_image(image_name, tag):
    """Pull image using Docker API."""
    global app_state
    print(f'Will pull {image_name}:{tag}')
    image = app_state['client'].images.pull(image_name, tag=tag)
    print(f'Image: {image}')

def pull_image_with_output(image_name, tag):
    """Pull image using plumbum to show progress."""
    dckr = plumbum.local['docker']
    dckr['image', 'pull', f'{image_name}:{tag}'] & plumbum.FG

def stop_container(container_name):
    """Check if container is running, and stop it."""
    try:
        container = app_state['client'].containers.get(container_name)
        if container.status == 'running':
            result = container.wait()
            if app_state['verbosity'] > 0:
                pprint.pprint(result)
        elif container is not None:
            result = container.remove()
            if app_state['verbosity'] > 0:
                pprint.pprint(result)


    except docker.errors.NotFound:
        # OK
        if app_state['verbosity'] > 0:
            print(f'Container {container_name} not found; continuing.')
        pass

def create_container(container_name):
    try:
        config = app_state['config']['systems'][container_name]
        options = config.get('create', {})
        options['name'] = container_name

        print(f'Creating container named {container_name}')
        if app_state['verbosity'] > 0:
            print('\tContainer options')
            pprint.pprint(options)

        container = app_state['client'].containers.create(config['image'], **options)

        print('Container created')
        _show_container_info(container)

    except docker.errors.ImageNotFound:
        print("Image [{}] not found; aborting.")
    except:
        traceback.print_exc()


if __name__ == '__main__':
    cli()
