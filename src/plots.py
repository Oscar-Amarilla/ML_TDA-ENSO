import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sbrn
import pandas as pd
import netCDF4 as nc
from .transform_and_load import year_month_num

def domain(data:nc._netCDF4.Dataset):

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
    sst_domain = sst[year_month_num(2017,6),lat_min:lat_max,lon_min:lon_max]
    
    # Initializinf the plot.
    fig = plt.figure(figsize=(20, 8))

    # Creating a contour plot and adding a colorbar.
    plt.contourf(x, y, sst_domain)
    plt.colorbar()

    # Adding a title and axis labels
    plt.title('Mean Sea Surface temperature (ºC) - June 2017')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Putting a rectangular patch to highlight the selected region.
    rect = patches.Rectangle((160, -10), 110, 20, 
                             linewidth=2, edgecolor='red', facecolor='none')
    plt.gca().add_patch(rect)

    plt.savefig('outputs/june_17.png')
    plt.close(fig)

def first_histo(enso_info:pd.DataFrame,kind:str='actual'):
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

def neutro_distribution(enso_info:pd.DataFrame,neutral_index:list):
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
    ax = sbrn.histplot(data=enso_info['Anomaly (ºC)'][neutral_index], label='Actual ditribution', color='green',kde=True)
    sbrn.histplot(data=enso_info_strat['Anomaly (ºC)'][neutral_index_strat], label='Restricted ditribution', color='blue', kde=True)
    plt.title('Distribution of neutral phase with respect to the SST anomaly');
    plt.legend() 
    plt.savefig('outputs/Neutral_actual_vs_strat.png')
    plt.show()
