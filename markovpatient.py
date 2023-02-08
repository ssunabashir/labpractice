import numpy as np
from markovinput import HealthStates
from deampy.markov import MarkovJumpProcess
from deampy.plots.sample_paths import PrevalencePathBatchUpdate


class Patient:
    def __init__(self, id, transition_prob_matrix):
        """

        :param id: ID of the patient
        :param transition_prob_matrix: transition probability matrix
        """
        self.id =id
        self.tranProbMatrix = transition_prob_matrix
        self.stateMonitor = PatientStateMonitor()

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length"""

        #random
        rng = np.random.RandomState(seed = self.id)

        #Markov jump process
        markov_jump = MarkovJumpProcess(
            transition_prob_matrix = self.tranProbMatrix
        )

        k =0 # simulate time steps

        while self.stateMonitor.get_if_alive() or k<n_time_steps:


            new_state_index = markov_jump.get_next_state(
                current_state_index= self.stateMonitor.currentState.value,
                rng =rng
            )

            self.stateMonitor.update(
                time_steps=k,
                new_state= HealthStates(new_state_index)
            )
class PatientStateMonitor:
    def __int__(self):
        self.currentState = HealthStates.CD4_200to500
        self.survivalTime = None
        self.timeToAIDS = None

    def update(self, time_step, new_state):
        #update survival time
        if new_state == HealthStates.HIV_DEATH:
            self.survivalTime = time_step + 0.5 #half cycle correction

        #update time until AIDS
        if self.currentState != HealthStates.AIDS \
                and new_state == HealthStates.AIDS:
            self.timeToAIDS = time_step + 0.5

        #update current health state
        self.currentState = new_state

    def get_if_alive(self):
        if self.currentState == HealthStates.HIV_DEATH:
            return
