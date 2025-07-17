
from flask import Flask
import pandas as pd
import os

app = Flask('app')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/waterbill')
def display_water_bill():
    try:
        # Read the Excel file
        file_path = 'attached_assets/WaterBill_1752726609979.xlsx'
        
        if not os.path.exists(file_path):
            return '<h1>Error: File not found</h1>'
        
        # Read Excel file - try all sheets
        excel_file = pd.ExcelFile(file_path)
        
        html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Water Bill Data</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .sheet-title { color: #333; margin-top: 30px; }
            </style>
        </head>
        <body>
            <h1>Water Bill Data</h1>
        '''
        
        # Process each sheet in the Excel file
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            html_content += f'<h2 class="sheet-title">Sheet: {sheet_name}</h2>'
            
            if df.empty:
                html_content += '<p>No data found in this sheet.</p>'
            else:
                # Convert DataFrame to HTML table
                table_html = df.to_html(classes='data-table', table_id=f'table-{sheet_name}', escape=False)
                html_content += table_html
        
        html_content += '''
        </body>
        </html>
        '''
        
        return html_content
        
    except Exception as e:
        return f'<h1>Error reading Excel file:</h1><p>{str(e)}</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
