import matplotlib.pyplot as plt
import numpy as np
import json

def corr(x,y):
    cm = np.cov(x,y)
    if cm[0][0] == 0 or cm[1][1] == 0:
        c = 0
    else:
        c = cm[0][1] / np.sqrt(cm[0][0] * cm[1][1])
    return c


def exp2():
    exp2_data = np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["6","5","5","4","6","7","4","7","5","4","1","7","4","6","7","5","4"],["5","3","6","5","6","4","2","5","5","4","7","5","5","5","1","6","4"],["6","4","5","1","2","7","4","7","1","4","7","4","6","3","7","5","4"],["2","5","5","3","3","2","4","1","1","4","5","5","2","7","1","4","4"],["2","5","5","2","7","5","3","7","5","4","1","4","3","7","1","2","5"],["2","6","4","2","2","5","4","7","1","4","3","4","7","7","7","2","2"]]')))

    exp3_data = np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["3","2","4","5","6","4","4","2","1","2","6","6","1","6","2"],["4","2","4","4","5","4","4","5","6","5","3","4","2","6","1"],["5","2","2","4","6","3","5","5","1","2","3","7","1","6","1"],["3","7","7","7","1","6","3","4","6","6","4","1","7","6","7"],["4","2","1","4","2","3","2","6","6","2","2","2","1","7","1"],["5","2","2","3","7","3","2","1","1","2","2","5","1","7","1"]]')))

    complexity_no_knowledge = 1.0 / np.asarray([18, 18, 18, 18, 28, 48])
    complexity_knowledge =    1.0 / np.asarray([20, 24, 26, 18, 54, 56])
    complexity = [complexity_no_knowledge, complexity_knowledge]

    avg = [[4.4, 4.933333333, 3.2, 4.8, 3.666666667], #e1
           [5.4, 4.733333333, 4.2, 4.6, 5], #e2
           [5.533333333, 5.4, 3.666666667, 5.266666667, 3.666666667], #e3
           [4.2, 4.2, 5.333333333, 4.266666667, 5.6], #e4
           [4.533333333, 4.266666667, 4.6, 4.533333333, 4.4], #e5
           [5.266666667, 5.4, 3.4, 4.933333333, 3.533333333]] #e6
    avg = np.asarray(avg).transpose()

    sumTotal = exp3_data.sum(axis=1)
    mean = exp3_data.mean(axis=1)
    std = exp3_data.std(axis=1)

    fig, axes = plt.subplots(1,2)
    
    for i in [0,1]:
        #axe[i]s.errorbar([1,2,3,4,5,6], mean, yerr=std)
        axes[i].plot([1,2,3,4,5,6], complexity[i], color='r', marker='v', linestyle='--')
        axes[i].set_ylabel('Model Prediction', color='r') if i == 0 else ''
        for t in axes[i].get_yticklabels():
            t.set_color('r')
        axes[i].set_xlim(0,8)

        ax2 = axes[i].twinx()
        ax2.plot([1,2,3,4,5,6], mean, color='g', marker='o', linestyle='--')
        ax2.set_ylabel('Survey Average', color='g') if i == 1 else ''
        for t in ax2.get_yticklabels():
            t.set_color('g')
        
        axes[i].set_title('No Knowledge Edges' if i == 0 else 'Knowledge Edges')
        ax2.set_ylim(0,8)
        ax2.set_xlim(0,7)

    fig.set_size_inches(25,10)
        
    fig.suptitle('Human Ratings of Best Explanation', fontsize=18, fontweight='bold')
    plt.savefig('plot_human_data_exp3.png', dpi=200, bbox_inches='tight')

    # scatter plot
    fig, axes = plt.subplots(1,2)
    fig.suptitle('Model Predictions vs. Human Data', fontsize=20, fontweight='bold')
    

    cor = corr(complexity[0], mean)
    axes[0].plot(mean, complexity[0], color='r', marker='o', linestyle='', 
                 label='Corr = %0.4f' % cor)
    axes[0].set_ylabel('Model Predictions', color='g')        
    axes[0].set_title('No Knowledge Edges')
    axes[0].set_xlabel('Survey Data')
    axes[0].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


    cor = corr(complexity[1], mean)
    axes[1].plot(mean, complexity[1], color='r', marker='o', linestyle='', 
                 label='Corr = %0.4f' % cor)
    axes[1].set_ylabel('Model Predictions', color='g')        
    axes[1].set_title('Knowledge Edges')
    axes[1].set_xlabel('Survey Data')
    axes[1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')

    fig.set_size_inches(25,10)
    plt.savefig('plot_scatter_exp3.png', dpi=200, bbox_inches='tight')


    fig, axes = plt.subplots(2,2)
    
    axes[0][0].plot([1,2,3,4,5,6], mean, color='r', marker='o', linestyle='--')
    axes[0][0].set_ylabel('Survey Data', color='r')
    axes[0][0].set_xlim(0,7)
    axes[0][0].set_ylim(0,8)
    axes[0][0].set_title('Exp 3 Data')
    
    axes[0][1].plot([1,2,3,4,5,6], avg[3], color='r', marker='o', linestyle='--')
    axes[0][1].set_ylabel('Survey Data', color='r')
    axes[0][1].set_xlim(0,7)
    axes[0][1].set_ylim(0,8)
    axes[0][1].set_title('Exp 1 Data, Case 4')

    axes[1][0].plot([1,2,3,4,5,6], mean, color='r', marker='o', linestyle='--')
    axes[1][0].set_ylabel('Exp 2 Data', color='r')
    axes[1][0].set_xlim(0,7)
    axes[1][0].set_ylim(0,8)
    axes[1][0].set_title('Exp 1 and Exp 3')
        
    ax2 = axes[1][0].twinx()
    ax2.plot([1,2,3,4,5,6], avg[3], color='g', marker='v', linestyle='--')
    ax2.set_ylabel('Exp 1 Data', color='g') if i == 1 else ''
    for t in ax2.get_yticklabels():
        t.set_color('g')        
    axes[1][0].set_title('Exp 1 and Exp 3')
    ax2.set_ylim(0,8)
    ax2.set_xlim(0,7)


    cor = corr(mean, avg[3])
    axes[1][1].plot(avg[3], mean, color='r', marker='o', linestyle='', label='Corr = %0.4f' % cor)
    axes[1][1].set_ylabel('Exp 3 Data', color='r')
    axes[1][1].set_xlabel('Exp 1 Data')
    axes[1][1].set_xlim(0,7)
    axes[1][1].set_ylim(0,8)
    axes[1][1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')
    axes[1][1].set_title('Exp 1 and Exp 3')

    fig.set_size_inches(20,20)
        
    fig.suptitle('Experiment 1 (case 4) and 3 Comparison', fontsize=18, fontweight='bold')
    plt.savefig('plot_exp1_exp3_compare.png', dpi=200, bbox_inches='tight')


def exp1():
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

    exp5_data = np.asarray(map (lambda z: map(lambda x: map(lambda y: int(y), x), z), json.loads('[[["5","1","1","4","5","6","6","4","6","5","4","1"],["5","2","5","4","3","6","7","6","3","6","4","4"],["5","3","2","2","5","6","6","4","5","6","4","1"],["5","5","6","6","5","6","5","5","6","6","5","5"],["4","3","1","6","4","6","5","6","3","6","3","1"]],[["6","7","6","6","4","2","6","6","3","6","4","1"],["4","6","5","6","4","6","5","6","5","7","4","4"],["4","6","6","6","6","3","6","5","4","7","3","1"],["4","5","5","4","4","2","6","5","4","7","4","4"],["5","3","4","4","4","2","6","4","6","7","4","1"]],[["6","1","1","6","4","2","4","4","4","4","4","1"],["6","6","5","4","4","5","6","5","4","5","4","4"],["4","3","1","2","5","5","5","5","5","5","3","1"],["6","5","6","6","6","2","6","6","4","6","2","5"],["6","3","2","4","5","6","4","5","6","6","4","1"]],[["5","7","6","6","3","7","3","5","6","4","4","7"],["5","5","5","6","5","6","6","5","3","6","4","7"],["5","6","4","6","4","6","7","6","6","6","3","7"],["5","6","5","4","3","7","4","6","5","6","4","6"],["5","7","5","5","5","7","6","4","6","4","4","7"]],[["4","1","6","6","5","2","5","5","3","6","4","1"],["6","6","5","6","5","6","6","5","6","6","4","3"],["4","3","5","6","3","3","5","5","5","6","3","1"],["4","5","4","4","5","2","4","5","5","6","4","4"],["5","2","2","5","4","2","5","5","6","7","4","1"]],[["5","1","1","4","4","2","6","5","4","6","4","1"],["6","6","5","4","6","6","4","5","6","7","4","2"],["6","3","1","2","5","3","7","5","5","6","4","1"],["5","5","3","6","4","2","5","4","4","7","3","3"],["6","3","1","6","3","6","3","5","3","7","4","1"]]]')))



    #print exp5_data
# columns are indiviuals
# each row is a case
# each block is a explanation
    avg = exp5_data.mean(axis=2)

    fig, axes = plt.subplots(2,3)
    for i in range(len(avg)):
        ax1 = axes[i/3][i%3]
        
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
    
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.1), fancybox=True, shadow=True, 
                   ncol=1, fontsize='small')


        ax2 = ax1.twinx()
        ax2.plot([1,2,3,4,5], avg[i], color='g', marker='o', linestyle='--')
        ax2.set_ylabel('Survey Average', color='g')
        for t in ax2.get_yticklabels():
            t.set_color('g')
        
        ax2.set_ylim(0,8)
        ax1.set_xlim(0,6)
    
    ax1.set_title('Explanation '+str(i+1))
    
    fig.set_size_inches(16,14)
    plt.tight_layout(pad=4, h_pad=6, w_pad=2)
    fig.suptitle('Model Predictions for Explanations', fontsize=20, fontweight='bold')
    plt.savefig('plot_explanations_exp5.png', dpi=200, bbox_inches='tight')
            
    max_no_knowledge = np.array(max_no_knowledge).transpose()
    max_knowledge = np.array(max_knowledge).transpose()
    match_no_knowledge = np.array(match_no_knowledge).transpose()
    match_knowledge = np.array(match_knowledge).transpose()
    avg = np.array(avg).transpose()

    fig, axes = plt.subplots(5,1)
    for i in range(len(avg)):
        ax1 = axes[i]
    
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
    
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.15), fancybox=True, shadow=True, 
                   ncol=2, fontsize='small')

        ax2 = ax1.twinx()
        ax2.plot([1,2,3,4,5,6], avg[i], color='g', marker='o', linestyle='--')
        ax2.set_ylabel('Survey Average', color='g')
        for t in ax2.get_yticklabels():
            t.set_color('g')
        
        ax2.set_ylim(0,8)
        ax1.set_xlim(0,7)
    
        ax1.set_title('Case '+str(i+1))
    
    fig.set_size_inches(6,14)
    fig.suptitle('Model Predictions for Cases', fontsize=20, fontweight='bold')
    plt.tight_layout(pad=4, h_pad=3, w_pad=2)
    plt.savefig('plot_cases_exp5.png', dpi=200, bbox_inches='tight')
            


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
            ax_i[2].plot([1,2,3,4,5,6], match_no_knowledge[i], marker='v', linestyle='--',
                         color='c', label='match no knowledge, %.4f' % (c3 if x == 1 else 0))
            ax_i[3].plot([1,2,3,4,5,6], match_knowledge[i], marker='*', linestyle='--', color='m', 
                         label='match knowledge, %.4f' % (c4 if x == 1 else 0))
            map(lambda ax: ax.set_xlabel('Explanations'), ax_i)
            map(lambda ax: ax.set_ylabel('Model Prediction', color='b'), ax_i) if i == 0 else ''

            def setLabels(ax1):
                for t in ax1.get_yticklabels():
                    t.set_color('b')
            map(setLabels, ax_i)

            map(lambda ax1: ax1.legend(loc='upper center', bbox_to_anchor=(0.5,-0.05),
                                       fancybox=True, shadow=True, ncol=4, fontsize='small'), ax_i)

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
        plt.savefig('plot_total_exp5.png' if x==1 else 'plot_prediction.png', dpi=200, bbox_inches='tight')


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
    plt.savefig('plot_human_data_exp5.png', dpi=200, bbox_inches='tight')


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
    plt.savefig('plot_scatter_exp5.png', dpi=200, bbox_inches='tight')



