import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class DashboardGenerator:
    """Generates interactive visualizations and dashboards"""
    
    def recommend_chart(self, x_var, y_var, data):
        """Recommend appropriate chart type based on data types"""
        x_type = data[x_var].dtype
        y_type = data[y_var].dtype if y_var != 'Count' else 'count'
        
        # Time series
        if pd.api.types.is_datetime64_any_dtype(data[x_var]):
            return 'Line Chart'
        
        # Categorical x, numeric y
        if pd.api.types.is_categorical_dtype(data[x_var]) or data[x_var].dtype == 'object':
            if y_var == 'Count':
                return 'Bar Chart'
            else:
                return 'Bar Chart'
        
        # Both numeric
        if pd.api.types.is_numeric_dtype(data[x_var]):
            if y_var == 'Count':
                return 'Histogram'
            elif pd.api.types.is_numeric_dtype(data[y_var]):
                return 'Scatter Plot'
            else:
                return 'Box Plot'
        
        return 'Bar Chart'
    
    def create_chart(self, data, x_var, y_var, chart_type):
        """Create visualization based on selected parameters"""
        try:
            # When y_var is "Count", pre-compute value counts for any chart type
            # This ensures all chart types work with the "Count" option
            if y_var == 'Count':
                # Compute value counts and create a proper dataframe
                count_data = data[x_var].value_counts().reset_index()
                count_data.columns = [x_var, 'count']
                count_label = 'Count'
                
                if chart_type == 'Bar Chart':
                    fig = px.bar(count_data, x=x_var, y='count', 
                                 title=f'Count by {x_var}',
                                 color_discrete_sequence=px.colors.qualitative.Set2)
                
                elif chart_type == 'Line Chart':
                    fig = px.line(count_data, x=x_var, y='count', 
                                  title=f'Count by {x_var}', markers=True)
                
                elif chart_type == 'Scatter Plot':
                    fig = px.scatter(count_data, x=x_var, y='count', 
                                     title=f'Count by {x_var}', opacity=0.6)
                
                elif chart_type == 'Pie Chart':
                    fig = px.pie(count_data, values='count', names=x_var, 
                                 title=f'Distribution of {x_var}')
                
                elif chart_type == 'Histogram':
                    fig = px.histogram(data, x=x_var, title=f'Distribution of {x_var}',
                                       nbins=30, marginal="box")
                
                elif chart_type == 'Box Plot':
                    fig = px.box(data, y=x_var, title=f'Distribution of {x_var}')
                
                else:
                    fig = px.bar(count_data, x=x_var, y='count',
                                 color_discrete_sequence=px.colors.qualitative.Set2)
            
            else:
                # y_var is an actual column name
                if chart_type == 'Bar Chart':
                    fig = px.bar(data, x=x_var, y=y_var, title=f'{y_var} vs {x_var}',
                                 color_discrete_sequence=px.colors.qualitative.Set2)
                
                elif chart_type == 'Line Chart':
                    if pd.api.types.is_datetime64_any_dtype(data[x_var]):
                        fig = px.line(data, x=x_var, y=y_var, title=f'{y_var} over {x_var}',
                                      markers=True)
                    else:
                        # Sort by x for line chart
                        sorted_data = data.sort_values(by=x_var)
                        fig = px.line(sorted_data, x=x_var, y=y_var, title=f'{y_var} vs {x_var}',
                                      markers=True)
                
                elif chart_type == 'Scatter Plot':
                    fig = px.scatter(data, x=x_var, y=y_var, title=f'{y_var} vs {x_var}',
                                     opacity=0.6)
                
                elif chart_type == 'Pie Chart':
                    # Aggregate for pie chart with actual column
                    aggregated = data.groupby(x_var)[y_var].sum().reset_index()
                    fig = px.pie(aggregated, values=y_var, names=x_var, title=f'{y_var} by {x_var}')
                
                elif chart_type == 'Histogram':
                    fig = px.histogram(data, x=x_var, title=f'Distribution of {x_var}',
                                       nbins=30, marginal="box")
                
                elif chart_type == 'Box Plot':
                    fig = px.box(data, x=x_var, y=y_var, title=f'{y_var} by {x_var}')
                
                else:
                    fig = px.bar(data, x=x_var, y=y_var,
                                 color_discrete_sequence=px.colors.qualitative.Set2)
            
            # Update layout for better appearance
            fig.update_layout(
                template='plotly_white',
                height=500,
                showlegend=True,
                title_x=0.5,
                font=dict(size=12)
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
    
    def create_correlation_heatmap(self, data):
        """Create correlation heatmap"""
        numeric_data = data.select_dtypes(include=['number'])
        if len(numeric_data.columns) >= 2:
            corr_matrix = numeric_data.corr()
            fig = px.imshow(corr_matrix, 
                           text_auto=True, 
                           aspect="auto",
                           color_continuous_scale='RdBu_r',
                           title='Correlation Heatmap')
            fig.update_layout(height=600)
            return fig
        return None
