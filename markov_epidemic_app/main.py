import numpy as np
import pandas as pd
import networkx as nx
from markov_epidemic import *

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Panel, Plot, Range1d, StaticLayoutProvider
from bokeh.models.widgets import TextInput, Slider, Tabs, Div
from bokeh.models.graphs import from_networkx
from bokeh.layouts import layout, WidgetBox
from bokeh.plotting import figure


def extract_numeric_input(s: str) -> int:
    try:
        int(s)
        return int(s)
    except:
        try:
            float(s)
            return float(s)
        except:
            raise Exception('{:s} must be numeric.')


def make_dataset_sir(graph_type,
                     N,
                     d,
                     infection_rate,
                     recovery_rate,
                     T,
                     initial_infected,
                     div_,
                     ):
    """Creates a ColumnDataSource object with data to plot.
    """

    if graph_type == 1:
        G_sir = nx.random_regular_graph(d, N)
        if d == 2:
            graph_type_str = 'Chain'
        elif d >= N-1:
            graph_type_str = 'Complete'
        else:
            graph_type_str = 'Random regular graph'

    elif graph_type == 2:
        G_sir = nx.barabasi_albert_graph(N, d)
        graph_type_str = 'Preferential attachment'

    T = 5.0
    initial_infected = 5

    epidemic = MarkovSIR(infection_rate, recovery_rate, G_sir)
    df_G = nx.to_pandas_edgelist(G_sir)

    epidemic.simulate(T, epidemic.random_seed_nodes(initial_infected))

    df_sim = pd.DataFrame({'transition_times': epidemic.transition_times,
                           'fraction_infected': epidemic.number_of_infected/epidemic.N}).set_index('transition_times')

    params_text = '<b>Network type:</b> {:s}<br>\
    <ul>\
    <li>Inverse spectral radius = {:.0%}</li>\
    <li>Effective diffusion rate = {:.0%}</li>\
    </ul>'.format(graph_type_str, 1/epidemic.spectral_radius, epidemic.effective_diffusion_rate)
    div_.text = params_text

    # Convert dataframe to column data source#
    return ColumnDataSource(df_G), ColumnDataSource(df_sim)


def make_plots_sir(src_sir_G, src_sir_sim):
    """Create a figure object to host the plot.
    """
    ### Graph plot
    plot_sir_G = Plot(plot_width=500,
                      plot_height=550,
                      x_range=Range1d(-1.1,1.1),
                      y_range=Range1d(-1.1,1.1)
                      )

    plot_sir_G.title.text = 'SIR epidemic'
    G_sir = nx.from_pandas_edgelist(pd.DataFrame(src_sir_G.data))
    graph_renderer_sir = from_networkx(G_sir, nx.spring_layout, scale=1, center=(0,0))

    ### Epidemic simulation figure

    # Blank plot with correct labels
    plot_sir_sim = figure(plot_width=800,
                          plot_height=400,
                          title='SIR simulation',
                          x_axis_label='time',
                          y_axis_label='% population infected',
                          )

    # original function
    plot_sir_sim.line('transition_times',
                      'fraction_infected',
                      source = src_sir_sim,
                      color = 'color',
                      line_color = 'blue',
                      )

    plot_sir_sim.legend.click_policy = 'hide'
    plot_sir_sim.legend.location = 'bottom_right'
    return graph_renderer_sir, plot_sir_sim


