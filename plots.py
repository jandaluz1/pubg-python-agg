import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import figure
import seaborn as sns
from scipy import ndimage
from maps import MAPS, DIMENSIONS, get_map_plot_image
import sys

def get_events_by_map(root_df, map_name):
    return root_df[root_df['map_name'].str.lower() == MAPS[map_name].lower()]

def get_plot_dimensions(map_name):
    return DIMENSIONS[map_name]
    

def plot_landing_events(plot_name, landings_df, dimensions, map_img):
    #negate the y axis
    neg_df = landings_df.copy()
    neg_df['landing_y'] = landings_df['landing_y'].apply(lambda y: y*-1)
    x_lim = (0, dimensions[0])
    y_lim = (-dimensions[1], 0)
    figure(num=None, figsize=(11, 11), dpi=500, facecolor='w', edgecolor='k')
    heatmap = sns.kdeplot(neg_df.landing_x, neg_df.landing_y, shade=True, alpha=0.65, zorder=2, cmap="afmhot", shade_lowest=False, legend=False)
    heatmap.set(yticks=[], xticks=[])
    heatmap.imshow(map_img, aspect=heatmap.get_aspect(), extent=x_lim + y_lim, zorder=1)
    plt.savefig(plot_name, quality=95, transparent=True)



def main(maps=None):
    df = pq.ParquetDataset('data/parquet').read().to_pandas()
    if maps:
        print(maps)
        for map_name in maps:
            map_df = get_events_by_map(df, map_name)
            dimensions = get_plot_dimensions(map_name)
            plt_img = get_map_plot_image(map_name)

            print(f"generate plot for {map_name}")
            try:
                plot_landing_events(f"{map_name}_heat", map_df, dimensions, plt_img)
                print(f'density map for {map_name} created successfully')
            except Exception as e:
                print(f"unable to plot {map_name}")
                print(e)
    else:        
        erangel_df = get_events_by_map(df, 'Erangel')
        dimensions = get_plot_dimensions('Erangel')
        plt_img = get_map_plot_image('Erangel')
        print(f"generate plot for Erangel")
        try:
            plot_landing_events("Erangel_heat", erangel_df, dimensions, plt_img)
        except Exception as e:
            print(f"unable to plot {map_name}")
            print(e)
    
if __name__ == "__main__":    
    if len(sys.argv) > 1:
        maps = sys.argv[1:]
        main(maps)
    else:
        main()
    