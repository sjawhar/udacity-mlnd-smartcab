# Basic Driving Agent
When actions are chosen purely by random and the agent is given unlimited time to reach the destination, it does eventually reach it. However, this is purely a matter of chance.

# Indentifying and Updating State
**Relevant state variables:**
* Direction of next waypoint: `[None, 'forward', 'left', 'right']`
* Does the agent have the right of way to proceed forward? `[True, False]`
* Does the agent have the right of way to turn right? `[True, False]`
* Does the agent have the right of way to turn left? `[True, False]`

**Valid actions:** `[None, 'forward', 'left', 'right']`

# Using Docker Container
```bash
docker run -dt -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix -v $WORKDIR:/home/pygame/work \
    --name pygame pygame /bin/bash -c "cd work; python smartcab/agent.py"
```
