# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 21:59:22 2021

@author: Dolan Clahan
"""
import random as rand
import numpy as np
import matplotlib.pyplot as plt

m1 = 10.0
sd1 = 5.0
m2 = 8.0
sd2 = 4.0
m3 = 5.0
sd3 = 2.5
#resturaunts, displayed in form (mean_score,standard_dev)
rests = [(m1,sd1),(m2,sd2),(m3,sd3)]

def e_greedy_plot(gm): 
    # evenly sampled time at 200ms intervals
    b = np.arange(0, 300, 1)     
    # red dashes, blue squares and green triangles
    plt.plot(b, np.array(gm[0]), 'r--', b, np.array(gm[1]), 'b--', b, np.array(gm[2]),'g--')
    plt.show()
    
def explore(itr):
    scores = []
    for i in range(itr):
        score = 0
        for j in range(300):
            choice = rand.randint(0,len(rests)-1)
            score+= rand.gauss(rests[choice][0], rests[choice][1])
        scores.append(score)
    av_score = sum(scores)/len(scores)
    print("average score:", av_score, "regret:", 3000-av_score)
    return scores
    
def exploit(itr):
    scores = []
    for i in range(itr):
        score = 0
        first_try = [0,0,0]
        for k in range(len(rests)): # try each one once
            exp = rand.gauss(rests[k][0], rests[k][1])
            first_try[k] = exp
            score += exp
        choice = first_try.index(max(first_try))
        for j in range(297): # only visit best one from 1st visit
            score += rand.gauss(rests[choice][0], rests[choice][1])
        scores.append(score)
    av_score = sum(scores)/len(scores)
    print("average score:", av_score, "regret:", 3000-av_score)
    return scores

def ep_greedy(epsilon, plot_it = False):
    plt_av = [[0 for i in range(300)] for i in range(len(rests))]
    plt_spot = 0
    memory = [[] for i in range(len(rests))]
    for i in range(len(rests)):
        exp = rand.gauss(rests[i][0], rests[i][1])
        memory[i].append(exp)
        plt_av[i][plt_spot] = exp
        plt_spot+=1
    for i in range(297):
        #exploit
        av_scores = [sum(b)/len(b) for b in memory]
        choice = av_scores.index(max(av_scores))
        #explore
        if rand.random() <= epsilon:
            choice = rand.randint(0,2)
        memory[choice].append(rand.gauss(rests[choice][0], rests[choice][1]))
        for j in range(len(rests)):
            plt_av[j][plt_spot] = av_scores[j]
        plt_spot+=1
    av_scores = [sum(b)/len(b) for b in memory]
    #print total score/regret
    score = sum([sum(b) for b in memory])
    if plot_it:
        print("Score:",score,"Regret:", 3000-score)
        e_greedy_plot(plt_av)
    return score

if __name__=="__main__":
    print("EXPLORE ONLY")
    re = explore(1000)
    print("EXPLOIT ONLY")
    it = exploit(1000)
    print("EPSILON-GREEDY ALGORITHM -- 10%")
    scores_10 = []
    for i in range(1000):
        scores_10.append(ep_greedy(0.1))
    av_score = sum(scores_10)/len(scores_10)
    print("average score:", av_score, "regret:", 3000-av_score)
#    print("EXAMPLE E-GREEDY -- 10%")
#    ep_greedy(0.1, True)
    print("EPSILON-GREEDY ALGORITHM -- 5%")
    scores_5 = []
    for i in range(1000):
        scores_5.append(ep_greedy(0.05))
    av_score = sum(scores_5)/len(scores_5)
    print("average score:", av_score, "regret:", 3000-av_score)
#    print("EXAMPLE E-GREEDY -- 5%")
#    ep_greedy(0.05, True)
    print("EPSILON-GREEDY ALGORITHM -- 1%")
    scores_1 = []
    for i in range(1000):
        scores_1.append(ep_greedy(0.01))
    av_score = sum(scores_1)/len(scores_1)
    print("average score:", av_score, "regret:", 3000-av_score)
#    print("EXAMPLE E-GREEDY -- 1%")
#    ep_greedy(0.01, True)
    
    # TODO: plot all (average?) scores for all simulations