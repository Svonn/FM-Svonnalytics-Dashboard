import plotly.graph_objs as go

def calculate_deviations(values):
    average_value = sum(values) / len(values)
    return [value - average_value for value in values]

def create_continuous_color_scale(min_value, max_value):
    if max_value - min_value == 0:
        return [
            (0, 'rgb(247,136,136)'),  # Red
            (1, 'rgb(247,136,136)'),  # Red
        ]

    return [
        # Red, yellow, green
        (0, 'rgb(247,136,136)'),  # Red
        ((min_value - min_value) / (max_value - min_value), 'rgb(247,136,136)'),  # Red
        (0.5, 'rgb(247,247,131)'),  # Yellow
        (1, 'rgb(131,247,136)'),  # Green
        ((max_value - min_value) / (max_value - min_value), 'rgb(131,247,136)'),  # Green
    ]

def create_sorted_bar_chart(x, y, title, xaxis_label, yaxis_label, highlighted_league=None, club_league_mapping=None):

    if highlighted_league == "All":
        highlighted_league = None

    deviations = calculate_deviations(y)
    
    # Sort the bars by y values
    sorted_indices = sorted(range(len(x)), key=lambda i: y[i], reverse=True)
    sorted_x = [x[i] for i in sorted_indices]
    sorted_y = [y[i] for i in sorted_indices]
    sorted_devs = [deviations[i] for i in sorted_indices]
    sorted_leagues = [club_league_mapping.get(club, None) for club in sorted_x] if club_league_mapping else [None] * len(sorted_x)

    # Get min, max for color scaling and setting y-axis range
    min_value = min(sorted_y)
    max_value = max(sorted_y)
    y_axis_min = min_value - (max_value - min_value) * 0.1

    # Create custom continuous color scale
    continuous_color_scale = create_continuous_color_scale(min_value, max_value)

    # Determine bar colors and opacities based on the highlighted league
    bar_colors = []
    bar_opacities = []
    for value, league in zip(sorted_y, sorted_leagues):
        bar_colors.append(value)  # Color set to value for continuous color scale
        if highlighted_league and league != highlighted_league:
            bar_opacities.append(0.2)
        else:
            bar_opacities.append(1)  # Full opacity for all bars

    fig = go.Figure(data=[
        go.Bar(
            x=sorted_x,
            y=sorted_y,
            text=[f"{round(yi, 1)} ({dev:+.1f})" for yi, dev in zip(sorted_y, sorted_devs)],
            textposition='auto',
            marker=dict(
                color=bar_colors,
                opacity=bar_opacities,
                coloraxis="coloraxis",
            )
        )
    ])
    
    if highlighted_league:
        title += f" ({highlighted_league})"
    # Update layout to adjust the y-axis range and apply color scale for non-highlighted bars
    fig.update_layout(
        title=title,
        xaxis=dict(title=xaxis_label),
        yaxis=dict(title=yaxis_label, range=[y_axis_min, max_value + max_value * 0.1]),
        template='plotly_white',
        coloraxis=dict(
            colorscale=continuous_color_scale,
            cmin=min_value,
            cmax=max_value,
            colorbar=dict(title="Score"),
        ),
    )
    
    return fig