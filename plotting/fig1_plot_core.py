"""Core plotting snippet for Figure 1.

Note:
The elevation files used for panels (b) and (d) are not included in this repository
because of file size limitations and should be downloaded separately.
"""

file_all = '../data/fig1/LLJ_frequency_all_2014_2023_04-07_15_35_105_130.nc'
file_n   = '../data/fig1/LLJ_frequency_northerly_2014_2023_04-07_15_35_105_130.nc'
shp_file = '../data/common/attachment/bou2_4m/bou2_4l.shp'

ds_all = xr.open_dataset(file_all)
ds_n   = xr.open_dataset(file_n)
gdf    = gpd.read_file(shp_file)

freq_all = ds_all['frequency']
freq_n   = ds_n['frequency']

proj = ccrs.PlateCarree()
fig, axs = uplt.subplots(nrows=2, ncols=2, proj=proj, refwidth=5, share=0)
ax_a, ax_b = axs[0, 0], axs[0, 1]
ax_c, ax_d = axs[1, 0], axs[1, 1]

# (a) Total LLJ frequency
m0 = ax_a.contourf(ds_all['lon'], ds_all['lat'], freq_all, transform=proj)
gdf.plot(ax=ax_a, facecolor='none', edgecolor='k', linewidth=0.4)
ax_a.coastlines(color='black', linewidth=0.4)
ax_a.add_patch(patches.Rectangle((118, 24), 4.5, 4, fill=False, ec='blue', lw=1.2))
ax_a.add_patch(patches.Rectangle((120, 25), 3, 3, fill=False, ec='red', lw=1.2))

# (b) Overview topography
# Elevation data should be downloaded separately and plotted here.
# ds_over = xr.open_dataset('../data/fig1/Fig_A1_overview_elevation.nc')
# ax_b.contourf(ds_over['lon'], ds_over['lat'], ds_over['elevation'], transform=proj)

# (c) Northerly LLJ frequency
m2 = ax_c.contourf(ds_n['lon'], ds_n['lat'], freq_n, transform=proj)
gdf.plot(ax=ax_c, facecolor='none', edgecolor='k', linewidth=0.4)
ax_c.coastlines(color='black', linewidth=0.4)

# (d) Zoomed topography
# Elevation data should be downloaded separately and plotted here.
# ds_zoom = xr.open_dataset('../data/fig1/Fig_A1_zoom_elevation.nc')
# ax_d.contourf(ds_zoom['lon'], ds_zoom['lat'], ds_zoom['elevation'], transform=proj)

for ax in [ax_a, ax_b, ax_c, ax_d]:
    gdf.plot(ax=ax, facecolor='none', edgecolor='k', linewidth=0.4)
    ax.coastlines(color='black', linewidth=0.4)

fig.colorbar(m0, loc='b', label='Frequency (%)')