def exp4(knowledge=None, no_knowledge=None, complexity=None, utility=None, ind=1):
    # COMPLEXITY USING 9 for chance nodes
    #knowledge = np.asarray([0.0063180277053399309, 0.010102110589350849, 0.0078424541108970888, 0.0067753815521579648, 0.006882589550070665, 0.0080923941651205224, 0.0086899127185534903, 0.0023242725015461436, 0.0059349889389358774, 0.0052615889954349257, 0.0041276657704530512, 0.0023242725015461436, 0.0067824475465922797])
    #no_knowledge = np.asarray([0.0069716167783061313, 0.011147156512387143, 0.0082100691473453898, 0.0069584999724865582, 0.0072052109352302275, 0.0089295383890985076, 0.0090972523772356855, 0.0025647144844647106, 0.0062131915454484961, 0.0054037941034196539, 0.0043211501034430373, 0.0025647144844647106, 0.0071003747753387927])

    # COMPLEXITY USING CALC VAL FOR CHANCE NODES
    #knowledge = np.asarray([0.018954083116019795, 0.030306331768052547, 0.032170066863067649, 0.0331025784405432, 0.02823266325641232, 0.024277182495361569, 0.035646376661821459, 0.0069728175046384318, 0.024345566871961453, 0.025706620520553496, 0.016931853466552311, 0.0069728175046384318, 0.027821876670715267])
    #no_knowledge = np.asarray([0.019565505152020431, 0.031283955373473595, 0.032840276589381559, 0.033582325954174264, 0.02882084374092091, 0.025060317414566779, 0.036389009508942742, 0.0071977471015622517, 0.024852766181793984, 0.026079180238242676, 0.017284600413772149, 0.0071977471015622517, 0.028401499101355171])

    # USING k=0.2
