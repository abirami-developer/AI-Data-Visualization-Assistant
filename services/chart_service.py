import plotly.express as px
import pandas as pd


class ChartService:

    @staticmethod
    def generate_chart(df, chart_info):
        """
        Generate a Plotly chart based on the parsed visualization request.

        Parameters
        ----------
        df : pandas.DataFrame
            Uploaded dataset

        chart_info : dict
            Output from ParserService

        Returns
        -------
        plotly.graph_objects.Figure
        """

        chart_type = chart_info.get("chart_type")
        x_axis = chart_info.get("x_axis")
        y_axis = chart_info.get("y_axis")
        aggregation = chart_info.get("aggregation")

        data = df.copy()

        # --------------------------
        # Apply Aggregation
        # --------------------------

        if aggregation and x_axis and y_axis:

            if aggregation == "sum":
                data = (
                    data.groupby(x_axis)[y_axis]
                    .sum()
                    .reset_index()
                )

            elif aggregation in ("mean", "average"):
                data = (
                    data.groupby(x_axis)[y_axis]
                    .mean()
                    .reset_index()
                )

            elif aggregation == "count":
                data = (
                    data.groupby(x_axis)[y_axis]
                    .count()
                    .reset_index()
                )

        # --------------------------
        # Generate Chart
        # --------------------------

        if chart_type == "bar":

            fig = px.bar(
                data,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} by {x_axis}"
            )

        elif chart_type == "line":

            fig = px.line(
                data,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} by {x_axis}"
            )

        elif chart_type == "scatter":

            fig = px.scatter(
                data,
                x=x_axis,
                y=y_axis,
                title=f"{y_axis} vs {x_axis}"
            )

        elif chart_type == "pie":

            fig = px.pie(
                data,
                names=x_axis,
                values=y_axis,
                title=f"{y_axis} by {x_axis}"
            )

        elif chart_type == "histogram":

            fig = px.histogram(
                data,
                x=x_axis,
                title=f"Distribution of {x_axis}"
            )

        else:
            raise ValueError("Unsupported chart type.")

        fig.update_layout(
            template="plotly_white",
            title_x=0.5
        )

        return fig