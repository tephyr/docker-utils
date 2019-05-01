Docker Utilities
================
Requirements
++++++++++++
- Python 3.7+

Create/Update container
+++++++++++++++++++++++
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
