# Evaluating Climate Model Low Clouds Against Ship Observations

A two-month exploratory research project I designed and carried out under Dr. Chengfei He at the Northeastern Marine Science Center. It checks how well a global climate model (CESM1) represents low clouds and marine fog. Historical ship weather logs are processed into a gridded observational record, and the model output is compared against it.

## Data

- **Observations: EECRA ship reports.** Raw fixed-width synthetic cloud reports from ships, 1952–2008. These are parsed, filtered to ocean reports, and used as the "observed" record.
- **Model: CESM1 Large Ensemble (historical, member 002).** The monthly `CLOUD` variable at the lowest model level (1920–2005) stands in for fog and low cloud.
- **ICOADS 2° Enhanced (NOAA PSL).** Monthly gridded surface cloudiness (`cldc`) from ship reports, used during early exploration.
- **ERA5 reanalysis (ECMWF / Copernicus C3S).** Monthly averaged low cloud cover (`lcc`), 1940–2024, used for seasonal comparison with the model.
- **Study period:** 1955–2004.

Raw data lives in `data/` and is not tracked in git.

## Analysis

- **Parsing:** decoding raw ship log records into clean tables (`00parseEECRA.py`).
- **Gridding:** both datasets are put on a common 5° × 5° grid.
- **Fog probability of occurrence:** fog reports divided by total cloud observations, by season (DJF/MAM/JJA/SON) and in 5-year blocks.
- **Climatology maps:** global and seasonal maps, plus regional views of the North Atlantic and North Pacific.
- **Trends:** per-grid-cell linear regression of fog probability over time.
- **Distributions:** KDE and histogram comparisons between observations and the model.
- **EOF analysis:** detrended, latitude-weighted EOFs to compare dominant modes of variability.

Figures are saved in `dataViz/`.

## Tech Stack

Python, pandas, NumPy, matplotlib, xarray, Cartopy, SciPy, seaborn, and `eofs`, in Jupyter notebooks.

## Disclosure
This research was conducted during my 2025 internship at the Marine Science Center. This research has not been peeer reviewed and includes known discrepencies. This repository is not intended to serve as a proven or accurate source of data, conclusions, or methodology. This repository is intended to serve as a display of code Anika has written.