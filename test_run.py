import json
from grading_engine_processor import DataProcessor
from pdf_reports import StandardReport, AnnualReport

def test_run():
    # 1. Load the sample parsed Excel data
    try:
        with open('parsed_excel.json', 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"Could not load parsed_excel.json: {e}")
        return
        
    print(f"Loaded {len(raw_data)} rows from parsed_excel.json")
    
    # 2. Process data (exactly as in the N8N main script block)
    target_semester = 'First Semester'
    session_label = '2024-2025'
    
    processor = DataProcessor(raw_data, fallback_grade='IV')
    
    print(f"Parsed Config: {processor.config}")
    print(f"Found {len(processor.students)} students.")
    
    # 3. Pick the first student and generate both a standard and annual report
    if not processor.students:
        print("No students parsed.")
        return
        
    first_student_id = list(processor.students.keys())[0]
    student_data = processor.students[first_student_id]
    
    print(f"Generating reports for student: {student_data.get('name')} (CID: {student_data.get('cid')})")
    
    try:
        # Standard Report Test
        std_report = StandardReport(student_data, processor.config, session_label, target_semester)
        std_report.build(f"Test_Standard_Report_{student_data.get('cid')}.pdf")
        
        # Annual Report Test
        ann_report = AnnualReport(student_data, processor.config, session_label, target_semester)
        ann_report.build(f"Test_Annual_Report_{student_data.get('cid')}.pdf")
        
        print("Test generation completed successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        
if __name__ == "__main__":
    test_run()