#    knowledge = np.asarray([0.025585336033686932, 0.023543844876824798, 0.032084363043599497, 0.028904602186319267, 0.025916716673141944, 0.014099636372061675, 0.02458349795845647, 0.017150363627938325, 0.02657580963576367, 0.030299220360434313, 0.027909028350449144, 0.017150363627938325, 0.019074944550620646])
 #   no_knowledge = np.asarray([0.026410669454128444, 0.024303323743819147, 0.032752787273674484, 0.029323509464381867, 0.02645664827049907, 0.0145544633518056, 0.025095654165924314, 0.017703601164323433, 0.027129472336508746, 0.030738339496092781, 0.028490466441083502, 0.017703601164323433, 0.019472339228758576])
    
    # complexity only
    #knowledge = 1.0/np.asarray([88, 88, 182, 308, 182, 88, 182, 88, 182, 308, 182, 88, 182])
    #no_knowledge = 1.0/np.asarray([80, 80, 174, 300, 174, 80, 174, 80, 174, 300, 174, 80, 174])


    # utility only
    #knowledge = np.asarray([0.81873075307798182, 0.75340303605839354, 1.5721337891363754, 2.0233221530423489, 1.2699191169839554, 0.45118836390597361, 1.2045913999643671, 0.54881163609402639, 1.3022146721524199, 2.1209454252304019, 1.3675423891720082, 0.54881163609402639, 0.93467228298041172])
    #no_knowledge = np.asarray([0.81873075307798182, 0.75340303605839354, 1.5721337891363754, 2.0233221530423489, 1.2699191169839554, 0.45118836390597361, 1.2045913999643671, 0.54881163609402639, 1.3022146721524199, 2.1209454252304019, 1.3675423891720082, 0.54881163609402639, 0.93467228298041172])

    # final
    #knowledge = np.asarray([0.0093037585577043398, 0.0085613981370271999, 0.008638097742507558, 0.0065692277696180164, 0.0069775775658459096, 0.0051271404989315181, 0.006618634065738282, 0.0062364958647048458, 0.0071550256711671433, 0.006886186445553253, 0.007513969171274771, 0.0062364958647048458, 0.0051355619943978673])
    #no_knowledge = np.asarray([0.010234134413474774, 0.0094175379507299203, 0.0090352516617033061, 0.0067444071768078297, 0.0072983857297928469, 0.0056398545488246703, 0.0069229390802549836, 0.0068601454511753304, 0.0074839923686920683, 0.0070698180841013399, 0.0078594390182299325, 0.0068601454511753304, 0.0053716797872437458])

    k1 = np.asarray([0.0086619997042744496, 0.0076004559818575882, 0.0084116150100682942, 0.0069137240841744543, 0.0072737307664943289, 0.0054005464442812541, 0.0067246564273131934, 0.0015261891402556084, 0.0060539939325679019, 0.0064999110555018268, 0.0066030682717490366, 0.0041039322877736897, 0.0047206785114378598])
    k2 = np.asarray([0.0086619997042744496, 0.0072361618422495111, 0.0082231870068227384, 0.0064826830710552558, 0.006763575058822564, 0.0044142454094491758, 0.0060260727163958727, 0.0015261891402556084, 0.0064657491148185382, 0.0067539727636990289, 0.0072032514572452303, 0.0052642864463996646, 0.0045322505081923032])
    k3 = np.asarray([0.0067527214989165571, 0.0067688664369732286, 0.0069939247944257512, 0.0053204245374573198, 0.0051216191967550203, 0.0031490756148098153, 0.0051299700267843328, 0.0031490756148098153, 0.0069939247944257512, 0.0064705242877041522, 0.0069855739643964387, 0.0067527214989165571, 0.0051299700267843328])
    k4 = np.asarray([0.0052642864463996646, 0.0061694469787649487, 0.0059140000474989371, 0.0041361454996021981, 0.0035123149586147959, 0.0015261891402556084, 0.0039805014408727021, 0.0044142454094491758, 0.0076714379395031364, 0.0064135318498209767, 0.0072032514572452303, 0.0086619997042744496, 0.0054743236490762707])

    u1 = np.asarray([0.77957997338470042, 0.68404103836718289, 1.4636210117518833, 1.9496701917371961, 1.2656291533700132, 0.48604917998531283, 1.1700902183524957, 0.13735702262300475, 1.0533949442668149, 1.8329749176515153, 1.1489338792843324, 0.36935390589963202, 0.82139806099018764])
    u2 = np.asarray([0.77957997338470042, 0.651254565802456, 1.4308345391871564, 1.8281166260375821, 1.1768620602351261, 0.39728208685042576, 1.0485366526528819, 0.13735702262300475, 1.1250403459784257, 1.9046203193631261, 1.2533657535606701, 0.47378578017596978, 0.78861158842546075])
    u3 = np.asarray([0.60774493490249015, 0.60919797932759057, 1.2169429142300807, 1.5003597195629641, 0.89116174023537353, 0.28341680533288338, 0.89261478466047395, 0.28341680533288338, 1.2169429142300807, 1.8246878491325709, 1.2154898698049803, 0.60774493490249015, 0.89261478466047395])
    u4 = np.asarray([0.47378578017596978, 0.55525022808884539, 1.0290360082648151, 1.1663930308878199, 0.61114280279897448, 0.13735702262300475, 0.69260725071185014, 0.39728208685042576, 1.3348302014735458, 1.8086159816495155, 1.2533657535606701, 0.77957997338470042, 0.95253231493927115])

    c1 = 1.0/np.asarray([90, 90, 174, 282, 174, 90, 174, 90, 174, 282, 174, 90, 174])
    c2 = 1.0/np.asarray([90, 90, 174, 282, 174, 90, 174, 90, 174, 282, 174, 90, 174])
    c3 = 1.0/np.asarray([90, 90, 174, 282, 174, 90, 174, 90, 174, 282, 174, 90, 174])
    c4 = 1.0/np.asarray([90, 90, 174, 282, 174, 90, 174, 90, 174, 282, 174, 90, 174])
    

    def normalize_survey_data(d):
        for i in range(len(d[0])): # for each user
            ut = 0.0
            for j in range(len(d)): # for each entry
                ut += d[j][i]
            for j in range(len(d)): # update each value
                d[j][i] = float(d[j][i]) / ut
        return d

    survey_data_x2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["7","7","7","7","7","7","7","7","7","7","7","7","7","4"],["7","7","7","7","7","2","1","7","7","7","7","7","3","1"],["7","7","7","7","7","2","7","7","7","7","5","7","7","4"],["7","3","7","5","6","3","7","7","6","7","7","7","6","3"],["5","5","6","5","6","6","7","6","4","7","3","7","6","7"],["3","2","5","1","2","5","4","2","4","5","4","7","5","1"],["4","4","7","5","3","3","7","6","7","7","3","7","6","5"],["1","1","1","1","1","7","1","1","1","1","2","1","1","1"],["3","1","2","6","5","4","3","3","2","1","4","2","1","4"],["7","4","4","6","7","2","3","6","4","5","3","3","6","5"],["6","5","3","6","6","7","6","6","4","3","4","2","3","5"],["3","2","2","6","2","3","2","2","1","1","2","1","1","5"],["1","1","1","1","4","4","1","1","1","1","1","1","1","4"]]')), dtype='float64'))

    survey_data_x1 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["7","7","5","2","7","7","3","6","7","7","5","1","4","7"],["2","7","6","2","7","2","3","6","7","5","5","1","4","7"],["6","7","6","5","7","6","4","6","7","6","4","1","5","7"],["6","7","5","6","7","7","4","6","7","7","5","1","4","5"],["6","7","4","3","7","5","3","6","7","4","3","1","4","6"],["2","7","4","6","7","2","3","6","6","4","3","1","1","5"],["6","7","4","4","7","7","4","6","7","6","3","1","4","5"],["1","7","6","7","1","1","1","1","1","1","1","1","1","1"],["2","7","4","7","2","1","2","6","3","3","2","1","1","1"],["6","1","6","2","3","2","3","6","4","4","4","1","4","3"],["5","1","6","7","2","5","3","6","5","5","3","1","1","3"],["1","1","3","5","1","1","2","6","1","2","2","1","1","2"],["2","1","1","5","1","1","1","2","3","1","1","1","1","1"]]')), dtype='float64'))

    survey_data_x3 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["6","5","5","5","5","5","6","4","6","7","6","4","4","1","6"],["7","6","2","4","6","6","7","4","6","1","5","6","5","7","6"],["7","6","2","3","5","4","4","4","6","1","4","6","5","1","6"],["1","3","4","1","3","3","6","1","3","1","4","2","4","1","7"],["1","2","1","1","2","2","7","1","2","7","6","3","4","3","1"],["1","3","3","1","3","2","5","1","2","4","4","1","4","4","5"],["1","5","3","2","4","2","6","1","2","4","5","4","4","3","6"],["1","3","2","1","2","1","5","1","1","1","4","1","5","3","1"],["7","6","4","7","5","6","6","4","5","5","5","6","3","3","6"],["7","6","3","7","6","7","7","7","7","1","7","6","4","3","6"],["7","6","5","7","6","7","6","7","6","7","5","6","4","3","7"],["6","5","2","3","5","4","7","4","6","1","5","4","4","1","5"],["1","3","1","2","3","4","4","1","2","1","6","3","4","3","7"]]')), dtype='float64'))

    survey_data_x4 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["2","3","2","5","1","1","3","1","1","2","2","2","1","2","1"],["6","5","5","5","6","6","3","6","6","6","6","7","7","5","1"],["1","3","4","4","4","2","4","4","3","1","2","1","5","6","1"],["1","1","2","1","1","1","1","1","1","1","3","1","7","2","1"],["1","1","1","1","1","1","1","1","1","2","2","1","1","1","1"],["1","1","1","1","1","1","1","1","1","1","2","1","1","1","1"],["1","3","2","1","1","1","1","2","1","2","2","2","1","2","1"],["4","6","2","3","4","6","2","6","5","5","4","5","5","3","1"],["6","2","6","7","6","6","7","7","6","7","6","6","6","7","1"],["2","5","5","3","5","3","6","4","5","1","3","3","6","6","2"],["3","1","6","7","3","3","6","5","4","2","3","2","5","6","1"],["7","7","7","7","7","7","7","7","7","5","7","7","7","7","7"],["4","7","4","6","7","6","6","4","6","6","6","6","7","7","1"]]')), dtype='float64'))

    sd = (survey_data_x1, survey_data_x2, survey_data_x3, survey_data_x4)

    labels = ['Near A', 'Far C', 'Near A, Far C', 'Near A, Far B and C', 'Near A, Far B', 'Far B', 'Far B and C', 'Far A', 'Near B, Far C', 'Near A and B, Far C', 'Near A and B', 'Near B', 'Far A and C']
    
    ind = 5

