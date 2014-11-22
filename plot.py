import matplotlib.pyplot as plt
import numpy as np
import json

def corr(x,y):
    """
    Computes the correlation between x and y
    """
    cm = np.cov(x,y)
    if cm[0][0] == 0 or cm[1][1] == 0:
        c = 0
    else:
        c = cm[0][1] / np.sqrt(cm[0][0] * cm[1][1])
    return c


def get_exp_data():
    """
    Gets the survey data for this experiment
    """
    def normalize_survey_data(d):
        """
        Normalizes the data per user so that it sums to one and
        can be more easily compared to the model predictions.
        """
        for i in range(len(d[0])): # for each user
            ut = 0.0
            for j in range(len(d)): # for each entry
                ut += d[j][i]
            for j in range(len(d)): # update each value
                d[j][i] = float(d[j][i]) / ut
        return d

    survey_data_x1 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["7","7","5","2","7","7","3","6","7","7","5","1","4","7"],["2","7","6","2","7","2","3","6","7","5","5","1","4","7"],["6","7","6","5","7","6","4","6","7","6","4","1","5","7"],["6","7","5","6","7","7","4","6","7","7","5","1","4","5"],["6","7","4","3","7","5","3","6","7","4","3","1","4","6"],["2","7","4","6","7","2","3","6","6","4","3","1","1","5"],["6","7","4","4","7","7","4","6","7","6","3","1","4","5"],["1","7","6","7","1","1","1","1","1","1","1","1","1","1"],["2","7","4","7","2","1","2","6","3","3","2","1","1","1"],["6","1","6","2","3","2","3","6","4","4","4","1","4","3"],["5","1","6","7","2","5","3","6","5","5","3","1","1","3"],["1","1","3","5","1","1","2","6","1","2","2","1","1","2"],["2","1","1","5","1","1","1","2","3","1","1","1","1","1"]]')), dtype='float64'))
    survey_data_x1_2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["7","7","3","7","7","7","7","7","7","7","7","7","4","7","6"],["7","7","2","7","7","1","7","7","6","7","7","7","3","1","6"],["7","7","4","7","7","7","7","7","7","7","6","7","3","7","6"],["7","6","3","7","5","7","7","7","7","6","5","7","6","4","7"],["7","6","4","7","7","7","7","5","4","5","5","7","5","4","4"],["7","5","4","7","7","1","7","6","5","5","4","7","3","4","3"],["7","7","2","7","7","7","7","7","7","6","5","6","4","1","6"],["1","1","4","1","1","1","1","1","1","1","1","2","3","1","1"],["7","4","5","1","7","7","6","3","3","2","3","5","3","1","4"],["7","4","5","1","5","5","1","5","7","4","5","6","4","4","6"],["7","4","5","1","5","1","5","6","7","5","6","5","5","4","6"],["1","2","4","1","1","1","1","4","1","1","3","5","4","1","1"],["1","1","2","1","1","1","1","3","1","1","1","7","5","1","1"]]')), dtype='float64'))

    survey_data_x2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["7","7","7","7","7","7","7","7","7","7","7","7","7","4"],["7","7","7","7","7","2","1","7","7","7","7","7","3","1"],["7","7","7","7","7","2","7","7","7","7","5","7","7","4"],["7","3","7","5","6","3","7","7","6","7","7","7","6","3"],["5","5","6","5","6","6","7","6","4","7","3","7","6","7"],["3","2","5","1","2","5","4","2","4","5","4","7","5","1"],["4","4","7","5","3","3","7","6","7","7","3","7","6","5"],["1","1","1","1","1","7","1","1","1","1","2","1","1","1"],["3","1","2","6","5","4","3","3","2","1","4","2","1","4"],["7","4","4","6","7","2","3","6","4","5","3","3","6","5"],["6","5","3","6","6","7","6","6","4","3","4","2","3","5"],["3","2","2","6","2","3","2","2","1","1","2","1","1","5"],["1","1","1","1","4","4","1","1","1","1","1","1","1","4"]]')), dtype='float64'))
    survey_data_x2_2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["6","7","7","7","7","6","7","7","7","6","5","5","7","6","7"],["4","7","7","7","7","6","7","7","7","4","6","6","5","4","7"],["6","7","7","7","7","7","7","7","7","5","5","5","6","6","7"],["5","7","7","7","7","3","7","4","6","5","6","6","3","5","4"],["4","7","7","7","7","5","7","3","4","5","5","4","3","5","5"],["4","4","7","7","7","4","5","3","4","5","6","2","2","5","5"],["4","7","7","7","7","4","7","4","4","5","5","6","4","4","5"],["1","1","1","1","1","1","7","1","1","5","2","1","1","1","1"],["2","2","5","7","7","3","5","1","4","2","2","1","6","5","3"],["4","2","5","5","5","5","3","3","5","4","3","5","6","5","4"],["3","3","1","1","1","4","4","2","4","2","2","2","5","5","4"],["3","4","1","1","1","1","1","2","3","5","1","2","4","3","3"],["2","1","1","1","1","1","6","1","1","6","3","1","1","1","2"]]')), dtype='float64'))

    survey_data_x3 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["6","5","5","5","5","5","6","4","6","7","6","4","4","1","6"],["7","6","2","4","6","6","7","4","6","1","5","6","5","7","6"],["7","6","2","3","5","4","4","4","6","1","4","6","5","1","6"],["1","3","4","1","3","3","6","1","3","1","4","2","4","1","7"],["1","2","1","1","2","2","7","1","2","7","6","3","4","3","1"],["1","3","3","1","3","2","5","1","2","4","4","1","4","4","5"],["1","5","3","2","4","2","6","1","2","4","5","4","4","3","6"],["1","3","2","1","2","1","5","1","1","1","4","1","5","3","1"],["7","6","4","7","5","6","6","4","5","5","5","6","3","3","6"],["7","6","3","7","6","7","7","7","7","1","7","6","4","3","6"],["7","6","5","7","6","7","6","7","6","7","5","6","4","3","7"],["6","5","2","3","5","4","7","4","6","1","5","4","4","1","5"],["1","3","1","2","3","4","4","1","2","1","6","3","4","3","7"]]')), dtype='float64'))
    survey_data_x3_2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["4","5","5","7","7","7","3","7","6","5","5","4","6","5","6"],["6","7","6","7","7","7","4","4","7","6","4","5","7","7","7"],["5","6","4","7","7","7","4","6","6","3","2","4","6","6","7"],["4","5","5","5","4","1","3","5","1","5","3","2","4","1","1"],["4","2","4","1","1","1","3","4","1","1","4","2","4","1","1"],["2","5","5","1","1","5","1","2","1","1","3","1","2","1","2"],["4","5","3","1","5","6","3","4","1","3","3","2","2","1","2"],["2","5","3","1","1","5","3","1","1","2","2","1","1","1","2"],["5","5","3","7","7","7","4","2","4","5","4","5","6","6","7"],["6","7","4","7","7","7","4","3","6","3","6","7","7","5","7"],["4","5","5","7","7","7","3","5","6","7","5","7","7","5","7"],["4","5","4","7","7","7","3","4","6","5","4","4","6","4","7"],["2","6","5","1","1","1","3","7","1","1","3","1","2","1","1"]]')), dtype='float64'))

    survey_data_x4 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["2","3","2","5","1","1","3","1","1","2","2","2","1","2","1"],["6","5","5","5","6","6","3","6","6","6","6","7","7","5","1"],["1","3","4","4","4","2","4","4","3","1","2","1","5","6","1"],["1","1","2","1","1","1","1","1","1","1","3","1","7","2","1"],["1","1","1","1","1","1","1","1","1","2","2","1","1","1","1"],["1","1","1","1","1","1","1","1","1","1","2","1","1","1","1"],["1","3","2","1","1","1","1","2","1","2","2","2","1","2","1"],["4","6","2","3","4","6","2","6","5","5","4","5","5","3","1"],["6","2","6","7","6","6","7","7","6","7","6","6","6","7","1"],["2","5","5","3","5","3","6","4","5","1","3","3","6","6","2"],["3","1","6","7","3","3","6","5","4","2","3","2","5","6","1"],["7","7","7","7","7","7","7","7","7","5","7","7","7","7","7"],["4","7","4","6","7","6","6","4","6","6","6","6","7","7","1"]]')), dtype='float64'))
    survey_data_x4_2 = normalize_survey_data(np.asarray(map(lambda x: map(lambda y: int(y), x), json.loads('[["4","2","2","3","1","1","1","3","3","3","1","2","3","1","2"],["4","3","6","5","7","7","7","5","6","5","4","4","5","4","7"],["3","4","3","5","1","7","7","1","2","3","4","2","5","6","5"],["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"],["1","2","1","1","1","1","1","1","1","2","1","1","1","1","1"],["1","1","1","3","1","1","1","1","1","1","1","1","1","1","1"],["4","4","1","3","1","1","1","1","2","1","2","1","1","1","1"],["5","6","3","4","7","7","7","2","4","5","1","3","3","7","6"],["6","6","7","3","7","7","7","5","6","6","7","4","5","7","7"],["4","4","2","1","5","7","6","4","4","6","5","3","5","6","5"],["4","4","4","1","1","1","1","3","4","4","6","2","5","3","4"],["7","6","7","3","7","7","7","7","7","7","7","6","6","7","7"],["6","6","2","5","7","6","7","3","4","6","6","4","5","6","7"]]')), dtype='float64'))
    
    survey_data_x1 = np.concatenate((survey_data_x1,survey_data_x1_2), axis=1)
    survey_data_x2 = np.concatenate((survey_data_x2,survey_data_x2_2), axis=1)
    survey_data_x3 = np.concatenate((survey_data_x3,survey_data_x3_2), axis=1)
    survey_data_x4 = np.concatenate((survey_data_x4,survey_data_x4_2), axis=1)
    sd = (survey_data_x1, survey_data_x2, survey_data_x3, survey_data_x4)
    return sd


