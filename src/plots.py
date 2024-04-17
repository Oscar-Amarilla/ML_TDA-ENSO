import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
import seaborn as sbrn
import pandas as pd
import netCDF4 as nc
import numpy as np
from .transform_and_load import year_month_num

def domain(data:nc._netCDF4.Dataset,year:int,month:int):
    """
    Plots the studied region in this proyect and highlight the 
    Niño 3.4 region in the plot.
    
    Parameters
    ----------
    data: nc._netCDF4.Dataset
        a netCDF data type with the mean SST field  of every 
        timestep of the time range.
    year: int
        Year of interest.
    month: int 
        Month of interest.
    """

    # Get the latitude and longitude variables
    lat_var = data.variables['lat']
    lon_var = data.variables['lon']
    sst = data['sst'][:]

    # Set the latitude and longitude range
    lat_min = 59
    lat_max = 121
    lon_min = 150
    lon_max = 300

    # Get the data and coordinate values
    y = lat_var[lat_min:lat_max]
    x = lon_var[lon_min:lon_max]
    sst_domain = sst[year_month_num(year,month),lat_min:lat_max,lon_min:lon_max]
    
    # Initializinf the plot.
    fig = plt.figure(figsize=(20, 8))

    # Creating a contour plot and adding a colorbar.
    domain = plt.contourf(x, y, sst_domain)
    cbar=fig.colorbar(domain, shrink=0.7, aspect=15)
    cbar.ax.set_ylabel('\N{DEGREE CELSIUS}', rotation=0)

    # Adding a title and axis labels
    months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Ago.', 'Sep.', 'Oct', 'Nov.', 'Dec.']
    title = 'Mean Sea Surface temperature (ºC) - ' + months[month-1] + ' ' + str(year)
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Putting a rectangular patch to highlight the selected region.
    rect = patches.Rectangle((160, -10), 110, 20, 
                             linewidth=2, edgecolor='red', facecolor='none')
    plt.gca().add_patch(rect)

    file_name = 'outputs/' + months[month-1] + '_' + str(year) + '.png'
    plt.savefig(file_name)
    plt.close(fig)

def phases_histo(enso_info:pd.DataFrame,kind:str='actual'):
    """
    Plots a histogram of the ditribution of the ENSO phases.

    Parameters
    ----------
    enso_info: pd.DataFrame
        a pandas DataFrame with information about the ENSO phases.

    kind: str
        a string telling if the data is restricted or not.
    """

    if kind=='actual':
        plot_title = 'Histogram of ENSO phases in the period 1950-2021'
        image_path = 'outputs/Phases_distribution.png'
    else:
        plot_title = 'Restricted histogram of ENSO phases in the period 1950-2021'
        image_path = 'outputs/Phases_distribution_restricted.png'
    counts = enso_info.Phase.value_counts()
    max_value = counts.max()
    ax = sbrn.histplot(data=enso_info['Phase'], shrink=2.5)
    for i in range(3):
         plt.text(i,counts[i] + max_value*0.05,str(counts[i]),ha='center')
    plt.title(plot_title)
    ax.set_ylim(top=max_value*1.15)
    ax.set(xlabel='', xlim=(-1, 3), xticks=[0, 1, 2], xticklabels=['Niña', 'Neutral', 'Niño'])
    plt.savefig(image_path)


def phases_histo_red(enso_info:pd.DataFrame):
    """
    Plots a histogram of the ditribution of the ENSO phases.

    Parameters
    ----------
    enso_info: pd.DataFrame
        a pandas DataFrame with information about the ENSO phases.

    kind: str
        a string telling if the data is restricted or not.
    """
    plot_title = 'Redistributed histogram of ENSO phases in the period 1950-2021'
    image_path = 'outputs/Phases_redistribution_restricted.png'
    counts = enso_info.Phase.value_counts()
    max_value = counts.max()
    ax = sbrn.histplot(data=enso_info['Phase'], bins=5, shrink=1)
    for i in range(5):
         plt.text(i,counts[i] + max_value*0.05,str(counts[i]),ha='center')
    plt.title(plot_title)
    ax.set_ylim(top=max_value*1.15)
    ax.set(xlabel='', xlim=(-1, 5), xticks=[0, 1, 2, 3, 4], xticklabels=['Niña', 'Trans(+)', 'Neutral', 'Trans(-)', 'Niño'])
    plt.savefig(image_path)