#    survey_data = sd[ind-1]
    fn = 'x'+str(ind)
    knowledge = np.concatenate((k1/k1.sum(),k2 / k2.sum(),k3 / k3.sum(), k4 / k4.sum()))
#    knowledge = knowledge / knowledge.sum()
#    no_knowledge = no_knowledge / no_knowledge.sum()
#    predictions = (no_knowledge, knowledge)
    predictions = [knowledge,knowledge]
#    complexity = complexity / complexity.sum()
 #   utility = utility / utility.sum()
    complexity = np.concatenate((c1/c1.sum(),c2/c2.sum(),c3/c3.sum(),c4/c4.sum()))
    utility = np.concatenate((u1/u1.sum(),u2/u2.sum(),u3/u3.sum(),u4/u4.sum()))
    
    #sumTotal = survey_data.sum(axis=1)
    #mean = survey_data.mean(axis=1)
    #std = survey_data.std(axis=1)
    #stderr = std / np.sqrt(15)
    mean = np.asarray([])
    stderr = np.asarray([])
    for i in range(len(sd)):
        mean = np.concatenate((mean,sd[i].mean(axis=1)))
        stderr = np.concatenate((stderr, sd[i].std(axis=1)/np.sqrt(15)))

    fig, ax = plt.subplots(1,2)
    ax[0].set_title('Near Function')
    ax[0].plot(np.arange(0,12,0.1), np.exp(-0.249 * np.arange(0,12,0.1)))
    ax[1].set_title('Far Function')
    ax[1].plot(np.arange(0,12,0.1), 1-np.exp(-0.249 * np.arange(0,12,0.1)))
    fig.set_size_inches(25,10)
        
    fig.suptitle('Utility Exp Functions', fontsize=18, fontweight='bold')
    plt.savefig('plot_utility_exp_functions.png', dpi=200, bbox_inches='tight')
    
    fig, axes = plt.subplots(1,3)
    bar_width = 0.3

    data = (complexity, utility, predictions[1])

    for i in []:#0,1,2]:
