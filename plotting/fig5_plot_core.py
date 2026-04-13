"""Core plotting snippet for Figure 5 momentum budget."""

ds_sblj = xr.open_dataset('../data/fig5/Diurnal_Diagnostics_950hPa_NBLJ_April.nc')
ds_nblj = xr.open_dataset('../data/fig5/Diurnal_Diagnostics_950hPa_SBLJ_June.nc')

# panel (a): diurnal momentum budget
ax.plot(ds_sblj['hour'], ds_sblj['term1_mean'], label='Term I')
ax.plot(ds_sblj['hour'], ds_sblj['term2_mean'], label='Term II')
ax.plot(ds_sblj['hour'], ds_sblj['term3_mean'], label='Term III')
ax.plot(ds_sblj['hour'], ds_sblj['term4_mean'], label='Term IV')
ax.plot(ds_sblj['hour'], ds_sblj['term6_mean'], label='Term VI')

# paired wind-anomaly panel
ax2.plot(ds_sblj['hour'], ds_sblj['wind_total'], color='k')
ax2.plot(ds_sblj['hour'], ds_sblj['wind_geo'],   color='b')
ax2.plot(ds_sblj['hour'], ds_sblj['wind_ageo'],  color='r')
