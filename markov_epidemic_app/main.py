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
from bokeh.models import NumeralTickFormatter

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
        density_type = 'Degree'
        if d == 2:
            graph_type_str = 'Chain'
        elif d >= N-1:
            graph_type_str = 'Complete'
        else:
            graph_type_str = 'Random regular graph'
    elif graph_type == 2:
        G_sir = nx.barabasi_albert_graph(N, d)
        density_type = 'Number of attachment for new nodes'
        graph_type_str = 'Preferential attachment'

    epidemic = MarkovSIR(infection_rate, recovery_rate, G_sir)
    df_G = nx.to_pandas_edgelist(G_sir)

    epidemic.simulate(T, epidemic.random_seed_nodes(initial_infected))

    df_sim = pd.DataFrame({
        'transition_times': epidemic.transition_times,
        'fraction_infected': epidemic.number_of_infected/epidemic.N,
        'fraction_recovered': epidemic.number_of_recovered/epidemic.N,
        }).set_index('transition_times')

    params_text = '<b>Network type:</b> {:s}<br>\
    <ul>\
    <li>Effective diffusion rate = {:.0%}</li>\
    <li>Inverse spectral radius = {:.0%}</li>\
    <li>Inverse Cheeger lower bound = {:.0%}</li>\
    <li>Inverse Cheeger upper bound = {:.0%}</li>\
    <li>Density parameter = {:s}</li>\
    </ul>'.format(graph_type_str,
                  epidemic.effective_diffusion_rate,
                  1/epidemic.spectral_radius,
                  1/epidemic.cheeger_lower_bound,
                  1/epidemic.cheeger_upper_bound,
                  density_type,
    )
    div_.text = params_text

    # Convert dataframe to column data source#
    return ColumnDataSource(df_G), ColumnDataSource(df_sim)


