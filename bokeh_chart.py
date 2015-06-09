from bokeh.plotting import figure
from bokeh.embed import components

def forecast_chart(df, y_fitted, units):

    p = figure(
        title="5-day temp. forecast",
        #plot_width=800,
        plot_height=400,
        tools="pan,wheel_zoom,box_select,reset",
        title_text_font_size="10pt",
        x_axis_type='datetime',
        x_axis_label="date",
        y_axis_label="temp [%s]" % units,
    )

    # format the behaviour of the x axis at diff levels of zoom
    fmt = dict(days=['%d %b'], hours=['%H:%M'])
    p.below[0].formatter.formats = fmt

    p.line(
        df.index, df.temp,
        nonselection_alpha=0.02
    )

    p.line(
        df.index, y_fitted,
        nonselection_alpha=0.02,
        line_color="olive"
    )

    script, div = components(p)

    return script, div
