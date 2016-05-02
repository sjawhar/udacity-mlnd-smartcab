# Basic Driving Agent
When actions are chosen purely by random and the agent is given unlimited time to reach the destination, it does eventually reach it. However, this is purely a matter of chance.

# Indentifying and Updating State
**Relevant state variables:**
* Left/right bearing from current location to target: `[-1,0,1]`
    - If the target is to the right of the current location, taking into account the current heading, the value is 1.
    - If the target is to the left, the value is -1.
    - If the target is straight ahead, the value is 0.
* Backwards/forwards bearing from current location to target: `[-1,0,1]`
    - If the target is ahead of the current location, taking into account the current heading, the value is 1.
    - If the target is behind, the value is -1.
    - If the target is directly left or right, the value is 0.
* Traffic light color: `['red','green']`
* Oncoming traffic: `[None, 'forward', 'left', 'right']`
* Right traffic: `[None, 'forward', 'left', 'right']`
* Left traffic: `[None, 'forward', 'left', 'right']`

**Valid actions:** `[None, 'forward', 'left', 'right']`

# Using Docker Container
```bash
docker run -dt -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix -v $WORKDIR:/home/pygame/work \
    --name pygame pygame /bin/bash -c "cd work; python smartcab/agent.py"
```
