"""Core plotting snippet for Figure 2b wind profile."""

# representative event definitions
events = {
    'NBLJ': {'csv': '../data/common/time_str NBLJ event.csv', 'lat': 24.5, 'lon': 119.75},
    'SBLJ': {'csv': '../data/common/time_str SBLJ event.csv', 'lat': 26.5, 'lon': 121.0},
}

for event_name, info in events.items():
    df = pd.read_csv(info['csv'])
    event_time = df['Time_since_1900'].values
    u = ncid.variables['u'][nc_indices, :, lat_idx, lon_idx].filled(np.nan)
    v = ncid.variables['v'][nc_indices, :, lat_idx, lon_idx].filled(np.nan)
    U_ave = np.nanmean(u, axis=0)
    V_ave = np.nanmean(v, axis=0)
    speed = np.sqrt(U_ave**2 + V_ave**2)
    plt.plot(speed, pressure_levels, label=event_name)
