# Basic Driving Agent
When actions are chosen purely by random and the agent is given unlimited time to reach the destination, it does eventually reach it. However, this is purely a matter of chance.

# Indentifying and Updating State
**Relevant state variables:**
* Direction of next waypoint: `[None, 'forward', 'left', 'right']`
* Light status: `['red', 'green']`
* Oncoming traffic: `[None, 'forward', 'left', 'right']`
* Traffic to the left: `[None, 'forward', 'left', 'right']`

**Valid actions:** `[None, 'forward', 'left', 'right']`

In this simplistic model, the smartcab cares about two things: first, the location of the next waypoint; and second, its ability (right of way) to execute its valid actions.

Of the provided inputs, I've decided to ignore two:
* Deadline: Having the cab's behavior depend on the remaining time seems to me to be undesirable. Also, since there are so many possible values, including this variable would make the state space enormous.
* Traffic to the right: This has no affect on the cab's ability to execute its chosen action:
    - If traffic to the right is empty, there is obviously no impact.
    - If traffic to the right is proceeding straight or turning left, its light must be green and therefore the light for the cab must be red. That means the cab can only turn right, which traffic on the right can not impair.
    - If traffic to the right is turning right, the cab has the right of way to proceed straight. It clearly does not affect the cab's ability to turn left or right.

# Implementing Q-Learning
My Q-learning model is initialized uniformly with a value of 1 for all state/action pairs. The learning rate is `1/t` and the discount factor is 0.5. It has a 10% chance to return a random action other than the one with the highest Q-value.

The agent now consistently learns to reach the destination in time. For the first several trials it often fails to do so, but by trial 50 this trend has shifted. By trial 100 it almost always reaches the destination in time and rarely receives any penalties.

The agent was previously choosing random actions at each step. It is now using the reward received after taking an action to update the Q-value of that state/action pair. After enough trials, the Q-values should converge to reveal a reasonable policy. This is consistent with the behavior observed above.

# Optimizing the Agent
I was seeing some variance in the performance of the agent over several 100-trial runs, so I reduced the random action chance from 10% to 5%, which seemed to help with consistency.

Overall, I believe the agent performs very well. It consistently reaches the destination in time, for both short and long trips, and it usually receives either no or only one penalty during the trip.

Though I have seen several instances where the agent reaches the destination in the minimum possible time (assuming perfect luck with the lights), I believe its directness could be improved further.