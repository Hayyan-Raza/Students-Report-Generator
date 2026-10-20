import os
import io
import zipfile
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, send_file
import openpyxl

from grading_engine_processor import DataProcessor
from pdf_reports import StandardReport, AnnualReport

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'assets'),
    static_url_path='/assets',
    template_folder=os.path.join(BASE_DIR, 'templates')
)

def excel_to_raw_data(file_stream):
    wb = openpyxl.load_workbook(file_stream, data_only=True)
    ws = wb.active
    
    raw_data = []
    
    row_iter = ws.iter_rows(values_only=True)
    try:
        first_row = next(row_iter)
    except StopIteration:
        return []
        
    headers = []
    empty_count = 0
    for val in first_row:
        if val is None or str(val).strip() == "":
            if empty_count == 0:
                headers.append("__EMPTY")
            else:
                headers.append(f"__EMPTY_{empty_count}")
            empty_count += 1
        else:
            headers.append(str(val).strip())
            
    for row in row_iter:
        row_dict = {}
        for h, v in zip(headers, row):
            row_dict[h] = v if v is not None else None
        raw_data.append(row_dict)
        
    return raw_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_reports():
    try:
        # 1. Parse form fields
        session_label = request.form.get('session', '2024-2025')
        semester = request.form.get('semester', 'First Semester')
        campus = request.form.get('campus', 'Zaman Town')
        
        # 2. Parse Excel
        excel_file = request.files['excel_file']
        raw_data = excel_to_raw_data(excel_file)
        
        if not raw_data:
            return "Excel file is empty or invalid.", 400
            
        # 3. Process Data
        processor = DataProcessor(raw_data, fallback_grade='')
        if campus:
            processor.config['campus'] = campus
            
        # 4. Generate PDFs in memory
        memory_zip = io.BytesIO()
        
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for cid, student_data in processor.students.items():
                sanitized_name = str(student_data.get('name', 'Unknown')).replace("/", "-")
                safe_grade_level = str(processor.config.get('gradeLevel', '')).strip().upper()
                class_4_to_8_tokens = ['IV', 'V', 'VI', 'VII', 'VIII', '4', '5', '6', '7', '8']
                is_class_4_to_8 = any(
                    safe_grade_level == t or 
                    f"CLASS {t}" in safe_grade_level or 
                    f"GRADE {t}" in safe_grade_level or 
                    safe_grade_level.endswith(f" {t}") 
                    for t in class_4_to_8_tokens
                )
                
                semester_clean = semester.lower()
                is_fourth_term = (
                    'fourth' in semester_clean or 
                    'final' in semester_clean or 
                    'annual' in semester_clean or 
                    '4th' in semester_clean
                )
                
                if is_class_4_to_8 and is_fourth_term:
                    ann_report = AnnualReport(student_data, processor.config, session_label, semester)
                    ann_pdf_stream = io.BytesIO()
                    ann_report.build(ann_pdf_stream)
                    ann_pdf_stream.seek(0)
                    zf.writestr(f"Annual_Report_{cid}_{sanitized_name}.pdf", ann_pdf_stream.read())
                else:
                    std_report = StandardReport(student_data, processor.config, session_label, semester)
                    std_pdf_stream = io.BytesIO()
                    std_report.build(std_pdf_stream)
                    std_pdf_stream.seek(0)
                    zf.writestr(f"Standard_Report_{cid}_{sanitized_name}.pdf", std_pdf_stream.read())
                
        memory_zip.seek(0)
        
        return send_file(
            memory_zip,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"Reports_{processor.config.get('gradeLevel', 'Class')}_{processor.config.get('section', '')}_{semester}.zip"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"An error occurred: {str(e)}", 500

def open_browser():
    webbrowser.open_new('http://127.0.1.1:5000/')

@app.route('/download-template')
def download_template():
    try:
        template_path = os.path.join(BASE_DIR, 'Template_For_Schools_Report_Generation.xlsx')
        return send_file(template_path, as_attachment=True)
    except Exception as e:
        return f"Template file not found: {str(e)}", 404

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(host='127.0.1.1', port=5000, debug=False)
