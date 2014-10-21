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
                   [0.00255, 0.002296, 0.001, 0.001913, 0.00064]] #e6

avg = [[4.4, 4.933333333, 3.2, 4.8, 3.666666667], #e1
       [5.4, 4.733333333, 4.2, 4.6, 5], #e2
       [5.533333333, 5.4, 3.666666667, 5.266666667, 3.666666667], #e3
       [4.2, 4.2, 5.333333333, 4.266666667, 5.6], #e4
       [4.533333333, 4.266666667, 4.6, 4.533333333, 4.4], #e5
       [5.266666667, 5.4, 3.4, 4.933333333, 3.533333333]] #e6


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
    plt.savefig('exp'+str(i+1)+'_plot.png', dpi=200, bbox_inches='tight')
            
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
    plt.savefig('case'+str(i+1)+'_plot.png', dpi=200, bbox_inches='tight')
            


for x in [0,1]:
    fig, axes = plt.subplots(4,5)
    axes = np.asarray(axes).transpose()
    
    axes[0][0].set_title('Case 1')
    axes[1][0].set_title('Case 2')
    axes[2][0].set_title('Case 3')
    axes[3][0].set_title('Case 4')
    axes[4][0].set_title('Case 5')

    for i in range(len(avg)):
        ax_i = axes[i]
        c1 = corr(max_no_knowledge[i], avg[i])
        c2 = corr(max_knowledge[i], avg[i])
        c3 = corr(match_no_knowledge[i], avg[i])
        c4 = corr(match_knowledge[i], avg[i])
        
        ax_i[0].plot([1,2,3,4,5,6], max_no_knowledge[i], marker='D', linestyle='--', color='b', 
                     label='max no knowledge, %.4f' % (c1 if x == 1 else 0))
        ax_i[1].plot([1,2,3,4,5,6], max_knowledge[i], marker='s', linestyle='--', color='r', 
                     label='max knowledge, %.4f' % (c2 if x == 1 else 0))
        ax_i[2].plot([1,2,3,4,5,6], match_no_knowledge[i], marker='v', linestyle='--', color='c', 
                     label='match no knowledge, %.4f' % (c3 if x == 1 else 0))
        ax_i[3].plot([1,2,3,4,5,6], match_knowledge[i], marker='*', linestyle='--', color='m', 
                     label='match knowledge, %.4f' % (c4 if x == 1 else 0))
        map(lambda ax: ax.set_xlabel('Explanations'), ax_i)
        map(lambda ax: ax.set_ylabel('Model Prediction', color='b'), ax_i) if i == 0 else ''

        def setLabels(ax1):
            for t in ax1.get_yticklabels():
                t.set_color('b')
        map(setLabels, ax_i)

        map(lambda ax1: ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05), fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small'), ax_i)

        def plotAvg(ax):
            ax2 = ax.twinx()
            ax2.plot([1,2,3,4,5,6], avg[i], color='g', marker='o', linestyle='--')
            ax2.set_ylabel('Survey Average', color='g') if i == len(avg)-1 else ''
            for t in ax2.get_yticklabels():
                t.set_color('g')
        
            ax2.set_ylim(0,8)
            ax.set_xlim(0,7)
        map(plotAvg, ax_i) if x == 1 else ''

    
    
        fig.set_size_inches(26,26)


    fig.suptitle('Model Predictions And Data' if x == 1 else 'Model Predictions', 
                 fontsize=34, fontweight='bold')
    plt.savefig('total_plot.png' if x==1 else 'prediction_plot.png', dpi=200, bbox_inches='tight')


fig, axes = plt.subplots(1,5)
    
axes[0].set_title('Case 1')
axes[1].set_title('Case 2')
axes[2].set_title('Case 3')
axes[3].set_title('Case 4')
axes[4].set_title('Case 5')

for i in range(5):
    axes[i].plot([1,2,3,4,5,6], avg[i], color='g', marker='o', linestyle='--')
    axes[i].set_ylabel('Survey Average', color='g') if i == 0 else ''
    for t in axes[i].get_yticklabels():
        t.set_color('g')
    axes[i].set_ylim(0,8)
    axes[i].set_xlim(0,7)

fig.set_size_inches(26,5.5)

fig.suptitle('Human Data', fontsize=18, fontweight='bold')
plt.savefig('human_data.png', dpi=200, bbox_inches='tight')


fig, axes = plt.subplots(2,2)
axes[0][0].set_title('Max No Knowledge')
axes[0][1].set_title('Max Knowledge')
axes[1][0].set_title('Match No Knowledge')
axes[1][1].set_title('Match Knowledge')

fig.suptitle('Model Predictions vs. Human Data', fontsize=20, fontweight='bold')

favg = avg.flatten()

axes[0][0].set_title('Max No Knowledge')
cor = corr(max_no_knowledge.flatten(), favg)
axes[0][0].plot(max_no_knowledge.flatten(), favg, color='b', marker = 'o', linestyle='',
                label='Corr = %0.4f' % cor)
axes[0][0].set_ylabel('Human Data')
axes[0][0].set_xlabel('Model Predictions')
axes[0][0].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


axes[0][1].set_title('Max Knowledge')
cor = corr(max_knowledge.flatten(), favg)
axes[0][1].plot(max_knowledge.flatten(), favg, color='b', marker = 'o', linestyle='',
                label='Corr = %0.4f' % cor)
axes[0][1].set_ylabel('Human Data')
axes[0][1].set_xlabel('Model Predictions')
axes[0][1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


axes[1][0].set_title('Match No Knowledge')
cor = corr(match_no_knowledge.flatten(), favg)
axes[1][0].plot(match_no_knowledge.flatten(), favg, color='b', marker = 'o', linestyle='',
                label='Corr = %0.4f' % cor)
axes[1][0].set_ylabel('Human Data')
axes[1][0].set_xlabel('Model Predictions')
axes[1][0].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


axes[1][1].set_title('Match Knowledge')
cor = corr(match_knowledge.flatten(), favg)
axes[1][1].plot(match_knowledge.flatten(), favg, color='b', marker = 'o', linestyle='',
                label='Corr = %0.4f' % cor)
axes[1][1].set_ylabel('Human Data')
axes[1][1].set_xlabel('Model Predictions')
axes[1][1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


fig.set_size_inches(15,15)
plt.savefig('scatter_plot.png', dpi=200, bbox_inches='tight')
