import numpy as np
import pickle
import matplotlib as mpl
from lxml import etree

# made from https://sciviscolor.org/media/filer_public/a6/8d/a68d45b2-ad63-436a-94e1-99be4654c3d8/cm_xml_to_matplotlib.py

def load_xml(xml):
    xmldoc = etree.parse(xml)
    data_vals = []
    color_vals = []
    for s in xmldoc.getroot().findall('.//Point'):
        data_vals.append(float(s.attrib['x']))
        color_vals.append((float(s.attrib['r']), float(s.attrib['g']), float(s.attrib['b'])))
    return [color_vals, data_vals]

def make_colormap(position, colors):
    if len(position) != len(colors):
        raise ValueError("position length must match colors")
    cdict = {'red': [], 'green': [], 'blue': []}
    if position[0] != 0:
        cdict['red'].append((0, colors[0][0], colors[0][0]))
        cdict['green'].append((0, colors[0][1], colors[0][1]))
        cdict['blue'].append((0, colors[0][2], colors[0][2]))
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))
    if position[-1] != 1:
        cdict['red'].append((1, colors[-1][0], colors[-1][0]))
        cdict['green'].append((1, colors[-1][1], colors[-1][1]))
        cdict['blue'].append((1, colors[-1][2], colors[-1][2]))
    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 256)
    return cmap

# Load and save
colors, positions = load_xml("fog_colormap.xml")
cmap = make_colormap(positions, colors)

# Save using pickle
with open("fog_colormap.pkl", "wb") as f:
    pickle.dump(cmap, f)