def update_sir(attr, old, new):
    """Update ColumnDataSource object.
    """
    # Change p to selected value
    graph_type_sir = graph_type_select_sir.value
    N_sir = extract_numeric_input(N_select_sir.value)
    d_sir = extract_numeric_input(d_select_sir.value)
    ir_sir = extract_numeric_input(ir_select_sir.value)
    rr_sir = extract_numeric_input(rr_select_sir.value)
    T_sir = extract_numeric_input(T_select_sir.value)
    initial_infected_sir = extract_numeric_input(initial_infected_select_sir.value)

    # Create new graph
    new_src_sir_G, new_src_sir_sim = make_dataset_sir(graph_type_sir,
                                                      N_sir,
                                                      d_sir,
                                                      ir_sir,
                                                      rr_sir,
                                                      T_sir,
                                                      initial_infected_sir,
                                                      div,
                                                      )

    # Update the data on the plot
    src_sir_G.data.update(new_src_sir_G.data)
    src_sir_sim.data.update(new_src_sir_sim.data)

    G_sir = nx.from_pandas_edgelist(src_sir_G.data)

    node_indices = list(range(N_sir))

    # 1. Update layout
    graph_layout = nx.spring_layout(G_sir)
    # Bokeh demands int keys rather than numpy.int64
    graph_layout = {int(k):v for k, v in graph_layout.items()}
    graph_renderer_sir.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # 2. Then update nodes and edges
    new_data_edge = {'start': src_sir_G.data['source'], 'end': src_sir_G.data['target']};
    new_data_nodes = {'index': node_indices};
    graph_renderer_sir.edge_renderer.data_source.data = new_data_edge;

    graph_renderer_sir.node_renderer.data_source.data = new_data_nodes;


######################################################################
###
### SIR
###
######################################################################
graph_type_select_sir = Slider(start=1,
                               end=2,
                               step=1,
                               title='Network type',
                               value=1,
                               )

N_select_sir = TextInput(value='50', title='Number of nodes')
d_select_sir = TextInput(value='10', title='Network density')
ir_select_sir = TextInput(value='1.0', title='Infection rate')
rr_select_sir = TextInput(value='1.0', title='Recovery rate')
T_select_sir = TextInput(value='5.0', title='Time horizon')
initial_infected_select_sir = TextInput(value='5.0', title='Initial number of infected')

# Update the plot when parameters are changed
graph_type_select_sir.on_change('value', update_sir)
N_select_sir.on_change('value', update_sir)
d_select_sir.on_change('value', update_sir)
ir_select_sir.on_change('value', update_sir)
rr_select_sir.on_change('value', update_sir)
T_select_sir.on_change('value', update_sir)
initial_infected_select_sir.on_change('value', update_sir)

graph_type_sir = extract_numeric_input(graph_type_select_sir.value)
N_sir = extract_numeric_input(N_select_sir.value)
d_sir = extract_numeric_input(d_select_sir.value)
ir_sir = extract_numeric_input(ir_select_sir.value)
rr_sir = extract_numeric_input(rr_select_sir.value)
T_sir = extract_numeric_input(T_select_sir.value)
initial_infected_sir = extract_numeric_input(initial_infected_select_sir.value)

div = Div(text='<b>Parameters:</b><br>', width=300, height=150)

src_sir_G, src_sir_sim = make_dataset_sir(graph_type_sir,
                                          N_sir,
                                          d_sir,
                                          ir_sir,
                                          rr_sir,
                                          T_sir,
                                          initial_infected_sir,
                                          div,
                                          )

controls_sir = WidgetBox(graph_type_select_sir,
                         N_select_sir,
                         d_select_sir,
                         ir_select_sir,
                         rr_select_sir,
                         T_select_sir,
                         initial_infected_select_sir,
                         div,
                         width=300,
                         height=550,
                         )

plot_sir_G = Plot(plot_width=500,
                  plot_height=550,
                  x_range=Range1d(-1.1,1.1),
                  y_range=Range1d(-1.1,1.1)
                  )

graph_renderer_sir, plot_sir_sim = make_plots_sir(src_sir_G, src_sir_sim)

plot_sir_G.renderers.append(graph_renderer_sir)

# Create a row layout
layout_sir = layout(
    [
        [controls_sir, plot_sir_G],
        [plot_sir_sim],
    ],
)

# Make a tab with the layout
tab_sir = Panel(child=layout_sir, title='SIR')

### ALL TABS TOGETHER
tabs = Tabs(tabs=[tab_sir])

curdoc().add_root(tabs)
