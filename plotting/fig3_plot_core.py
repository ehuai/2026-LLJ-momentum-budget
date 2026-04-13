"""Core plotting snippet for Figure 3."""

plan = xr.open_dataset('../data/fig3/planview_diagnostics.nc')
cs   = xr.open_dataset('../data/fig3/cross_section_diagnostics.nc')
diu  = xr.open_dataset('../data/fig3/pressure_hour_diagnostics.nc')

# (a) Plan view
ax.contourf(plan['lon'], plan['lat'], plan['T_anom'], levels=T_levels, cmap=T_cmap)
ax.quiver(plan['lon'][::skip], plan['lat'][::skip],
          plan['u_anom'][::skip, ::skip], plan['v_anom'][::skip, ::skip])

# (b) Cross section
ax2.contourf(cs['distance'], cs['pressure'], cs['wind_speed'], levels=spd_levels, cmap=spd_cmap)
ax2.contour(cs['distance'], cs['pressure'], cs['theta'], colors='k', linewidths=0.8)
ax2.invert_yaxis()

# (c) Diurnal evolution
ax3.contourf(diu['hour'], diu['pressure'], diu['wind_speed'], levels=spd_levels, cmap=spd_cmap)
ax3.contour(diu['hour'], diu['pressure'], diu['theta'], colors='k', linewidths=0.8)
ax3.invert_yaxis()