def neutro_distribution(enso_info:pd.DataFrame,neutral_index:list):
    """
    Plots a histogram of the ditribution of the normal conditions with respect
    to the SST anomaly.

    Parameters
    ----------
    enso_info: pd.DataFrame
        a pandas DataFrame with information about the ENSO phases.

    neutral_index: list
        a list with the indexes of the rows related to the neutral conditions 
        in enso_info.
    """
    limits = [enso_info[enso_info["cat"]=='ln']['Anomaly (ºC)'].max(),
             enso_info[enso_info["cat"]=='un']['Anomaly (ºC)'].max(),
             enso_info[enso_info["cat"]=='c']['Anomaly (ºC)'].max(),
             enso_info[enso_info["cat"]=='lp']['Anomaly (ºC)'].max()]

    proportions = (enso_info["cat"].value_counts(normalize=True)[["ln","un","c","lp","up"]]*100).round()

    ax = sbrn.histplot(data=enso_info['Anomaly (ºC)'][neutral_index],color='green',kde=True)
    for limit in limits:
        ax.axvline(x=limit, color='r', linestyle='--')
    ax.set_ylim(top=70*1.15)
    for i in range(5):
         plt.text(-0.75+0.36*i,70,str(proportions[i])+'%',ha='center')
    plt.title('Distribution of neutral phase with respect to the SST anomaly');
    plt.savefig('outputs/Neutral_actual_vs_strat.png')
    plt.show()

def compared_histo(enso_info:pd.DataFrame,enso_info_strat:pd.DataFrame,neutral_index:list,neutral_index_strat:list):
    """
    Plots two histograms, one of the actual ditribution of the neutral phases 
    and a second under constrains.

    Parameters
    ----------
    enso_info: pd.DataFrame
        a pandas DataFrame with information about the ENSO phases.

    enso_info_strt: pd.DataFrame
        a pandas DataFrame with a redistribution of the netrual phases.

    neutral_index: list
        a list with the indexes of the rows related to the neutral conditions 
        in enso_info.
    neutral_index_strat: list
        a list with the indexes of the rows related to the neutral conditions 
        in enso_info_strat.
    """

    ax = sbrn.histplot(data=enso_info['Anomaly (ºC)'][neutral_index], label='Actual ditribution', color='green',kde=True)
    sbrn.histplot(data=enso_info_strat['Anomaly (ºC)'][neutral_index_strat], label='Restricted ditribution', color='blue', kde=True)
    plt.title('Distribution of neutral phase with respect to the SST anomaly');
    plt.legend() 
    plt.savefig('outputs/Neutral_actual_vs_strat.png')
    plt.show()

def sst_field_plot(sst:np.array,year:int,month:int):
    
    """
    Plots a 3-D graph of the studied region in this proyect. 
    
    Parameters
    ----------
    sst: np.array
        a numpy array with the mean SST field of every timestep of 
        the time range.
    year: int
        Year of interest.
    month: int 
        Month of interest.
    """

    # Taking the mean sst of a particular time of the time domain of the field of interest.
    sst_at_t = sst[year_month_num(year,month),79:101,160:270]
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(160, 270, sst_at_t.shape[1])
    y = np.linspace(-10, 10, sst_at_t.shape[0])

    X, Y = np.meshgrid(x, y)
    Z = np.flip(np.array(sst_at_t),axis=0)

    # Plot the triangular surface
    surf = ax.plot_trisurf(X.flatten(), Y.flatten(), Z.flatten(), cmap='viridis', edgecolor='none')

    # Set the axis labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Temperature')
    ax.view_init(elev=45, azim=-125)

    # Show the plot
    months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Ago.', 'Sep.', 'Oct', 'Nov.', 'Dec.']
    title = 'Mean SST (ºC) - ' + months[month-1] + ' ' + str(year)
    ax.set_title(title)
    cbar=fig.colorbar(surf, shrink=0.7, aspect=15)
    cbar.ax.set_ylabel('\N{DEGREE CELSIUS}', rotation=0)
    file_name = 'outputs/sst_field_' + months[month-1] + '_' + str(year) + '.png'
    plt.savefig(file_name)
    plt.show()

