def figure3(subject, xlabel, ylabel, title):
    '''
    Common plot frame for panels in figure3
    Args:
        subject (list)
        xlabel (string)
        ylabel (string)
        title (string)
    Returns:
        fig (figure)
    '''
    fig, ax= plt.subplots()
    i = 0
    for x in subject:
        ax.plot(x[0], x[1])
        ax.plot(x[0], x[2])
        ax.fill_between(x[0], x[1],x[2], color="xkcd:light gray")
        if i == 0:
            ax.plot(x[0], x[3], ":", label = "x-axis:believed score")
            i = i+1
        else:
            ax.plot(x[0], x[3],"-" ,label = "x-axis:true score")
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
        
    return fig