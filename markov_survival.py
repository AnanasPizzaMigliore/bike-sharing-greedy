import numpy as np
import calendar
import math
from scipy.special import iv

class Markov_Survival:

# Computes the survival time T for a given threshold probability and
# birth and death rates.
#
# p_th: threshold probability
# s: initial state of the BDP
# capacity: size of the MC
# departures: vector with death rates
# arrivals: vector with birth rates
# Tr: slot size (--> granularity with which the MDP is made discrete)
# Tp: frame size (mu and lambda are constant over a frame) !! Tr % Tp = 0
# hour: hour of the day (0-23)
# weekday: day of the week (0-6)
# day: day of the month (1-31)
# month: month of the year (1-12)
# year: last two digits of year

    def __init__(self,p_th,M,departures,arrivals,Tr,Tp,hour,weekday,day,month,year):
        self.p_th = p_th
        self.M = M
        self.departures = departures
        self.arrivals = arrivals
        self.Tr = Tr
        self.Tp = Tp
        self.hour = hour
        self.weekday = weekday
        self.day = day
        self.month = month
        self.year = year
        
    def T(self):
        n_max = self.Tr / self.Tp
        index = (self.month - 1) * 24 * 7 + self.weekday * 24 + self.hour
        T = np.zeros((self.M + 1))
        done = np.zeros((self.M + 1))
        done[0] = 1
        done[-1] = 1
        max_frames = n_max * 12
        Pt = []
        n = 1
        while (sum(done) < len(done) and n < max_frames):
            #print(f'the value of n {n} the index {index}\n')
            Pt = self.n_step_prob(n, self.M + 1, self.departures[index], self.arrivals[index], Pt)
            #print(f'matrix Pt {Pt}\n')
            for s in range(self.M + 1):
                if (done[s] == 0 and Pt[s,0] + Pt[s,-1] >= self.p_th):
                    # too large probability of having no bikes/docks available
                    T[s] = n
                    done[s] = 1
                    #print(f'matrix T {T} \n done {done} \n')

            # go on to new slot (new mu and lambda)
            if (np.mod(n, n_max) == 0):
                index = self.increase_index() # update index        
                #print(f'the index: {index} \n')
            
            n = n+1
            #print(f'value of n {n}\n')
        #print(f'done {done} and matrix {T}')
        for s in range(self.M + 1):
            if (done[s] == 0):
                T[s] = n


        T = T * self.Tp # real time: multiply for slots granularity
        
        return T
            
            
    def n_step_prob(self, n, M, mu, lam, P):
        if (n == 1):
            P = self.one_step_prob(M,mu,lam)
        else:
            P = np.matmul(self.one_step_prob(M,mu,lam), P)
        return P
            
     
    def one_step_prob(self, M, mu, lam):
        P = np.zeros((M, M))
        P[0,0] = 1
        P[-1,-1] = 1
        lam = max(0.01, lam * self.Tp / self.Tr)
        mu = max(0.01, mu * self.Tp / self.Tr)
        skellam = lambda k: math.exp(-lam-mu)*(lam/mu) ** (k/2)*iv(k,2 * math.sqrt(lam*mu))
        
        # Skellam distribution (Pjl = p(A-D = l-j), A~Poisson(lambda),D~Poisson(mu))
        for j in range(1, M-1):
            for l in range(1, M-1):
                P[j,l] = skellam(l-j)
        
            # support is infinite--> arrange P(j,1) and P(j,M)
            for l in range(-10*(j-1), -(j-1)):
                P[j,0] = P[j,0] + skellam(l)

            for l in range(M-j, 10*(M-j)):
                P[j,M-1] = P[j,M-1] + skellam(l)

            outage = 1 - sum(P[j,:]) # exceeding/missing to have sum(P(j,:))=1

            P[j,0] = P[j,0] + outage/2
            P[j,M-1] = P[j,M-1] + outage/2
            
        return P
            
    def increase_index(self):
        self.hour = self.hour + 1
        if self.hour >= 24: # change day
            self.hour = np.mod(self.hour, 24) # new hour
            self.day = self.day+1
            self.weekday = np.mod(self.weekday+1 ,7)
            last_day = calendar.monthrange(self.year+2000, self.month)[1]
            if self.day > last_day:
                self.day = np.mod(self.day,last_day)
                self.month = np.mod(self.month+1, 12)
                if self.month == 0:
                    self.month = 12
                elif self.month == 1:
                    self.year = self.year+1


        new_index = (self.month - 1) * 24 * 7 + self.weekday * 24 + self.hour
        #print(f'hour: {self.hour}, day: {self.day} weekday: {self.weekday}, month: {self.month}')
        
        return new_index
            