def ecc_plot(ecc:pd.DataFrame,year:int,month:int):

    """
    Plots the Euler characteristic curve of the mean SST field of 
    a particular month. 
    
    Parameters
    ----------
    ecc: pd.dataframe
        A daframe containing the Euler characteristics curve of every
        mean SST field of the database.
    year: int
        Year of interest.
    month: int 
        Month of interest.
    """
    year_month = str(year) + '_' + str(month)
    ax = plt.gca()
    plt.plot(ecc.loc[year_month])
    ax.set_xticklabels(np.arange(16, 33,1.95).round())    
    plt.xlabel('Temperature (ºC)')
    plt.ylabel('Euler characteristic')
    months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Ago.', 'Sep.', 'Oct', 'Nov.', 'Dec.']
    title = 'Euler characteristic curve - ' + months[month-1] + ' ' + str(year)
    plt.title(title)
    file_name = 'outputs/ecc_' + months[month-1] + '-' + str(year) + '.png'
    plt.savefig(file_name)
    plt.show()

def phases_vs_sst(enso_info:pd.DataFrame,target_names:list):
    """
    Display a histogram of the different labeled event of the 
    ENSO phenomena with respect to the SST anomaly.

    Parameters
    ----------
    enso_info: pd.DataFrame
        A daframe containing the Euler characteristics curve of every
        mean SST field of the database.
    target_names: list
        A list of the events labels.
    """

    phase_colors={
        'Niña':'blue',
        'Transition(-)':'gray',
        'Neutral':'green',
        'Transition(+)':'orange',
        'Niño':'red'
    }

    indexes={}
    for i,key in enumerate(target_names):
        indexes[key] = enso_info[enso_info['Phase']==i].index.tolist()

    sst_data={}
    for key in target_names:
        sst_data[key] = pd.DataFrame([enso_info['Anomaly (ºC)'][i] for i in indexes[key]])

    for key in target_names:
        sbrn.histplot(data=sst_data[key], x=0, color=phase_colors[key],label=key, kde=True)

    plt.title('ENSO phase histogram based on SST anomaly');
    plt.xlabel('Anomaly in the SST (ºC)')
    plt.legend() 
    plt.savefig('outputs/Phases_vs_SST.png')

    plt.show()

def descr_phase_plot(
    ninha_ecc_dscr: pd.DataFrame, 
    neutral_ecc_dscr: pd.DataFrame, 
    ninho_ecc_dscr: pd.DataFrame):
    """
    Display three plots showing the average and 
    the standard deviation of the ECC of the temperature
    fields grouped by the ENSO phenomena phase 
    each one is related to.

    Parameters
    ----------
    *_ecc_dscr: pd.DataFrame
        A daframe containing the Euler characteristics curve of every
        mean SST field related to the * phase.
    """

    fig, axs = plt.subplots(1, 3, figsize=(30, 7), sharex=True, sharey=True)
    axs = axs.flatten()
    
    # First subplot
    ax1 = axs[0]
    ninha_ecc_dscr['mean'].plot(ax=ax1, legend=False, lw=3)
    ax1.fill_between( ninha_ecc_dscr.index, ninha_ecc_dscr.lower_bound, ninha_ecc_dscr.upper_bound, alpha=0.3)
    ax1.grid(True)
    ax1.set_title('Niña', fontsize=25)
    ax1.set_xlabel('Temperature (Cº)', fontsize=20)
    ax1.set_ylabel('Euler Characteristic', fontsize=20)
    ax1.tick_params(axis='x', labelsize=20)
    ax1.tick_params(axis='y', labelsize=20)
    
    # Second subplot
    ax2 = axs[1]
    neutral_ecc_dscr['mean'].plot(ax=ax2, legend=False, lw=3)
    ax2.fill_between( neutral_ecc_dscr.index, neutral_ecc_dscr.lower_bound, neutral_ecc_dscr.upper_bound, alpha=0.3)
    ax2.grid(True)
    ax2.set_title('Neutral', fontsize=25)
    ax2.set_xlabel('Temperature (Cº)', fontsize=20)
    ax2.tick_params(axis='x', labelsize=20)
    
    # Third subplot
    ax3 = axs[2]
    ninho_ecc_dscr['mean'].plot(ax=ax3, legend=False, lw=3)
    ax3.fill_between( ninho_ecc_dscr.index, ninho_ecc_dscr.lower_bound, ninho_ecc_dscr.upper_bound, alpha=0.3)
    ax3.grid(True)
    ax3.legend(loc='upper left', fontsize=25)
    ax3.set_title('Niño', fontsize=25)
    ax3.set_xlabel('Temperature (Cº)', fontsize=20)
    ax3.tick_params(axis='x', labelsize=20)
    
    fig.suptitle('Descriptive values of each level\n', fontsize=30)
    plt.tight_layout()
    plt.savefig('outputs/ECC_descriptive_values')
    plt.show()