def make_dataset_sis(graph_type,
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
        G_sis = nx.random_regular_graph(d, N)
        density_type = 'Degree'
        if d == 2:
            graph_type_str = 'Chain'
        elif d >= N-1:
            graph_type_str = 'Complete'
        else:
            graph_type_str = 'Random regular graph'
    elif graph_type == 2:
        G_sis = nx.barabasi_albert_graph(N, d)
        density_type = 'Number of attachment for new nodes'
        graph_type_str = 'Preferential attachment'

    epidemic = MarkovSIS(infection_rate, recovery_rate, G_sis)
    df_G = nx.to_pandas_edgelist(G_sis)

    epidemic.simulate(T, epidemic.random_seed_nodes(initial_infected))

    df_sim = pd.DataFrame({
        'transition_times': epidemic.transition_times,
        'fraction_infected': epidemic.number_of_infected/epidemic.N,
        'fraction_susceptible': epidemic.number_of_susceptible/epidemic.N,
        }).set_index('transition_times')

    params_text = '<b>Network type:</b> {:s}<br>\
    <ul>\
    <li>Effective diffusion rate = {:.0%}</li>\
    <li>Inverse spectral radius = {:.0%}</li>\
    <li>Lower bound for Inverse Cheeger = {:.0%}</li>\
    <li>Upper bound for Inverse Cheeger = {:.0%}</li>\
    <li>Density parameter = {:s}</li>\
    </ul>'.format(graph_type_str,
                  epidemic.effective_diffusion_rate,
                  1/epidemic.spectral_radius,
                  1/epidemic.cheeger_upper_bound,
                  1/epidemic.cheeger_lower_bound,
                  density_type,
    )
    div_.text = params_text

    # Convert dataframe to column data source#
    return ColumnDataSource(df_G), ColumnDataSource(df_sim)


def make_dataset_seir(graph_type,
                      N,
                      d,
                      exposition_rate,
                      infection_rate,
                      recovery_rate,
                      T,
                      initial_infected,
                      div_,
                      ):
    """Creates a ColumnDataSource object with data to plot.
    """
    if graph_type == 1:
        G_seir = nx.random_regular_graph(d, N)
        density_type = 'Degree'
        if d == 2:
            graph_type_str = 'Chain'
        elif d >= N-1:
            graph_type_str = 'Complete'
        else:
            graph_type_str = 'Random regular graph'
    elif graph_type == 2:
        G_seir = nx.barabasi_albert_graph(N, d)
        density_type = 'Number of attachment for new nodes'
        graph_type_str = 'Preferential attachment'

    epidemic = MarkovSEIR(exposition_rate, infection_rate, recovery_rate, G_seir)
    df_G = nx.to_pandas_edgelist(G_seir)

    epidemic.simulate(T, epidemic.random_seed_nodes(initial_infected))

    df_sim = pd.DataFrame({
        'transition_times': epidemic.transition_times,
        'fraction_infected': epidemic.number_of_infected/epidemic.N,
        'fraction_exposed': epidemic.number_of_exposed/epidemic.N,
        'fraction_recovered': epidemic.number_of_recovered/epidemic.N,
        }).set_index('transition_times')

    params_text = '<b>Network type:</b> {:s}<br>\
    <ul>\
    <li>Effective diffusion rate = {:.0%}</li>\
    <li>Inverse spectral radius = {:.0%}</li>\
    <li>Inverse Cheeger lower bound = {:.0%}</li>\
    <li>Inverse Cheeger upper bound = {:.0%}</li>\
    <li>Density parameter = {:s}</li>\
    </ul>'.format(graph_type_str,
                  epidemic.effective_diffusion_rate,
                  1/epidemic.spectral_radius,
                  1/epidemic.cheeger_lower_bound,
                  1/epidemic.cheeger_upper_bound,
                  density_type,
    )
    div_.text = params_text

    # Convert dataframe to column data source#
    return ColumnDataSource(df_G), ColumnDataSource(df_sim)


def make_plots_sir(src_sir_G, src_sir_sim):
    """Create a figure object to host the plot.
    """
    ### Graph plot
    plot_sir_G = Plot(plot_width=600,
                      plot_height=550,
                      x_range=Range1d(-1.1,1.1),
                      y_range=Range1d(-1.1,1.1)
                      )

    plot_sir_G.title.text = 'SIR epidemic'
    G_sir = nx.from_pandas_edgelist(pd.DataFrame(src_sir_G.data))
    graph_renderer_sir = from_networkx(G_sir, nx.spring_layout, scale=1, center=(0,0))

    ### Epidemic simulation figure

    # Blank plot with correct labels
    plot_sir_sim_infected = figure(plot_width=900,
                                   plot_height=400,
                                   title='Number of infected individuals',
                                   x_axis_label='time',
                                   y_axis_label='% population infected',
                                   )

    plot_sir_sim_recovered = figure(plot_width=900,
                                    plot_height=400,
                                    title='Number of recovered individuals',
                                    x_axis_label='time',
                                    y_axis_label='% population recovered',
                                    )

    # original function
    plot_sir_sim_infected.line('transition_times',
                               'fraction_infected',
                               source=src_sir_sim,
                               color='color',
                               line_color='blue',
                               )

    # original function
    plot_sir_sim_recovered.line('transition_times',
                                'fraction_recovered',
                                source=src_sir_sim,
                                color='color',
                                line_color='blue',
                                )

    # plot_sir_sim_infected.legend.click_policy = 'hide'
    # plot_sir_sim_infected.legend.location = 'bottom_right'
    plot_sir_sim_infected.yaxis.formatter=NumeralTickFormatter(format='0%')

    # plot_sir_sim_recovered.legend.click_policy = 'hide'
    # plot_sir_sim_recovered.legend.location = 'bottom_right'
    plot_sir_sim_recovered.yaxis.formatter=NumeralTickFormatter(format='0%')

    return graph_renderer_sir, plot_sir_sim_infected, plot_sir_sim_recovered


def make_plots_sis(src_sis_G, src_sis_sim):
    """Create a figure object to host the plot.
    """
    ### Graph plot
    plot_sis_G = Plot(plot_width=600,
                      plot_height=550,
                      x_range=Range1d(-1.1,1.1),
                      y_range=Range1d(-1.1,1.1)
                      )

    plot_sis_G.title.text = 'SIS epidemic'
    G_sis = nx.from_pandas_edgelist(pd.DataFrame(src_sis_G.data))
    graph_renderer_sis = from_networkx(G_sis, nx.spring_layout, scale=1, center=(0,0))

    ### Epidemic simulation figure

    # Blank plot with correct labels
    plot_sis_sim_infected = figure(plot_width=900,
                                   plot_height=400,
                                   title='Number of infected individuals',
                                   x_axis_label='time',
                                   y_axis_label='% population infected',
                                   )

    # original function
    plot_sis_sim_infected.line('transition_times',
                               'fraction_infected',
                               source=src_sis_sim,
                               color='color',
                               line_color='blue',
                               )

    # plot_sis_sim_infected.legend.click_policy = 'hide'
    # plot_sis_sim_infected.legend.location = 'bottom_right'
    plot_sis_sim_infected.yaxis.formatter=NumeralTickFormatter(format='0%')

    return graph_renderer_sis, plot_sis_sim_infected


def make_plots_seir(src_seir_G, src_seir_sim):
    """Create a figure object to host the plot.
    """
    ### Graph plot
    plot_seir_G = Plot(plot_width=600,
                       plot_height=550,
                       x_range=Range1d(-1.1,1.1),
                       y_range=Range1d(-1.1,1.1)
                       )

    plot_seir_G.title.text = 'SEIR epidemic'
    G_seir = nx.from_pandas_edgelist(pd.DataFrame(src_seir_G.data))
    graph_renderer_seir = from_networkx(G_seir, nx.spring_layout, scale=1, center=(0,0))

    ### Epidemic simulation figure

    # Blank plot with correct labels
    plot_seir_sim_infected = figure(plot_width=900,
                                    plot_height=400,
                                    title='Number of infected individuals',
                                    x_axis_label='time',
                                    y_axis_label='% population infected',
                                    )

    plot_seir_sim_exposed = figure(plot_width=900,
                                   plot_height=400,
                                   title='Number of exposed individuals',
                                   x_axis_label='time',
                                   y_axis_label='% population exposed',
                                   )

    plot_seir_sim_recovered = figure(plot_width=900,
                                     plot_height=400,
                                     title='Number of recovered individuals',
                                     x_axis_label='time',
                                     y_axis_label='% population recovered',
                                     )

    # original function
    plot_seir_sim_infected.line('transition_times',
                                'fraction_infected',
                                source=src_seir_sim,
                                color='color',
                                line_color='blue',
                                )

    # original function
    plot_seir_sim_exposed.line('transition_times',
                               'fraction_exposed',
                               source=src_seir_sim,
                               color='color',
                               line_color='blue',
                               )

    # original function
    plot_seir_sim_recovered.line('transition_times',
                                 'fraction_recovered',
                                 source=src_seir_sim,
                                 color='color',
                                 line_color='blue',
                                 )

    # plot_seir_sim_infected.legend.click_policy = 'hide'
    # plot_seir_sim_infected.legend.location = 'bottom_right'
    plot_seir_sim_infected.yaxis.formatter=NumeralTickFormatter(format='0%')

    # plot_seir_sim_exposed.legend.click_policy = 'hide'
    # plot_seir_sim_exposed.legend.location = 'bottom_right'
    plot_seir_sim_exposed.yaxis.formatter=NumeralTickFormatter(format='0%')

    # plot_seir_sim_recovered.legend.click_policy = 'hide'
    # plot_seir_sim_recovered.legend.location = 'bottom_right'
    plot_seir_sim_recovered.yaxis.formatter=NumeralTickFormatter(format='0%')

    return graph_renderer_seir, plot_seir_sim_infected, plot_seir_sim_exposed, plot_seir_sim_recovered


def update_sir(attr, old, new):
    """Update ColumnDataSource object.
    """
    # Change parameters to selected values
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
                                                      div_sir,
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


def update_sis(attr, old, new):
    """Update ColumnDataSource object.
    """
    # Change parameters to selected values
    graph_type_sis = graph_type_select_sis.value
    N_sis = extract_numeric_input(N_select_sis.value)
    d_sis = extract_numeric_input(d_select_sis.value)
    ir_sis = extract_numeric_input(ir_select_sis.value)
    rr_sis = extract_numeric_input(rr_select_sis.value)
    T_sis = extract_numeric_input(T_select_sis.value)
    initial_infected_sis = extract_numeric_input(initial_infected_select_sis.value)

    # Create new graph
    new_src_sis_G, new_src_sis_sim = make_dataset_sis(graph_type_sis,
                                                      N_sis,
                                                      d_sis,
                                                      ir_sis,
                                                      rr_sis,
                                                      T_sis,
                                                      initial_infected_sis,
                                                      div_sis,
                                                      )

    # Update the data on the plot
    src_sis_G.data.update(new_src_sis_G.data)
    src_sis_sim.data.update(new_src_sis_sim.data)

    G_sis = nx.from_pandas_edgelist(src_sis_G.data)

    node_indices = list(range(N_sis))

    # 1. Update layout
    graph_layout = nx.spring_layout(G_sis)
    # Bokeh demands int keys rather than numpy.int64
    graph_layout = {int(k):v for k, v in graph_layout.items()}
    graph_renderer_sis.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # 2. Then update nodes and edges
    new_data_edge = {'start': src_sis_G.data['source'], 'end': src_sis_G.data['target']};
    new_data_nodes = {'index': node_indices};
    graph_renderer_sis.edge_renderer.data_source.data = new_data_edge;

    graph_renderer_sis.node_renderer.data_source.data = new_data_nodes;


def update_seir(attr, old, new):
    """Update ColumnDataSource object.
    """
    # Change parameters to selected values
    graph_type_seir = graph_type_select_seir.value
    N_seir = extract_numeric_input(N_select_seir.value)
    d_seir = extract_numeric_input(d_select_seir.value)
    er_seir = extract_numeric_input(er_select_seir.value)
    ir_seir = extract_numeric_input(ir_select_seir.value)
    rr_seir = extract_numeric_input(rr_select_seir.value)
    T_seir = extract_numeric_input(T_select_seir.value)
    initial_infected_seir = extract_numeric_input(initial_infected_select_seir.value)

    # Create new graph
    new_src_seir_G, new_src_seir_sim = make_dataset_seir(graph_type_seir,
                                                         N_seir,
                                                         d_seir,
                                                         er_seir,
                                                         ir_seir,
                                                         rr_seir,
                                                         T_seir,
                                                         initial_infected_seir,
                                                         div_seir,
                                                         )

    # Update the data on the plot
    src_seir_G.data.update(new_src_seir_G.data)
    src_seir_sim.data.update(new_src_seir_sim.data)

    G_seir = nx.from_pandas_edgelist(src_seir_G.data)

    node_indices = list(range(N_seir))

    # 1. Update layout
    graph_layout = nx.spring_layout(G_seir)
    # Bokeh demands int keys rather than numpy.int64
    graph_layout = {int(k):v for k, v in graph_layout.items()}
    graph_renderer_seir.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # 2. Then update nodes and edges
    new_data_edge = {'start': src_seir_G.data['source'], 'end': src_seir_G.data['target']};
    new_data_nodes = {'index': node_indices};
    graph_renderer_seir.edge_renderer.data_source.data = new_data_edge;

    graph_renderer_seir.node_renderer.data_source.data = new_data_nodes;


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
initial_infected_select_sir = TextInput(value='5', title='Initial number of infected')

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

div_sir = Div(text='<b>Network type:</b><br>', width=300, height=150)

src_sir_G, src_sir_sim = make_dataset_sir(graph_type_sir,
                                          N_sir,
                                          d_sir,
                                          ir_sir,
                                          rr_sir,
                                          T_sir,
                                          initial_infected_sir,
                                          div_sir,
                                          )

controls_sir = WidgetBox(graph_type_select_sir,
                         N_select_sir,
                         d_select_sir,
                         ir_select_sir,
                         rr_select_sir,
                         T_select_sir,
                         initial_infected_select_sir,
                         div_sir,
                         width=300,
                         height=550,
                         )

plot_sir_G = Plot(plot_width=600,
                  plot_height=550,
                  x_range=Range1d(-1.1,1.1),
                  y_range=Range1d(-1.1,1.1)
                  )

graph_renderer_sir, plot_sir_sim_infected, plot_sir_sim_recovered = make_plots_sir(src_sir_G, src_sir_sim)

plot_sir_G.renderers.append(graph_renderer_sir)

# Create a row layout
layout_sir = layout(
    [
        [controls_sir, plot_sir_G],
        [plot_sir_sim_infected],
        [plot_sir_sim_recovered],
    ],
)

# Make a tab with the layout
tab_sir = Panel(child=layout_sir, title='SIR')


######################################################################
###
### SIS
###
######################################################################
graph_type_select_sis = Slider(start=1,
                               end=2,
                               step=1,
                               title='Network type',
                               value=1,
                               )

N_select_sis = TextInput(value='50', title='Number of nodes')
d_select_sis = TextInput(value='10', title='Network density')
ir_select_sis = TextInput(value='1.0', title='Infection rate')
rr_select_sis = TextInput(value='1.0', title='Recovery rate')
T_select_sis = TextInput(value='5.0', title='Time horizon')
initial_infected_select_sis = TextInput(value='5', title='Initial number of infected')

# Update the plot when parameters are changed
graph_type_select_sis.on_change('value', update_sis)
N_select_sis.on_change('value', update_sis)
d_select_sis.on_change('value', update_sis)
ir_select_sis.on_change('value', update_sis)
rr_select_sis.on_change('value', update_sis)
T_select_sis.on_change('value', update_sis)
initial_infected_select_sis.on_change('value', update_sis)

graph_type_sis = extract_numeric_input(graph_type_select_sis.value)
N_sis = extract_numeric_input(N_select_sis.value)
d_sis = extract_numeric_input(d_select_sis.value)
ir_sis = extract_numeric_input(ir_select_sis.value)
rr_sis = extract_numeric_input(rr_select_sis.value)
T_sis = extract_numeric_input(T_select_sis.value)
initial_infected_sis = extract_numeric_input(initial_infected_select_sis.value)

div_sis = Div(text='<b>Network type:</b><br>', width=300, height=150)

src_sis_G, src_sis_sim = make_dataset_sis(graph_type_sis,
                                          N_sis,
                                          d_sis,
                                          ir_sis,
                                          rr_sis,
                                          T_sis,
                                          initial_infected_sis,
                                          div_sis,
                                          )

controls_sis = WidgetBox(graph_type_select_sis,
                         N_select_sis,
                         d_select_sis,
                         ir_select_sis,
                         rr_select_sis,
                         T_select_sis,
                         initial_infected_select_sis,
                         div_sis,
                         width=300,
                         height=550,
                         )

plot_sis_G = Plot(plot_width=600,
                  plot_height=550,
                  x_range=Range1d(-1.1,1.1),
                  y_range=Range1d(-1.1,1.1)
                  )

graph_renderer_sis, plot_sis_sim_infected = make_plots_sis(src_sis_G, src_sis_sim)

plot_sis_G.renderers.append(graph_renderer_sis)

# Create a row layout
layout_sis = layout(
    [
        [controls_sis, plot_sis_G],
        [plot_sis_sim_infected],
    ],
)

# Make a tab with the layout
tab_sis = Panel(child=layout_sis, title='SIS')


######################################################################
###
### SEIR
###
######################################################################
graph_type_select_seir = Slider(start=1,
                                end=2,
                                step=1,
                                title='Network type',
                                value=1,
                                )

N_select_seir = TextInput(value='50', title='Number of nodes')
d_select_seir = TextInput(value='10', title='Network density')
er_select_seir = TextInput(value='1.0', title='Exposition rate')
ir_select_seir = TextInput(value='1.0', title='Infection rate')
rr_select_seir = TextInput(value='1.0', title='Recovery rate')
T_select_seir = TextInput(value='5.0', title='Time horizon')
initial_infected_select_seir = TextInput(value='5', title='Initial number of infected')

# Update the plot when parameters are changed
graph_type_select_seir.on_change('value', update_seir)
N_select_seir.on_change('value', update_seir)
d_select_seir.on_change('value', update_seir)
er_select_seir.on_change('value', update_seir)
ir_select_seir.on_change('value', update_seir)
rr_select_seir.on_change('value', update_seir)
T_select_seir.on_change('value', update_seir)
initial_infected_select_seir.on_change('value', update_seir)

graph_type_seir = extract_numeric_input(graph_type_select_seir.value)
N_seir = extract_numeric_input(N_select_seir.value)
d_seir = extract_numeric_input(d_select_seir.value)
er_seir = extract_numeric_input(er_select_seir.value)
ir_seir = extract_numeric_input(ir_select_seir.value)
rr_seir = extract_numeric_input(rr_select_seir.value)
T_seir = extract_numeric_input(T_select_seir.value)
initial_infected_seir = extract_numeric_input(initial_infected_select_seir.value)

div_seir = Div(text='<b>Network type:</b><br>', width=300, height=150)

src_seir_G, src_seir_sim = make_dataset_seir(graph_type_seir,
                                             N_seir,
                                             d_seir,
                                             er_seir,
                                             ir_seir,
                                             rr_seir,
                                             T_seir,
                                             initial_infected_seir,
                                             div_seir,
                                             )

controls_seir = WidgetBox(graph_type_select_seir,
                          N_select_seir,
                          d_select_seir,
                          er_select_seir,
                          ir_select_seir,
                          rr_select_seir,
                          T_select_seir,
                          initial_infected_select_seir,
                          div_seir,
                          width=300,
                          height=550,
                          )

plot_seir_G = Plot(plot_width=600,
                   plot_height=550,
                   x_range=Range1d(-1.1,1.1),
                   y_range=Range1d(-1.1,1.1)
                   )

graph_renderer_seir, plot_seir_sim_infected, plot_seir_sim_exposed, plot_seir_sim_recovered = make_plots_seir(src_seir_G, src_seir_sim)

plot_seir_G.renderers.append(graph_renderer_seir)

# Create a row layout
layout_seir = layout(
    [
        [controls_seir, plot_seir_G],
        [plot_seir_sim_infected],
        [plot_seir_sim_exposed],
        [plot_seir_sim_recovered],
    ],
)

# Make a tab with the layout
tab_seir = Panel(child=layout_seir, title='SEIR')


### ALL TABS TOGETHER
tabs = Tabs(tabs=[tab_sir, tab_sis, tab_seir])

curdoc().add_root(tabs)
