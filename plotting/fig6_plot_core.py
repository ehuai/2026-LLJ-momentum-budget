"""Core plotting snippet for Figure 6."""

ds_sblj = xr.open_dataset('../data/fig6/SBLJ event June Circulation_Fields.nc')
ds_nblj = xr.open_dataset('../data/fig6/NBLJ event April Circulation_Fields.nc')

lon = ds_sblj['lon'].values
lat = ds_sblj['lat'].values
lon2d, lat2d = np.meshgrid(lon, lat)

def plot_panel(ax, ds, hour):
    sel = ds.sel(hour=hour)

    # temperature anomaly shading
    cf = ax.contourf(lon2d, lat2d, sel['T_anom'])

    # geopotential height anomaly
    ax.contour(lon2d, lat2d, sel['Z_anom'], colors='k')

    # 950 / 850 hPa geostrophic wind anomaly
    ax.quiver(lon2d[::4, ::4], lat2d[::4, ::4],
              sel['ug_anom'].values[::4, ::4],
              sel['vg_anom'].values[::4, ::4])

    ax.quiver(lon2d[::4, ::4], lat2d[::4, ::4],
              sel['ug850_anom'].values[::4, ::4],
              sel['vg850_anom'].values[::4, ::4])


    return cf

fig, axs = uplt.subplots(nrows=2, ncols=2, proj='pcarree', share=0)

cf = plot_panel(axs[0, 0], ds_sblj, 15)
cf = plot_panel(axs[0, 1], ds_sblj, 3)
cf = plot_panel(axs[1, 0], ds_nblj, 15)
cf = plot_panel(axs[1, 1], ds_nblj, 3)

fig.colorbar(cf)