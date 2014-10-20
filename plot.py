import matplotlib.pyplot as plt
import numpy as np

def corr(x,y):
    cm = np.cov(x,y)
    if cm[0][0] == 0 or cm[1][1] == 0:
        c = 0
    else:
        c = cm[0][1] / np.sqrt(cm[0][0] * cm[1][1])
    return c

# Exp1: 20 B, 16 B, 16 R, 10 B, 10 R
# Exp2: 20 B, 16 B, 16 R, 10 B, 10 R
# ...
max_no_knowledge = [[0.05556, 0.05556, 0, 0.05556, 0], #e1
                    [0.05556, 0.05556, 0.05556, 0.0277778, 0.0277778], #e2
                    [0.05556, 0.05556, 0, 0.05556, 0], #e3
                    [0.05556, 0.05556, 0.05556, 0.05556, 0.05556], #e4
                    [0.0104, 0, 0, 0, 0], #e5
                    [0.0104, 0.0104, 0, 0.0104, 0]] #e6

max_knowledge = [[0.05, 0.05, 0, 0.05, 0], #e1
                 [0.0416667, 0.0416667, 0.0416667, 0.0208333, 0.0208333], #e2
                 [0.03846, 0.03846, 0, 0.03846, 0], #e3
                 [0.05556, 0.05556, 0.05556, 0.05556, 0.05556], #e4
                 [0.00926, 0, 0, 0, 0], #e5
                 [0.00893, 0.00893, 0, 0.00893, 0]] #e6

match_no_knowledge = [[0.05556, 0.05556, 0, 0.05556, 0], #e1
                      [0.05556, 0.0444444, 0.0444444, 0.027778, 0.027778], #e2
                      [0.05556, 0.05556, 0, 0.05556, 0], #e3
                      [0.0416667, 0.0416667, 0.0416667, 0.0416667, 0.0416667], #e4
                      [0.0074, 0.00139, 0.00139, 0.00089, 0.00089], #e5
                      [0.00298, 0.00298, 0.00119, 0.00223, 0.00074]] #e6

match_knowledge = [[0.05, 0.05, 0, 0.05, 0], #e1
                   [0.0416667, 0.03333, 0.03333, 0.0208333, 0.0208333], #e2
                   [0.03846, 0.03846, 0, 0.03846, 0], #e3
                   [0.0416667, 0.0416667, 0.0416667, 0.0416667, 0.0416667], #e4
                   [0.00154, 0.00123, 0.00123, 0.000772, 0.000772], #e5
                   [0.00255, 0.002296, 0.001, 0.001913, 0.00064]]

avg = [[4.4, 4.933333333, 3.2, 4.8, 3.666666667], #e1
       [5.4, 4.733333333, 4.2, 4.6, 5], #e2
       [5.533333333, 5.4, 3.666666667, 5.266666667, 3.666666667], #e3
       [4.2, 4.2, 5.333333333, 4.266666667, 5.6], #e4
       [4.533333333, 4.266666667, 4.6, 4.533333333, 4.4], #e5
       [5.266666667, 5.4, 3.4, 4.933333333, 3.533333333]]


for i in range(len(avg)):
    fig, ax1 = plt.subplots()
    fig.set_size_inches(10,10)

    c1 = corr(max_no_knowledge[i], avg[i])
    c2 = corr(max_knowledge[i], avg[i])
    c3 = corr(match_no_knowledge[i], avg[i])
    c4 = corr(match_knowledge[i], avg[i])

    ax1.plot([1,2,3,4,5], max_no_knowledge[i], marker='D', linestyle='--', color='b', 
             label='max no knowledge, %.4f' % c1)
    ax1.plot([1,2,3,4,5], max_knowledge[i], marker='s', linestyle='--', color='r', 
             label='max knowledge, %.4f' % c2)
    ax1.plot([1,2,3,4,5], match_no_knowledge[i], marker='v', linestyle='--', color='c', 
             label='match no knowledge, %.4f' % c3)
    ax1.plot([1,2,3,4,5], match_knowledge[i], marker='*', linestyle='--', color='m', 
             label='match knowledge, %.4f' % c4)
    ax1.set_xlabel('Cases')
    ax1.set_ylabel('Model Prediction', color='b')
    for t in ax1.get_yticklabels():
        t.set_color('b')
    
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05), fancybox=True, shadow=True, ncol=4,
                             fontsize='small')


    ax2 = ax1.twinx()
    ax2.plot([1,2,3,4,5], avg[i], color='g', marker='o', linestyle='--')
    ax2.set_ylabel('Survey Average', color='g')
    for t in ax2.get_yticklabels():
        t.set_color('g')
        
    ax2.set_ylim(0,8)
    ax1.set_xlim(0,6)
    
    plt.title('Explanation '+str(i+1))
    
    fig.set_size_inches(14,10)
    plt.savefig('exp'+str(i+1)+'_plot.png', dpi=200)
            
max_no_knowledge = np.array(max_no_knowledge).transpose()
max_knowledge = np.array(max_knowledge).transpose()
match_no_knowledge = np.array(match_no_knowledge).transpose()
match_knowledge = np.array(match_knowledge).transpose()
avg = np.array(avg).transpose()

for i in range(len(avg)):
    fig, ax1 = plt.subplots()
    fig.set_size_inches(10,10)
    
    c1 = corr(max_no_knowledge[i], avg[i])
    c2 = corr(max_knowledge[i], avg[i])
    c3 = corr(match_no_knowledge[i], avg[i])
    c4 = corr(match_knowledge[i], avg[i])

    ax1.plot([1,2,3,4,5,6], max_no_knowledge[i], marker='D', linestyle='--', color='b', 
             label='max no knowledge, %.4f' % c1)
    ax1.plot([1,2,3,4,5,6], max_knowledge[i], marker='s', linestyle='--', color='r', 
             label='max knowledge, %.4f' % c2)
    ax1.plot([1,2,3,4,5,6], match_no_knowledge[i], marker='v', linestyle='--', color='c', 
             label='match no knowledge, %.4f' % c3)
    ax1.plot([1,2,3,4,5,6], match_knowledge[i], marker='*', linestyle='--', color='m', 
             label='match knowledge, %.4f' % c4)
    ax1.set_xlabel('Explanations')
    ax1.set_ylabel('Model Prediction', color='b')
    for t in ax1.get_yticklabels():
        t.set_color('b')
    
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05), fancybox=True, shadow=True, ncol=4,
                             fontsize='small')

    ax2 = ax1.twinx()
    ax2.plot([1,2,3,4,5,6], avg[i], color='g', marker='o', linestyle='--')
    ax2.set_ylabel('Survey Average', color='g')
    for t in ax2.get_yticklabels():
        t.set_color('g')
        
    ax2.set_ylim(0,8)
    ax1.set_xlim(0,7)
    
    plt.title('Case '+str(i+1))
    
    fig.set_size_inches(14,10)
    plt.savefig('case'+str(i+1)+'_plot.png', dpi=200)
            