def deep_descr_phase_plot(
    ninha_ecc_weak_dscr: pd.DataFrame, 
    ninha_ecc_moderate_dscr: pd.DataFrame, 
    ninha_ecc_strong_dscr: pd.DataFrame,
    ninho_ecc_weak_dscr: pd.DataFrame, 
    ninho_ecc_moderate_dscr: pd.DataFrame, 
    ninho_ecc_strong_dscr: pd.DataFrame):
    """
    Display six plots showing the average and 
    the standard deviation of the ECC of the temperature
    fields grouped by the ENSO phenomena phase 
    each one is related to.

    Parameters
    ----------
    *_ecc_#_dscr: pd.DataFrame
        A daframe containing the Euler characteristics curve of every
        mean SST field related to the * phase of # category.
    """

    fig, axs = plt.subplots(2, 3, figsize=(30, 10), sharex=True, sharey=True)
    axs = axs.flatten()
    
    # First subplot
    ax1 = axs[0]
    ninha_ecc_weak_dscr['mean'].plot(ax=ax1, legend=False, lw=3)
    ax1.fill_between(ninha_ecc_weak_dscr.index, ninha_ecc_weak_dscr.lower_bound, ninha_ecc_weak_dscr.upper_bound, alpha=0.3)
    ax1.grid(True)
    ax1.set_xlabel('Temperature (Cº)', fontsize=20)
    ax1.set_ylabel('Euler Characteristic', fontsize=20)
    ax1.set_title('Niña weak', fontsize=25)
    ax1.tick_params(axis='y', labelsize=20)
    
    # Third subplot
    ax2 = axs[3]
    ninho_ecc_weak_dscr['mean'].plot(ax=ax2, legend=False, lw=3)
    ax2.fill_between(ninho_ecc_weak_dscr.index, ninho_ecc_weak_dscr.lower_bound, ninho_ecc_weak_dscr.upper_bound, alpha=0.3)
    ax2.grid(True)
    ax2.set_title('Niño weak', fontsize=25)
    ax2.set_xlabel('Temperature (Cº)', fontsize=20)
    ax2.set_ylabel('Euler Characteristic', fontsize=20)
    ax2.tick_params(axis='x', labelsize=20)
    ax2.tick_params(axis='y', labelsize=20)
    
    # Second subplot
    ax3 = axs[1]
    ninha_ecc_moderate_dscr['mean'].plot(ax=ax3, legend=False, lw=3)
    ax3.fill_between(ninha_ecc_moderate_dscr.index, ninha_ecc_moderate_dscr.lower_bound, ninha_ecc_moderate_dscr.upper_bound, alpha=0.3)
    ax3.grid(True)
    ax3.set_title('Niña moderate', fontsize=25)
    
    # Third subplot
    ax4 = axs[4]
    ninho_ecc_moderate_dscr['mean'].plot(ax=ax4, legend=False, lw=3)
    ax4.fill_between(ninho_ecc_moderate_dscr.index, ninho_ecc_moderate_dscr.lower_bound, ninho_ecc_moderate_dscr.upper_bound, alpha=0.3)
    ax4.grid(True)
    ax4.set_title('Niño moderate', fontsize=25)
    ax4.set_xlabel('Temperature (Cº)', fontsize=20)
    ax4.tick_params(axis='x', labelsize=20)
    
    # Second subplot
    ax5 = axs[2]
    ninha_ecc_strong_dscr['mean'].plot(ax=ax5, legend=False, lw=3)
    ax5.fill_between(ninha_ecc_strong_dscr.index, ninha_ecc_strong_dscr.lower_bound, ninha_ecc_strong_dscr.upper_bound, alpha=0.3)
    ax5.grid(True)
    ax5.set_title('Niña strong', fontsize=25)
    ax5.legend(loc='upper right', fontsize=25)
    
    # Third subplot
    ax6 = axs[5]
    ninho_ecc_strong_dscr['mean'].plot(ax=ax6, legend=False, lw=3)
    ax6.fill_between(ninho_ecc_strong_dscr.index, ninho_ecc_strong_dscr.lower_bound, ninho_ecc_strong_dscr.upper_bound, alpha=0.3)
    ax6.grid(True)
    ax6.set_title('Niño strong', fontsize=25)
    ax6.set_xlabel('Temperature (Cº)', fontsize=20)
    ax6.tick_params(axis='x', labelsize=20)
    
    fig.suptitle('Descriptive values of each level\n', fontsize=30)
    plt.tight_layout()
    plt.savefig('outputs/ECC_descriptive_values_strong_cases')
    plt.show()