def exp_plot(knowledge=None, no_knowledge=None, complexity=None, utility=None, ind=1):
    """
    Generates the plots for the first experiment
    """
    sd = get_exp_data()
    
    # explanation labels for plot
    labels = ['Near A', 'Far C', 'Near A, Far C', 'Near A, Far B and C', 'Near A, Far B', 'Far B', 'Far B and C', 'Far A', 'Near B, Far C', 'Near A and B, Far C', 'Near A and B', 'Near B', 'Far A and C']

    # gets the survey data for this case
    survey_data = sd[ind-1]
    # sets up the file name for this case
    fn = 'x'+str(ind)

    # sets up the various model predictions used for this case
    knowledge = knowledge / knowledge.sum()
    no_knowledge = no_knowledge / no_knowledge.sum()
    predictions = (no_knowledge, knowledge)
    complexity = 1.0 / complexity
    complexity = complexity / complexity.sum()
    utility = utility / utility.sum()
    
    # sets up the survey data for plotting
    sumTotal = survey_data.sum(axis=1)
    mean = survey_data.mean(axis=1)
    std = survey_data.std(axis=1)
    stderr = std / np.sqrt(15)

    # plots the near and far exponential functions
    fig, ax = plt.subplots(1,2)
    ax[0].set_title('Near Function')
    ax[0].plot(np.arange(0,12,0.1), np.exp(-0.249 * np.arange(0,12,0.1)))
    ax[1].set_title('Far Function')
    ax[1].plot(np.arange(0,12,0.1), 1-np.exp(-0.249 * np.arange(0,12,0.1)))
    fig.set_size_inches(25,10)
        
    fig.suptitle('Utility Exp Functions', fontsize=18, fontweight='bold')
    plt.savefig('plots/plot_utility_exp_functions.png', dpi=100, bbox_inches='tight')
    

    # plots var plots for complexity, utility and combined metric for this case
    fig, axes = plt.subplots(1,3)
    bar_width = 0.3

    data = (complexity, utility, predictions[1])

    for i in [0,1,2]:
