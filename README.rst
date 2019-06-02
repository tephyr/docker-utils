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

Data format
+++++++++++
- ``CONTAINER_NAME`` is the chosen name for the built container.
- ``IMAGE_SOURCE`` is the canonical Docker image name.
- ``tag`` element is optional.
- Fill the optional ``environment``, ``ports``, and ``volumes`` values using the docker-py_ syntax for those elements:

::

    {
        "systems": {
            "CONTAINER_NAME": {
                "image": "IMAGE_SOURCE",
                "tag": "<OPTIONAL>",
                "create": {
                    "environment": [],
                    "ports": {},
                    "volumes": {}
                }
            }
        }
    }

Examples::

    {
        "systems": {
            "couchdb": {
                "image": "apache/couchdb"
            },
            "nextcloud": {
                "image": "nextcloud",
                "tag": "15",
                "create": {
                    "environment": [
                        "NEXTCLOUD_TRUSTED_DOMAINS='example:7070 localhost'"
                    ],
                    "ports": {
                        "80/tcp": 7070
                    },
                    "volumes": {
                        "/opt/storage/nextcloud-data": {
                            "bind": "/var/www/html", "mode": "rw"
                        }
                    }
                }
            }
        }
    }

.. _docker-py: https://github.com/docker/docker-py
