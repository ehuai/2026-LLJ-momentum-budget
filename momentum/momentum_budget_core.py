"""
Core momentum-budget workflow used in this study.
"""

def compute_local_tendency(u_minus, u_plus, v_minus, v_plus, dt_seconds, phi):
    """Term I: local tendency by centered time difference."""
    du_dt = (u_plus - u_minus) / (2 * dt_seconds)
    dv_dt = (v_plus - v_minus) / (2 * dt_seconds)
    return du_dt * np.cos(phi) + dv_dt * np.sin(phi)


def compute_horizontal_advection_projection(u, v, lat, lon, plev, phi):
    """Term II: horizontal advection projected onto the jet axis."""
    u_plev = u.sel(pressure=plev, method='nearest')
    v_plev = v.sel(pressure=plev, method='nearest')
    dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)
    dudx, dudy = mpcalc.gradient(u_plev, deltas=(dy, dx))[1], mpcalc.gradient(u_plev, deltas=(dy, dx))[0]
    dvdx, dvdy = mpcalc.gradient(v_plev, deltas=(dy, dx))[1], mpcalc.gradient(v_plev, deltas=(dy, dx))[0]
    adv_u = -(u_plev * dudx + v_plev * dudy)
    adv_v = -(u_plev * dvdx + v_plev * dvdy)
    return adv_u * np.cos(phi) + adv_v * np.sin(phi)


def compute_coriolis_projection(u, v, ug, vg, lat, plev, phi):
    """Term III: Coriolis acting on the ageostrophic wind."""
    u_plev  = u.sel(pressure=plev, method='nearest')
    v_plev  = v.sel(pressure=plev, method='nearest')
    ug_plev = ug.sel(pressure=plev, method='nearest')
    vg_plev = vg.sel(pressure=plev, method='nearest')
    ua = u_plev - ug_plev
    va = v_plev - vg_plev
    f = 2 * 7.2921e-5 * np.sin(np.deg2rad(lat))[:, None]
    cor_u =  f * va
    cor_v = -f * ua
    return cor_u * np.cos(phi) + cor_v * np.sin(phi)


def compute_vertical_advection_projection(w, u, v, plev, phi):
    """Term IV: vertical advection projected onto the jet axis."""
    du_dp = u.differentiate('pressure')
    dv_dp = v.differentiate('pressure')
    w_plev = w.sel(pressure=plev, method='nearest')
    adv_u = -w_plev * du_dp.sel(pressure=plev, method='nearest')
    adv_v = -w_plev * dv_dp.sel(pressure=plev, method='nearest')
    return adv_u * np.cos(phi) + adv_v * np.sin(phi)


def compute_pressure_gradient_force(ug, vg, lat, plev, phi):
    """Term V: pressure-gradient-force term represented through geostrophic wind."""
    ug_plev = ug.sel(pressure=plev, method='nearest')
    vg_plev = vg.sel(pressure=plev, method='nearest')
    f = 2 * 7.2921e-5 * np.sin(np.deg2rad(lat))[:, None]
    pgf_u =  f * vg_plev
    pgf_v = -f * ug_plev
    return pgf_u * np.cos(phi) + pgf_v * np.sin(phi)


def close_budget(term1, term2, term3, term4, term5):
    """Term VI: residual for budget closure."""
    return term1 - term2 - term3 - term4 - term5


def polygon_mean(field2d, lon, lat, polygon):
    lon2d, lat2d = np.meshgrid(lon, lat)
    mask = np.zeros_like(field2d, dtype=bool)
    for j in range(field2d.shape[0]):
        for i in range(field2d.shape[1]):
            mask[j, i] = polygon.contains(Point(lon2d[j, i], lat2d[j, i]))
    return np.nanmean(np.where(mask, field2d, np.nan))


for hour in range(24):
    event_times = filter_event_times(csv_file, month, hour)

    # read composites from preprocessed ERA5 fields
    # u_minus, v_minus : one hour before event times
    # u_now,   v_now   : event time
    # u_plus,  v_plus  : one hour after event times
    # w_now, ug_now, vg_now : corresponding fields at event time
    # lat, lon : coordinate arrays

    # Term I
    # term1 = compute_local_tendency(u_minus, u_plus, v_minus, v_plus, 3600.0, phi)

    # Term II
    # term2 = compute_horizontal_advection_projection(u_now, v_now, lat, lon, plev, phi)

    # Term III
    # term3 = compute_coriolis_projection(u_now, v_now, ug_now, vg_now, lat, plev, phi)

    # Term IV
    # term4 = compute_vertical_advection_projection(w_now, u_now, v_now, plev, phi)

    # Term V
    # term5 = compute_pressure_gradient_force(ug_now, vg_now, lat, plev, phi)

    # Term VI
    # term6 = close_budget(term1, term2, term3, term4, term5)

    # polygon averages for the hourly composite curve
    # mean_I  = polygon_mean(term1.values, lon, lat, poly)
    # mean_II = polygon_mean(term2.values, lon, lat, poly)
    # ...
    pass
