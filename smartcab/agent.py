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
        self.discount = 0.5
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
        # TODO: Add negative reward if failed to reach destination
        self.update_q_values(t, action, reward)
        self.net_reward += reward

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        if self.planner.next_waypoint() == None:
            print "Reached destination with net reward of {}".format(self.net_reward)

    def build_state_tuple(self, waypoint, inputs):
        forward_clear = self.is_forward_clear(inputs)
        right_clear = self.is_right_clear(inputs)
        left_clear = self.is_left_clear(inputs)
        return (waypoint, forward_clear, right_clear, left_clear)

    def is_forward_clear(self, inputs):
        if inputs['light'] == 'red':
            return False
        return True

    def is_right_clear(self, inputs):
        if inputs['light'] == 'green':
            return True
        if inputs['left'] == 'forward':
            return False
        if inputs['oncoming'] == 'left':
            return False
        return True

    def is_left_clear(self, inputs):
        if inputs['light'] == 'red':
            return False
        if inputs['oncoming'] == 'forward':
            return False
        if inputs['oncoming'] == 'right':
            return False
        return True

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
    sim = Simulator(e, update_delay=0.01)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
