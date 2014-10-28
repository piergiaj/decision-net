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
    exp2_data = np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["6","5","5","4","6","7","4","7","5","4","1","7","4","6","7","5","4"],["5","3","6","5","6","4","2","5","5","4","7","5","5","5","1","6","4"],["6","4","5","1","2","7","4","7","1","4","7","4","6","3","7","5","4"],["2","5","5","3","3","2","4","1","1","4","5","5","2","7","1","4","4"],["2","5","5","2","7","5","3","7","5","4","1","4","3","7","1","2","5"],["2","6","4","2","2","5","4","7","1","4","3","4","7","7","7","2","2"]]'))) # is now in the format where columns are the rows

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

    sumTotal = exp2_data.sum(axis=1)
    mean = exp2_data.mean(axis=1)
    std = exp2_data.std(axis=1)

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
    plt.savefig('plot_human_data_exp2.png', dpi=200, bbox_inches='tight')

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
    plt.savefig('plot_scatter_exp2.png', dpi=200, bbox_inches='tight')


    fig, axes = plt.subplots(2,2)
    
    axes[0][0].plot([1,2,3,4,5,6], mean, color='r', marker='o', linestyle='--')
    axes[0][0].set_ylabel('Survey Data', color='r')
    axes[0][0].set_xlim(0,7)
    axes[0][0].set_ylim(0,8)
    axes[0][0].set_title('Exp 2 Data')
    
    axes[0][1].plot([1,2,3,4,5,6], avg[3], color='r', marker='o', linestyle='--')
    axes[0][1].set_ylabel('Survey Data', color='r')
    axes[0][1].set_xlim(0,7)
    axes[0][1].set_ylim(0,8)
    axes[0][1].set_title('Exp 1 Data, Case 4')

    axes[1][0].plot([1,2,3,4,5,6], mean, color='r', marker='o', linestyle='--')
    axes[1][0].set_ylabel('Exp 2 Data', color='r')
    axes[1][0].set_xlim(0,7)
    axes[1][0].set_ylim(0,8)
    axes[1][0].set_title('Exp 1 and Exp 2')
        
    ax2 = axes[1][0].twinx()
    ax2.plot([1,2,3,4,5,6], avg[3], color='g', marker='v', linestyle='--')
    ax2.set_ylabel('Exp 1 Data', color='g') if i == 1 else ''
    for t in ax2.get_yticklabels():
        t.set_color('g')        
    axes[1][0].set_title('Exp 1 and Exp 2')
    ax2.set_ylim(0,8)
    ax2.set_xlim(0,7)


    cor = corr(mean, avg[3])
    axes[1][1].plot(avg[3], mean, color='r', marker='o', linestyle='', label='Corr = %0.4f' % cor)
    axes[1][1].set_ylabel('Exp 2 Data', color='r')
    axes[1][1].set_xlabel('Exp 1 Data')
    axes[1][1].set_xlim(0,7)
    axes[1][1].set_ylim(0,8)
    axes[1][1].legend(loc='upper left', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')
    axes[1][1].set_title('Exp 1 and Exp 2')

    fig.set_size_inches(20,20)
        
    fig.suptitle('Experiment 1 (case 4) and 2 Comparison', fontsize=18, fontweight='bold')
    plt.savefig('plot_exp1_exp2_compare.png', dpi=200, bbox_inches='tight')


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
    plt.savefig('plot_explanations.png', dpi=200, bbox_inches='tight')
            
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
    plt.savefig('plot_cases.png', dpi=200, bbox_inches='tight')
            


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
        plt.savefig('plot_total.png' if x==1 else 'plot_prediction.png', dpi=200, bbox_inches='tight')


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
    plt.savefig('plot_human_data.png', dpi=200, bbox_inches='tight')


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
    plt.savefig('plot_scatter.png', dpi=200, bbox_inches='tight')




if __name__ == '__main__':
    exp2()
