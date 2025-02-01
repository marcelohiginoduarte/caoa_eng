import openpyxl
from django.http import HttpResponse

def export_to_excel(data, headers, filename='relatorio.xlsx'):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Relatório"

    
    ws.append(headers)

    
    for row in data:
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response