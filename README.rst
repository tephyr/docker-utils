Docker Utilities
================
A suite of customized Docker utilities to simplify common multi-step tasks.

Requirements
++++++++++++
- Python 3.7+
- Install supporting modules: ``pip install -r requirements.txt``

Commands
++++++++
``show``
  Show current containers

``pull``
  Pull an image; defaults to latest

``manage``
  Refresh a container

Create/Update container
+++++++++++++++++++++++
Typical command::

    python container-builder.py -v manage -n DOCKER_CONTAINER_NAME --data FILENAME

Steps

#. Verify that 'name' parameter matches a "systems" key.
#. Pull latest image.

   - If no image, or no change, abort.

#. Check if container, by name, is running.

   - If so, shut it down.

#. Create container.
#. Return results.

   - Updated image info.
   - Name of created container.
