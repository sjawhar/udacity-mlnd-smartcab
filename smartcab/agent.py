import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

from collections import defaultdict
from operator import itemgetter

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.randomness = 0.1
        self.discount = 1
        self.net_reward = 0

        def get_default_q_values():
            default_q_values = {}
            for action in self.env.valid_actions:
                default_q_values[action] = 1
            return default_q_values
        self.q_values = defaultdict(get_default_q_values)

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.net_reward = 0

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = self.build_state_tuple(self.next_waypoint, inputs)
        
        # TODO: Select action according to your policy
        action = self.get_next_action()

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.update_q_values(t, action, reward)
        self.net_reward += reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

    def build_state_tuple(self, waypoint, inputs):
        return (waypoint, inputs['light'], inputs['oncoming'], inputs['right'], inputs['left'])

    def get_next_action(self):
        best_action = self.get_best_action(self.state)[0]

        if random.random() < self.randomness:
            random_actions = [action for action in self.env.valid_actions if action != best_action]
            return random.choice(random_actions)

        return best_action

    def get_best_action(self, state):
        actions = self.q_values[state]
        return max(actions.iteritems(), key=itemgetter(1))

    def update_q_values(self, t, action, reward):
        learning_rate = 1.0/(t + 1)
        
        new_waypoint = self.planner.next_waypoint()
        new_inputs = self.env.sense(self)
        new_state = self.build_state_tuple(new_waypoint, new_inputs)
        new_best_action = self.get_best_action(new_state)
        new_q_value = reward + self.discount * new_best_action[1]

        current_q_value = self.q_values[self.state][action]        
        self.q_values[self.state][action] = (1 - learning_rate) * current_q_value + learning_rate * new_q_value

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
