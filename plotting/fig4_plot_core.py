"""Core plotting snippet for Figure 4."""

files = ['../data/fig4/SBLJ_circulation_fields.nc',
         '../data/fig4/NBLJ_circulation_fields.nc']
row_titles = ['SBLJ June', 'NBLJ April']

fig, axs = uplt.subplots(nrows=2, ncols=3, proj=ccrs.PlateCarree(), share=False, span=False)
axs = np.array(axs, dtype=object).reshape(2, 3)

for i, f in enumerate(files):
    ds = xr.open_dataset(f)
    lon, lat = ds['lon'].values, ds['lat'].values
    lon2d, lat2d = np.meshgrid(lon, lat)

    U500, V500, Z500 = ds['U'].sel(level=500), ds['V'].sel(level=500), ds['GeoH'].sel(level=500)
    U850, V850, Z850 = ds['U'].sel(level=850), ds['V'].sel(level=850), ds['GeoH'].sel(level=850)
    U925, V925, Z925 = ds['U'].sel(level=925), ds['V'].sel(level=925), ds['GeoH'].sel(level=925)
    T850, Q925 = ds['T'].sel(temp_level=850), ds['Q'].sel(q_level=925) * 1000
    PW, Spd850, Spd925, Sp = ds['TCWV'], ds['wind_speed'].sel(level=850), ds['wind_speed'].sel(level=925), ds['Sp']

    for lev, Z, U, V in [(500, Z500, U500, V500), (850, Z850, U850, V850), (925, Z925, U925, V925)]:
        mask = Sp / 100 < lev
        Z.values[mask] = np.nan
        U.values[mask] = np.nan
        V.values[mask] = np.nan
    T850.values[Sp / 100 < 850] = np.nan
    Q925.values[Sp / 100 < 925] = np.nan

    # PW + 500 hPa
    ax = axs[i, 0]
    cf1 = ax.contourf(lon2d, lat2d, PW, levels=np.arange(4, 68, 4), extend='both')
    ax.barbs(lon2d[::15, ::15], lat2d[::15, ::15], U500.values[::15, ::15], V500.values[::15, ::15],
             length=5, barbcolor='dimgrey', linewidth=0.6)
    c1 = ax.contour(lon2d, lat2d, Z500, levels=np.arange(5400, 5921, 40), colors='b', linewidths=1.0)
    ax.clabel(c1, c1.levels, fmt='%1.0f', fontsize=10)
    gdf.plot(ax=ax, color='k', linewidth=0.4)
    ax.coastlines(resolution='10m', color='black', linewidth=0.2)
    ax.set_xlim([110, 140]); ax.set_ylim([15, 45])

    # T850 + 850 hPa
    ax = axs[i, 1]
    cf2 = ax.contourf(lon, lat, T850, levels=np.arange(3, 24, 1), extend='both')
    qv2 = ax.quiver(lon2d[::3, ::3], lat2d[::3, ::3], U850.values[::3, ::3], V850.values[::3, ::3],
                    scale=200 if i == 0 else 100, color='dimgrey', width=0.005)
    c2 = ax.contour(lon, lat, Z850, levels=10, colors='b', linewidths=1)
    c3 = ax.contour(lon, lat, Spd850, levels=[10, 14], colors='w', linewidths=1.2)
    ax.clabel(c2, c2.levels, fmt='%1.0f', fontsize=10)
    ax.clabel(c3, c3.levels, fmt='%1.0f', fontsize=10)
    gdf.plot(ax=ax, color='k', linewidth=0.4)
    ax.coastlines(resolution='10m', color='black', linewidth=0.2)
    ax.set_xlim([110, 125]); ax.set_ylim([20, 35])

    # Q925 + 925 hPa
    ax = axs[i, 2]
    cf3 = ax.contourf(lon, lat, Q925, levels=np.arange(3, 19, 1), extend='both')
    qv3 = ax.quiver(lon2d[::3, ::3], lat2d[::3, ::3], U925.values[::3, ::3], V925.values[::3, ::3],
                    scale=200, color='dimgrey', width=0.005)
    c4 = ax.contour(lon, lat, Z925, levels=10, colors='b', linewidths=1)
    c5 = ax.contour(lon, lat, Spd925, levels=[10, 14], colors='w', linewidths=1.2)
    ax.clabel(c4, c4.levels, fmt='%1.0f', fontsize=10)
    ax.clabel(c5, c5.levels, fmt='%1.0f', fontsize=10)
    ax.coastlines(resolution='10m', color='black', linewidth=0.2)
    ax.set_xlim([115, 125]); ax.set_ylim([20, 30])

for j, title in enumerate([r'500-hPa $Z$, $\vec{V}_h$ & $PW$', r'850-hPa $Z$, $\vec{V}_h$ & $T$', r'925-hPa $Z$, $\vec{V}_h$ & $Q$']):
    axs[0, j].set_title(title)
for i, title in enumerate(row_titles):
    axs[i, 0].text(-0.08, 0.5, title, transform=axs[i, 0].transAxes, rotation=90,
                   ha='right', va='center')

fig.colorbar(cf1, ax=axs[:, 0], loc='b', label='TCWV (kg m$^{-2}$)')
fig.colorbar(cf2, ax=axs[:, 1], loc='b', label='Temperature (°C)')
fig.colorbar(cf3, ax=axs[:, 2], loc='b', label='Specific humidity (g kg$^{-1}$)')