#        axe[i].errorbar([1,2,3,4,5,6,7,8,9,10,11,12,13], mean, yerr=std)
        axes[i].bar(np.arange(13)+1, data[i], bar_width, color='#4D4D4D', label='Model Prediction')
        
       # for t in axes[i].get_yticklabels():
        #    t.set_color('r')
        axes[i].set_xlim(0,14)

        ax2 = axes[i]#.twinx()
        ax2.bar(np.arange(13)+1+bar_width, mean, bar_width, color='#F15854', label='Survey Data')
        ax2.errorbar(np.arange(13)+1+bar_width+0.15, mean, yerr=stderr,linestyle='', ecolor='#5DA5DA', capsize=3, elinewidth=3)
       # for t in ax2.get_yticklabels():
        #    t.set_color('g')
        
        axes[i].set_title('Complexity' if i == 0 else 'Utility' if i == 1 else 'Combined', fontsize=16)
        #ax2.set_ylim(0,8)
        ax2.set_xlim(0,14)

        axes[i].set_xticks(np.arange(13)+1)
        axes[i].set_xticklabels(labels, rotation=75, fontsize=16)

    fig.set_size_inches(20,5)
        
    fig.suptitle('Case '+str(ind), fontsize=28, fontweight='bold')
    plt.savefig('plots/plot_human_data_exp_'+fn+'.png', dpi=200, bbox_inches='tight')



    # plots the model predictions for this case
    fig, axes = plt.subplots(1,1)
    axes.bar(np.arange(13)+1, data[2], bar_width, color='#4D4D4D', label='Model Predictions')
    axes.set_xlim(0,14)

    ax2 = axes
    ax2.bar(np.arange(13)+1+bar_width, mean, bar_width, color='#F15854', label='Survey Data')
    ax2.errorbar(np.arange(13)+1+bar_width+0.15, mean, yerr=stderr,linestyle='', ecolor='#5DA5DA', capsize=3, elinewidth=3)
    ax2.set_xlim(0,14)

    axes.set_xticks(np.arange(13)+1)
    axes.set_xticklabels(labels, rotation=75, fontsize=16)

    
    axes.legend(loc='upper right', fancybox=True, 
                                   shadow=True, ncol=4, fontsize='small')

    fig.set_size_inches(5,5)
        
    fig.suptitle('Case '+str(ind), fontsize=28, fontweight='bold')
    plt.savefig('plots/plot_human_data_exp_case'+str(ind)+'_'+fn+'.png', dpi=100, bbox_inches='tight')
    plt.close(fig)


    # Shows the scatter plot for complexity, utility and combined for this case
    fig, axes = plt.subplots(1,3)
    fig.suptitle('Model Predictions vs. Human Data', fontsize=20, fontweight='bold')
    

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
    plt.savefig('plots/plot_scatter_exp_'+fn+'.png', dpi=100, bbox_inches='tight')
    plt.close(fig)

    # Model predictions vs. data for this case
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


    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_scatter_exp_case'+str(ind)+'_'+fn+'.png', dpi=100, bbox_inches='tight')
    plt.close(fig)

