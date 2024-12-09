import pandas as pd
import plotly.express as px
import sys
import os
import json

def analyze_csv(file_path):
    try:
        # Crear la carpeta 'output' si no existe
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Leer el CSV
        data = pd.read_csv(file_path)

        # Resumen de los datos
        summary = {
            "total_rows": len(data),
            "total_columns": len(data.columns),
            "missing_values": data.isnull().sum().to_dict(),
            "duplicates": data.duplicated().sum(),
            "column_types": data.dtypes.apply(lambda x: str(x)).to_dict()
        }

        # Generar gráfico de barras para valores nulos
        fig = px.bar(data.isnull().sum(), labels={'index': 'Columnas', 'value': 'Valores Nulos'}, title="Valores Nulos por Columna")
        bar_chart_path = os.path.join(output_dir, "bar_chart.html")
        fig.write_html(bar_chart_path)

        # Generar gráfico de dispersión (si hay dos columnas numéricas)
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) >= 2:
            fig_scatter = px.scatter(data, x=numeric_columns[0], y=numeric_columns[1], title="Gráfico de Dispersión")
            scatter_chart_path = os.path.join(output_dir, "scatter_chart.html")
            fig_scatter.write_html(scatter_chart_path)

        # Generar diagrama de caja (Boxplot)
        if len(numeric_columns) > 0:
            fig_box = px.box(data, y=numeric_columns[0], title="Diagrama de Caja")
            boxplot_chart_path = os.path.join(output_dir, "boxplot_chart.html")
            fig_box.write_html(boxplot_chart_path)

        # Generar gráfico de líneas (Line chart)
        if len(numeric_columns) > 1:
            fig_line = px.line(data, x=numeric_columns[0], y=numeric_columns[1], title="Gráfico de Líneas")
            line_chart_path = os.path.join(output_dir, "line_chart.html")
            fig_line.write_html(line_chart_path)

        return summary

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Verificar si se ha pasado un argumento (el archivo CSV)
    if len(sys.argv) < 2:
        print("Error: Debes proporcionar el archivo CSV como argumento.")
        sys.exit(0)  # Cambiar de sys.exit(1) a sys.exit(0) para evitar el error de "SystemExit"
    
    file_path = sys.argv[1]  # Obtiene el archivo CSV pasado como argumento
    try:
        result = analyze_csv(file_path)
        print(json.dumps(result, indent=4))  # Mostrar el resultado en formato JSON
    except Exception as e:
        print(f"Error al analizar el archivo: {str(e)}")
