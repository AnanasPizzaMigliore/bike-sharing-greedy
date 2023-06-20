
import markov_survival as MS
import numpy as np

def optimal_states(p_th: float, state, capacities, departures, arrivals, Tr, Tp, date, survival_mat, lastday):
#start_date = [hour(1-24) weekday(0-6) day(1-31) month(1-12) year]

    M = len(capacities)  # of stations
    optimal_state = np.copy(state)
    old_state = state.astype(int)
    survival = np.zeros((M))
    max_survival = {}

    for i in range(M):
    
    #fprintf('station %i (%i docks)\n', i, capacities(i));
        if (lastday and date[0] > 18):
            T = MS.Markov_Survival.T(p_th, capacities[i], departures[:,i], arrivals[:,i], Tr, Tp, 
                                     date[0], date[1], date[2], date[3], date[4])
        else:
            T = survival_mat[i][date[1], date[0], :]

        max_survival[i]= np.max(T)
        s1 = np.argmax(T)
        s2 = np.argmax(np.flip(T))
        optimal_state[i] = np.ceil(np.mean([s1, len(T) + 1 - s2]))
        survival[i] = T[old_state[i]]
        optimal_state[i] = optimal_state[i] - 1
    
    #pick the optimal state (the one that maximizes the survival time)
    #[~, s1] = max(T);
    
    return optimal_state, survival, max_survival