#        axe[i].errorbar([1,2,3,4,5,6,7,8,9,10,11,12,13], mean, yerr=std)
        axes[i].bar(np.arange(13)+1, data[i], bar_width, color='#4D4D4D')
       # for t in axes[i].get_yticklabels():
        #    t.set_color('r')
        axes[i].set_xlim(0,14)

        ax2 = axes[i]#.twinx()
        ax2.bar(np.arange(13)+1+bar_width, mean, bar_width, color='#F15854')
        ax2.errorbar(np.arange(13)+1+bar_width+0.15, mean, yerr=stderr,linestyle='', ecolor='#5DA5DA', capsize=3, elinewidth=3)
       # for t in ax2.get_yticklabels():
        #    t.set_color('g')
        
        axes[i].set_title('Complexity' if i == 0 else 'Utility' if i == 1 else 'Combined', fontsize=16)
        #ax2.set_ylim(0,8)
        ax2.set_xlim(0,14)

        axes[i].set_xticks(np.arange(13)+1)
        axes[i].set_xticklabels(labels, rotation=75, fontsize=16)

 #   fig.set_size_inches(40,10)
 #       
 #   fig.suptitle('Case '+str(ind), fontsize=28, fontweight='bold')
 #   plt.savefig('plot_human_data_exp4_'+fn+'.png', dpi=300, bbox_inches='tight')
 #
 #   fig, axes = plt.subplots(1,1)
 #   axes.bar(np.arange(13)+1, data[2], bar_width, color='#4D4D4D')
 #   axes.set_xlim(0,14)
 #
 #   ax2 = axes
 #   ax2.bar(np.arange(13)+1+bar_width, mean, bar_width, color='#F15854')
 #   ax2.errorbar(np.arange(13)+1+bar_width+0.15, mean, yerr=stderr,linestyle='', ecolor='#5DA5DA', capsize=3, elinewidth=3)
 #   ax2.set_xlim(0,14)

  #  axes.set_xticks(np.arange(13)+1)
  #  axes.set_xticklabels(labels, rotation=75, fontsize=16)

   # fig.set_size_inches(10,10)
        
   # fig.suptitle('Case '+str(ind), fontsize=28, fontweight='bold')
   # plt.savefig('plot_human_data_exp4_case'+str(ind)+'_'+fn+'.png', dpi=300, bbox_inches='tight')

    # scatter plot
    fig, axes = plt.subplots(1,3)
    fig.suptitle('Model Predictions vs. Human Data', fontsize=20, fontweight='bold', y=1.05)
    print mean

    cor = corr(data[0], mean)
    axes[0].errorbar(mean, data[0], xerr=stderr, linestyle='')
    axes[0].plot(mean, data[0], color='r', label='Corr = %0.4f' % cor, marker = 'o', 
                 linestyle='')
    axes[0].set_ylabel('Complexity Values', color='g')        
    axes[0].set_title('Complexity Vs. Survey Data')
    axes[0].set_xlabel('Survey Data')
    axes[0].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


    cor = corr(data[1], mean)
    axes[1].errorbar(mean, data[1], xerr=stderr, linestyle='')
    axes[1].plot(mean, data[1], color='r', label='Corr = %0.4f' % cor, marker = 'o', linestyle='')
    axes[1].set_ylabel('Utility', color='g')        
    axes[1].set_title('Utility vs Survey Data')
    axes[1].set_xlabel('Survey Data')
    axes[1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')

    cor = corr(data[2], mean)
    axes[2].errorbar(mean, data[2], xerr=stderr, linestyle='')
    axes[2].plot(mean, data[2], color='r', label='Corr = %0.4f' % cor, marker = 'o', linestyle='')
    axes[2].set_ylabel('Combined', color='g')        
    axes[2].set_title('Combined vs Survey Data')
    axes[2].set_xlabel('Survey Data')
    axes[2].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')

    fig.set_size_inches(20,5)
    plt.savefig('plot_scatter_exp4_'+fn+'.png', dpi=300, bbox_inches='tight')


    # scatter plot
    fig, axes = plt.subplots(1,1)
    fig.suptitle('Case '+str(ind), fontsize=20, fontweight='bold')
    

    cor = corr(data[2], mean)
    axes.errorbar(mean, data[2], xerr=stderr, linestyle='')
    axes.plot(mean, data[2], color='r', label='Corr = %0.4f' % cor, marker = 'o', 
                 linestyle='')
    axes.set_ylabel('Model Predictions', color='g')        
    axes.set_title('Model Predictions Vs. Survey Data')
    axes.set_xlabel('Survey Data')
    axes.legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')


    fig.set_size_inches(10,10)
    plt.savefig('plot_scatter_exp4_case'+str(ind)+'_'+fn+'.png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    exp4()
    