def exp4_full_scatter(predictions, complexity, utility):
    """
    generates the full scatter plot for all 4 cases in one plot
    """
    survey_data = get_exp4_data()

    # sets up the model predictions
    predictions = np.concatenate((predictions[0] / predictions[0].sum(), predictions[1] / predictions[1].sum(), predictions[2] / predictions[2].sum(), predictions[3] / predictions[3].sum()))
    
    complexity = 1.0 / complexity
    complexity = np.concatenate((complexity[0] / complexity[0].sum(), complexity[1] / complexity[1].sum(), complexity[2] / complexity[2].sum(), complexity[3] / complexity[3].sum()))
    utility = np.concatenate((utility[0] / utility[0].sum(), utility[1] / utility[1].sum(), utility[2] / utility[2].sum(), utility[3] / utility[3].sum()))

    data = (complexity, utility, predictions)

    # sets up survey data
    mean = np.concatenate((survey_data[0].mean(axis=1), survey_data[1].mean(axis=1), survey_data[2].mean(axis=1), survey_data[3].mean(axis=1)))
    std = np.concatenate((survey_data[0].std(axis=1), survey_data[1].std(axis=1), survey_data[2].std(axis=1), survey_data[3].std(axis=1)))
    stderr = std / np.sqrt(15)

    # scatter plot
    fig, axes = plt.subplots(1,3)
    fig.suptitle('Model Predictions vs. Human Data', fontsize=20, fontweight='bold')
    
    
    cor = corr(data[0], mean)
    axes[0].errorbar(mean, data[0], xerr=stderr, linestyle='')
    axes[0].plot(mean, data[0], color='r', label='Corr = %0.4f' % cor, marker = 'o', 
                     linestyle='')
    axes[0].set_ylabel('Complexity Values')        
    axes[0].set_title('Complexity Vs. Survey Data')
    axes[0].set_xlabel('Survey Data')
    axes[0].legend(loc='upper left', fancybox=True, 
                   shadow=True, ncol=4, fontsize='small')
    
    
    cor = corr(data[1], mean)
    axes[1].errorbar(mean, data[1], xerr=stderr, linestyle='')
    axes[1].plot(mean, data[1], color='r', label='Corr = %0.4f' % cor, marker = 'o', linestyle='')
    axes[1].set_ylabel('Utility')        
    axes[1].set_title('Utility vs Survey Data')
    axes[1].set_xlabel('Survey Data')
    axes[1].legend(loc='upper left', fancybox=True, 
                   shadow=True, ncol=4, fontsize='small')
    
    cor = corr(data[2], mean)
    axes[2].errorbar(mean, data[2], xerr=stderr, linestyle='')
    axes[2].plot(mean, data[2], color='r', label='Corr = %0.4f' % cor, marker = 'o', linestyle='')
    axes[2].set_ylabel('Combined')        
    axes[2].set_title('Combined vs Survey Data')
    axes[2].set_xlabel('Survey Data')
    axes[2].legend(loc='upper left', fancybox=True, 
                   shadow=True, ncol=4, fontsize='small')
    
    fig.set_size_inches(20,5)
    plt.savefig('plots/plot_scatter_exp.png', dpi=100, bbox_inches='tight')
    plt.close(fig)


def plot_generate():
    """
    Plots the explanations generated by people compared to the survey data
    """
    # represents how many explanations were covered by top model predictions
    # starts at (0,0)
    case_1 = np.asarray([0,7,0,2,1,4,0,0,0,0,0,0,0,0]).cumsum() / 15.0
    case_2 = np.asarray([0,9,3,0,1,1,0,0,1,0,0,0,0,0]).cumsum() / 15.0
    case_3 = np.asarray([0,0,0,9,1,0,1,0,0,0,0,0,0,0]).cumsum() / 15.0
    case_4 = np.asarray([0,8,6,0,0,0,1,0,0,0,0,0,0,0]).cumsum() / 15.0

    fig, axes = plt.subplots(1,1)
    axes.plot(np.arange(14), case_1, color='#F15854', linestyle='-')
    axes.plot(np.arange(14), case_2, color='#B276B2', linestyle='-')
    axes.plot(np.arange(14), case_3, color='#5DA5DA', linestyle='-')
    axes.plot(np.arange(14), case_4, color='#FAA43A', linestyle='-')
    axes.set_ylabel('Percent accounted for')
    axes.set_xlabel('Number of best explanations used')
    axes.set_ylim(0,1.1)
    axes.set_xlim(0,13)
    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_generate_all.png', dpi=100, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(1,1)
    #fig.suptitle('Model predictions compared to generated responses', fontsize=18, fontweight='bold')
    axes.plot(np.arange(14), case_1, color='r', linestyle='-')
    axes.set_ylabel('Percent accounted for')
    axes.set_xlabel('Number of best explanations used')
    axes.set_ylim(0,1.1)
    axes.set_xlim(0,13)
    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_generate_case1.png', dpi=100, bbox_inches='tight')
    plt.close(fig)
  
    fig, axes = plt.subplots(1,1)
    #fig.suptitle('Model predictions compared to generated responses', fontsize=18, fontweight='bold')
    axes.plot(np.arange(14), case_2, color='r', linestyle='-')
    axes.set_ylabel('Percent accounted for')
    axes.set_xlabel('Number of best explanations used')
    axes.set_ylim(0,1.1)
    axes.set_xlim(0,13)
    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_generate_case2.png', dpi=100, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(1,1)
    #fig.suptitle('Model predictions compared to generated responses', fontsize=18, fontweight='bold')
    axes.plot(np.arange(14), case_3, color='r', linestyle='-')
    axes.set_ylabel('Percent accounted for')
    axes.set_xlabel('Number of best explanations used')
    axes.set_ylim(0,1.1)
    axes.set_xlim(0,13)
    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_generate_case3.png', dpi=100, bbox_inches='tight')
    plt.close(fig)

    fig, axes = plt.subplots(1,1)
   # fig.suptitle('Model predictions compared to generated responses', fontsize=18, fontweight='bold')
    axes.plot(np.arange(14), case_4, color='r', linestyle='-')
    axes.set_ylabel('Percent accounted for')
    axes.set_xlabel('Number of best explanations used')
    axes.set_ylim(0,1.1)
    axes.set_xlim(0,13)
    fig.set_size_inches(5,5)
    plt.savefig('plots/plot_generate_case4.png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    
if __name__ == '__main__':
    plot_generate()
