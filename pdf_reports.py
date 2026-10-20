import math
import os
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, landscape, portrait
from reportlab.lib.colors import HexColor
from grading_engine_processor import GradingEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ZAMAN_SVG_PATH = "M61.047096,99.187424 C55.385193,101.476006 50.102268,103.266541 44.231750,101.364403 C37.101784,99.054176 32.724487,93.063026 33.970177,86.873138 C35.141773,81.051407 42.123787,76.482735 48.977570,76.943161 C51.376129,77.104294 53.782764,78.548943 56.453571,76.963470 C56.123451,72.978432 53.655575,69.947350 51.652912,66.819801 C46.255470,58.390625 41.354332,49.690651 36.765728,40.806164 C36.113831,39.543945 34.671200,38.250488 36.064358,36.781696 C37.449806,35.321037 39.169743,35.999706 40.711578,36.694283 C45.109463,38.675465 48.312172,42.033848 51.033333,45.894432 C59.387596,57.746845 66.991631,70.089325 74.153214,82.676453 C76.337715,86.515923 78.239891,86.922531 82.018860,85.385445 C110.406235,73.838867 138.665634,61.966431 167.419342,51.339787 C169.506989,50.568245 171.532990,48.978249 173.908234,50.172058 C175.089203,52.211323 172.648941,53.195969 172.807861,54.850716 C173.055176,56.203831 175.284821,56.047119 175.047745,58.081066 C171.351395,59.656166 168.890549,57.920071 166.732971,54.492550 C137.527618,66.201965 108.413246,77.874893 79.645805,89.408737 C79.774300,92.754814 81.441208,94.128288 82.298561,95.894348 C82.875740,97.083275 82.822586,98.272087 81.770058,99.053993 C80.556442,99.955559 79.657417,99.055199 78.785561,98.188187 C76.942238,96.355141 76.136269,93.024872 72.710197,93.485596 C71.783615,94.552773 72.242073,95.273949 72.679367,95.994606 C73.372162,97.136360 74.340118,98.376129 73.030884,99.564812 C71.680069,100.791237 70.482864,99.681114 69.582367,98.755928 C66.704346,95.799019 64.088562,97.843781 61.047096,99.187424 M62.738857,86.611084 C58.730099,81.565628 50.682667,78.888977 44.917183,80.683434 C38.472897,82.689178 36.070572,89.345169 39.928898,94.504227 C42.681454,98.184731 49.887859,99.503700 54.292389,97.081406 C54.698093,94.867653 51.184147,91.970062 55.311657,90.310875 C58.068748,89.202568 60.794468,91.585938 63.474380,90.550995 C64.411964,89.180359 63.495323,88.236076 62.738857,86.611084 M41.755524,42.626091 C42.506470,44.280270 43.131348,46.006493 44.028839,47.576920 C49.805195,57.684357 55.833302,67.653946 61.363495,77.893082 C63.588741,82.013123 66.819115,84.239334 70.963203,86.065796 C71.210381,83.776024 70.096519,82.257401 69.162590,80.769142 C62.885574,70.766479 56.616817,60.756741 50.169590,50.863861 C48.024677,47.572632 46.061028,43.953445 41.755524,42.626091 z"
OTHER_SVG_PATH = "M143.1 12.5c13.9 1.7 21.6 10.2 28 21.5a176 176 0 0 1 14.7 36.2c3.2 10.5-.4 19.5-6.5 27.4-9.2 11.6-20 13-33.9 5.6-1.5 1.4-1.7 3.4-2 5.3-1.5 10.1-7.8 13.6-17.5 7.9.2 12.5-2 24.6-8.3 35.4A86 86 0 0 1 98 175.4a35 35 0 0 1-29.2 6.7A68 68 0 0 1 32.5 165a61 61 0 0 1-16.7-28.8c-2.5-9-6-17.9-6.5-27.3-.6-11.6 0-22.5 7.4-32.8a53 53 0 0 1 33.4-21.4 49 49 0 0 1 45.6 11.6 65 65 0 0 1 12.7 19.9q1.4 3.2 2.2 6.2c1.7 1.1 2.5-.2 3.5-.4 5-1.4 8.8.5 10 5.5q1 4.7 4.2 8.3c1 1 1.4 2.9 3.2 2.7 2.2-.3 2-2.5 2.6-4q1.5-4.6 3.3-9.3c2.2-5.6 7.5-6.5 11.6-2 8.4 9.6 17.2 8 24-3 6.3-10.2 3.3-19.8 0-29.4a97 97 0 0 0-15-30.6c-3.8-4.7-8-8.8-14.4-9.8-10.8-1.6-17.3 6-20 13.7a37 37 0 0 0 0 26.8q1.1 2.2-.5 3.6c-1.5 1.5-2.6.1-3.8-.8-6.6-5.2-7-13-7.5-20.3A31 31 0 0 1 122 17.3c5.8-5.1 13.1-6 21-4.8M39.4 69c-2 1.7-3.9 3.7-6.1 5-12 7.5-14.5 19.3-13.7 31.9.9 12.3 3.5 24.5 8.8 36a52 52 0 0 0 41.9 31.6c4.6.5 9.6 1.6 13.8-.6 7.7-3.9 13.9-10 19.4-16.7a59 59 0 0 0 13-43.7c-.2-3.9-.4-8.1-3.8-12.8 1.5 11.8 2.2 22.3-2.4 32.2-3.6 7.6-7.8 15-14.4 20.4-2.6 2.3-5.5 4.8-9.4 5.2-9.2 1-17.5-1.5-25.2-6.1A24 24 0 0 1 51 140a46 46 0 0 1 .8-38.1c1.7-3.5 5-4.7 8.2-2.5 3.3 2.2 3.3 6.4 5 9.7.6 1.3-1.2 2-2.7 2.1q-2.5 0-3 2.6c-1.4 8.3-1.6 16.7 3 24 5.7 9.5 14.7 14.4 25 8.2 10.2-6 14.1-16.6 16.1-27.4 1.8-9.8-.3-19.7-4.2-28.7A52 52 0 0 0 86 69.8C74 59.6 54 59.5 39.4 68.9M237.2 20.2q4.8-4.3 9.4-7.9c3-2.2 7-3 9.7-.3 2.4 2.4 3 6.3 1.3 9.7-1.4 2.7-1.6 5.7-2.7 8.5-.8 2.3-1.8 5-5 4.9-3-.2-4-2.5-4.4-5.2q-.1-.9-.5-2c-4.6 2.8-8 6.7-12.8 8.9-5.2 2.4-5.9 8.1-7.7 12.8-2.3 6.2-5.1 11.2-13 10.8-2.4-.1-3 2.1-3.2 4.2-.3 3-1.7 5.4-4.7 5.5-3 .2-5.6-1.4-6-4.8-.6-5.9-5.8-7.3-9.5-10-7.2-5.5-9.3-16.3-4.4-22.5 4-5 10.6-4.5 13.8 1q1.6 2.8 3 5.7.8 2.3 3 2.1c4.7-.7 7 1.6 8 6 .1.5.8.9 1.2 1.4 2.5-1.2 2.6-3.5 3-5.5q2.2-10.1 11.2-15 5.7-3.1 10.3-8.3M201.2 113.3a73 73 0 0 1 25.5-19.8q3.3-1.4 7-2.2 4.5-1.4 6.2 2.4c1.3 3-1.4 4.1-3.4 5.1-10.9 5.4-18.5 14.6-27 22.7-2.4 2.2-4 5.2-6 7.8-2.3 2.7-5.6 4-8.4 2.1-2.6-1.7-4.4-5-2.2-8.5 2.3-3.6 4.7-7 8.3-9.6M258.7 99c-3 .7-5-.3-7-1.6-3.2-2-3.8-4.4-.7-7q3.1-2.9 6.4-5.4c2.2-1.6 7 .4 6.3 2.7-1.2 3.8.2 9-5 11.3"


class TopDownCanvas:
    def __init__(self, c, page_height):
        self.c = c
        self.page_height = page_height
        self.current_font_size = 10
        
    def _y(self, y):
        return self.page_height - y
        
    def rect(self, x, y, width, height, stroke=1, fill=0):
        # PDFKit rect(x, y, w, h) draws down from y. 
        # ReportLab rect(x, y, w, h) draws up from y.
        # So we anchor at self._y(y) - height
        self.c.rect(x, self._y(y) - height, width, height, stroke=stroke, fill=fill)
        
    def line(self, x1, y1, x2, y2):
        self.c.line(x1, self._y(y1), x2, self._y(y2))
        
    def drawString(self, x, y, text):
        # PDFKit text(x, y) anchors at the top-left of the text.
        # ReportLab anchors at the bottom-left (baseline).
        baseline_y = self._y(y) - (self.current_font_size * 0.8)
        self.c.drawString(x, baseline_y, str(text))
        
    def setFont(self, font, size):
        self.current_font_size = size
        self.c.setFont(font, size)
        
    def setLineWidth(self, w):
        self.c.setLineWidth(w)
        
    def setStrokeColor(self, color):
        self.c.setStrokeColor(color)
        
    def setFillColor(self, color):
        self.c.setFillColor(color)
        
    def stringWidth(self, text, font, size):
        return self.c.stringWidth(str(text), font, size)
        
    def drawImage(self, image, x, y, width, height, preserveAspectRatio=True, mask='auto'):
        self.c.drawImage(image, x, self._y(y) - height, width=width, height=height, preserveAspectRatio=preserveAspectRatio, mask=mask)
        
    def save(self):
        self.c.save()
        
    def showPage(self):
        self.c.showPage()
        
    def drawStar(self, cx, cy, spikes, outer_radius, inner_radius):
        rot = math.pi / 2 * 3
        step = math.pi / spikes
        
        path = self.c.beginPath()
        path.moveTo(cx, self._y(cy - outer_radius))
        
        for i in range(spikes):
            x = cx + math.cos(rot) * outer_radius
            y = cy + math.sin(rot) * outer_radius
            path.lineTo(x, self._y(y))
            rot += step
            
            x = cx + math.cos(rot) * inner_radius
            y = cy + math.sin(rot) * inner_radius
            path.lineTo(x, self._y(y))
            rot += step
            
        path.lineTo(cx, self._y(cy - outer_radius))
        self.c.drawPath(path, stroke=1, fill=0)


class BasePdfReport:
    def __init__(self, student, config, session_label, target_semester):
        self.student = student
        self.config = config
        self.session_label = session_label
        self.target_semester = target_semester
        
        def find_matching_term(target, possible_terms):
            if not possible_terms: return target
            clean = lambda t: "".join(c for c in str(t).lower() if c.isalnum())
            target_clean = clean(target)
            
            for t in possible_terms:
                if clean(t) == target_clean: return t
                
            if any(kw in target_clean for kw in ['fourth', 'annual', 'final', '4th']):
                for t in possible_terms:
                    tc = clean(t)
                    if any(kw in tc for kw in ['annual', 'fourth', 'final', '4th']): return t
                    
            prefixes = ['first', 'second', 'third', 'fourth', '1st', '2nd', '3rd', '4th']
            for prefix in prefixes:
                if prefix in target_clean:
                    for t in possible_terms:
                        if prefix in clean(t): return t
                        
            for t in possible_terms:
                tc = clean(t)
                if tc in target_clean or target_clean in tc: return t
            return target
            
        if self.student.get("terms"):
            matched_term = find_matching_term(self.target_semester, list(self.student["terms"].keys()))
            if matched_term in self.student["terms"]:
                self.term_data = self.student["terms"][matched_term]
            else:
                self.term_data = list(self.student["terms"].values())[-1]
        else:
            self.term_data = {}

        self.LAYOUT = {
            "margin": 50,
            "leftX": 50,
            "rightEdge": 0,
            "tableWidth": 0
        }

    @property
    def is_booklet(self):
        return False

    def draw_grid_row(self, c, y_pos, cols, col_widths, is_bold=False, is_header=False, center_first_col=False):
        left_x = self.LAYOUT["leftX"]
        table_width = self.LAYOUT["tableWidth"]
        is_booklet = self.is_booklet
        
        if is_booklet:
            row_height = 35 if is_header else 25
            font_size = 8
        else:
            row_height = 28 if is_header else 19
            font_size = 10

        c.setLineWidth(1)
        if is_header:
            c.setFillColor(HexColor('#f4f4f4'))
            c.setStrokeColor(HexColor('#000000'))
            c.rect(left_x, y_pos, table_width, row_height, fill=1, stroke=1)
        else:
            c.setStrokeColor(HexColor('#000000'))
            c.rect(left_x, y_pos, table_width, row_height, fill=0, stroke=1)
            
        c.setFillColor(HexColor('#000000'))

        current_x = left_x
        for i, text in enumerate(cols):
            if i > 0:
                c.line(current_x, y_pos, current_x, y_pos + row_height)
            
            c.setFont('Helvetica-Bold' if is_bold else 'Helvetica', font_size)
            
            is_eval_header = is_header and i == 0 and str(text).strip() == 'Evaluation'
            align = 'left' if (i == 0 and not is_eval_header and not center_first_col) else 'center'

            cell_width = col_widths[i]
            text_str = str(text)
            text_width = c.stringWidth(text_str, 'Helvetica-Bold' if is_bold else 'Helvetica', font_size)
            
            if align == 'center':
                text_x = current_x + (cell_width - text_width) / 2
            else:
                text_x = current_x + (5 if not is_booklet else 3)
                
            # EXACT JS LOGIC FOR TEXT Y ALIGNMENT
            text_y = y_pos + (8 if is_booklet else (8 if is_header else 4))
            
            if "\n" in text_str:
                lines = text_str.split("\n")
                line_y = text_y - 2
                for line in lines:
                    line_w = c.stringWidth(line, 'Helvetica-Bold' if is_bold else 'Helvetica', font_size)
                    line_x = current_x + (cell_width - line_w) / 2 if align == 'center' else text_x
                    c.drawString(line_x, line_y, line)
                    line_y += font_size + 2
            else:
                c.drawString(text_x, text_y, text_str)

            current_x += cell_width

        return row_height

    def draw_signatures(self, c, y_pos, label1, label2, label3=None):
        left_x = self.LAYOUT["leftX"]
        is_booklet = self.is_booklet
        
        sig_width = 139
        padding = 45
        font_size = 9

        if is_booklet and label3:
            sig_width = 110
            padding = 35
            font_size = 8.5

        sig1_start = left_x + padding
        sig2_start = left_x + self.LAYOUT["tableWidth"] - padding - sig_width
        sig3_start = left_x + (self.LAYOUT["tableWidth"] / 2) - (sig_width / 2)

        c.setStrokeColor(HexColor('#000000'))
        c.setFillColor(HexColor('#000000'))
        c.setFont("Helvetica", font_size)

        c.line(sig1_start, y_pos, sig1_start + sig_width, y_pos)
        c.drawString(sig1_start + (sig_width - c.stringWidth(label1, "Helvetica", font_size))/2, y_pos + 8, label1)

        def draw_sig(label, x_start):
            if label and ("Principal" in label or "Incharge" in label):
                campus = self.config.get("campus", "Other")
                if campus == "Zaman Town":
                    svg_str = f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><path d="{ZAMAN_SVG_PATH}" fill="black" /></svg>'
                    scale = 0.60 if not is_booklet else (0.35 if label3 else 0.26)
                    y_offset = -35 if not is_booklet else -25
                    x_offset = 25 if not is_booklet else 10
                else:
                    svg_str = f'<svg viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg"><path d="{OTHER_SVG_PATH}" fill="black" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" /></svg>'
                    scale = 0.40 if not is_booklet else (0.24 if label3 else 0.15)
                    y_offset = -30 if not is_booklet else -25
                    x_offset = 20 if not is_booklet else 5
                
                try:
                    drawing = svg2rlg(io.StringIO(svg_str))
                    drawing.scale(scale, scale)
                    # Coordinates for renderPDF.draw need to be in standard ReportLab space (bottom-up)
                    raw_y = c._y(y_pos) + y_offset # actually SVG draws upwards, so we position above the line
                    renderPDF.draw(drawing, c.c, x_start + x_offset, raw_y)
                except Exception as e:
                    print(f"Failed to draw signature: {e}")

        if label3:
            draw_sig(label3, sig3_start)
            c.line(sig3_start, y_pos, sig3_start + sig_width, y_pos)
            c.drawString(sig3_start + (sig_width - c.stringWidth(label3, "Helvetica", font_size))/2, y_pos + 8, label3)

        draw_sig(label2, sig2_start)
        c.line(sig2_start, y_pos, sig2_start + sig_width, y_pos)
        c.drawString(sig2_start + (sig_width - c.stringWidth(label2, "Helvetica", font_size))/2, y_pos + 8, label2)


class StandardReport(BasePdfReport):
    @property
    def is_booklet(self):
        return False

    def build(self, output_filename):
        page_width, page_height = landscape(A4) 
        
        raw_c = canvas.Canvas(output_filename, pagesize=(page_width, page_height))
        c = TopDownCanvas(raw_c, page_height)

        content_width = 600
        self.LAYOUT["margin"] = 50
        self.LAYOUT["leftX"] = (page_width - content_width) / 2
        self.LAYOUT["rightEdge"] = self.LAYOUT["leftX"] + content_width
        self.LAYOUT["tableWidth"] = content_width

        current_y = 120 

        c.setFont("Helvetica-Bold", 16)
        title = f"{self.target_semester.upper()} AGGREGATE"
        title_w = c.stringWidth(title, "Helvetica-Bold", 16)
        c.drawString((page_width - title_w) / 2, current_y, title)
        current_y += 15
        
        c.setFont("Helvetica", 10)
        session_str = f"SESSION {self.session_label}"
        sess_w = c.stringWidth(session_str, "Helvetica", 10)
        c.drawString((page_width - sess_w) / 2, current_y, session_str)
        current_y += 35 

        c.setFont('Helvetica-Bold', 11)
        base_x = self.LAYOUT["leftX"]
        spacing = 18 
        
        c.drawString(base_x, current_y, "Student's Name:")
        c.setFont('Helvetica', 11)
        c.drawString(base_x + 95, current_y, str(self.student.get("name", "-")))
        current_y += spacing

        c.setFont('Helvetica-Bold', 11)
        c.drawString(base_x, current_y, "Father's Name:")
        c.setFont('Helvetica', 11)
        c.drawString(base_x + 95, current_y, str(self.student.get("fatherName", "-")))
        current_y += spacing

        c.setFont('Helvetica-Bold', 11)
        c.drawString(base_x, current_y, "Grade:")
        c.setFont('Helvetica', 11)
        c.drawString(base_x + 45, current_y, str(self.config.get("gradeLevel", "-")))
        
        # Center Section
        section_val = str(self.config.get("section", "-"))
        sec_lbl_w = c.stringWidth("Section: ", 'Helvetica-Bold', 11)
        sec_val_w = c.stringWidth(section_val, 'Helvetica', 11)
        sec_total_w = sec_lbl_w + 30 + sec_val_w
        sec_start_x = base_x + (self.LAYOUT["tableWidth"] - sec_total_w) / 2
        
        c.setFont('Helvetica-Bold', 11)
        c.drawString(sec_start_x, current_y, "Section: ")
        c.setFont('Helvetica', 11)
        c.drawString(sec_start_x + sec_lbl_w + 30, current_y, section_val)

        # Right aligned CID
        cid_val = str(self.student.get("cid", "-"))
        cid_lbl_w = c.stringWidth("CID No: ", 'Helvetica-Bold', 11)
        cid_val_w = c.stringWidth(cid_val, 'Helvetica', 11)
        cid_total_w = cid_lbl_w + 30 + cid_val_w
        cid_start_x = base_x + self.LAYOUT["tableWidth"] - cid_total_w

        c.setFont('Helvetica-Bold', 11)
        c.drawString(cid_start_x, current_y, "CID No: ")
        c.setFont('Helvetica', 11)
        c.drawString(cid_start_x + cid_lbl_w + 30, current_y, cid_val)
        
        current_y += spacing + 10

        base_col_widths = [139, 80, 80, 80, 80]
        scale_val = self.LAYOUT["tableWidth"] / 459
        col_widths = [w * scale_val for w in base_col_widths]
        sum_except_last = sum(col_widths[:-1])
        col_widths[-1] = self.LAYOUT["tableWidth"] - sum_except_last
        
        h = self.draw_grid_row(c, current_y, ['Subjects', 'Max\nMarks', 'Obtained\nMarks', 'Per %', 'Grade'], col_widths, is_bold=True, is_header=True, center_first_col=True)
        current_y += h

        safe_grade_level = str(self.config.get("gradeLevel", "")).strip().upper()
        class_4_to_8_tokens = ['IV', 'V', 'VI', 'VII', 'VIII', '4', '5', '6', '7', '8']
        is_class_4_to_8 = any(safe_grade_level == t or f"CLASS {t}" in safe_grade_level or f"GRADE {t}" in safe_grade_level or safe_grade_level.endswith(f" {t}") for t in class_4_to_8_tokens)

        grand_total = 0
        total_max_marks = 800
        has_failed = False
        has_absent_4_to_8 = False

        for key, subject_name in self.config.get("subjectMap", {}).items():
            if "project" in subject_name.lower():
                continue

            subject_val = self.term_data.get(key, "-")

            if "drawing" in subject_name.lower():
                h = self.draw_grid_row(c, current_y, [subject_name, '-', subject_val, '-', subject_val], col_widths, center_first_col=True)
                current_y += h
            else:
                subject_total_display = subject_val
                subject_percent_display = "-"
                grade = "-"
                
                is_exempt = isinstance(subject_val, str) and subject_val.upper() in ("EXEMPT", "EXCUSED")
                is_absent = isinstance(subject_val, str) and subject_val.upper() == "ABSENT"

                if is_class_4_to_8 and is_exempt:
                    subject_total_display = "EXCUSED"
                    subject_percent_display = "EXCUSED"
                    grade = "EXCUSED"
                    total_max_marks -= 100
                    h = self.draw_grid_row(c, current_y, [subject_name, '0', subject_total_display, subject_percent_display, grade], col_widths, center_first_col=True)
                    current_y += h
                elif is_class_4_to_8 and is_absent:
                    subject_total_display = "ABSENT"
                    subject_percent_display = "ABSENT"
                    grade = "ABSENT"
                    has_absent_4_to_8 = True
                    has_failed = True
                    h = self.draw_grid_row(c, current_y, [subject_name, '100', subject_total_display, subject_percent_display, grade], col_widths, center_first_col=True)
                    current_y += h
                elif is_exempt:
                    subject_total_display = "EXEMPT"
                    subject_percent_display = "100%"
                    grade = "A*"
                    grand_total += 100
                    h = self.draw_grid_row(c, current_y, [subject_name, '100', subject_total_display, subject_percent_display, grade], col_widths, center_first_col=True)
                    current_y += h
                else:
                    score = 0 if subject_val in ("ABSENT", "-") else float(subject_val) if str(subject_val).replace('.', '', 1).isdigit() else 0
                    subject_total_display = subject_val
                    subject_percent_display = f"{GradingEngine.custom_round(score)}%"
                    grade = GradingEngine.calculate_grade(score)
                    grand_total += score

                    if grade == 'U':
                        has_failed = True
                    h = self.draw_grid_row(c, current_y, [subject_name, '100', subject_total_display, subject_percent_display, grade], col_widths, center_first_col=True)
                    current_y += h

        raw_overall_percent = (grand_total / total_max_marks * 100) if total_max_marks > 0 else 0
        overall_percent = GradingEngine.custom_round(raw_overall_percent)
        overall_grade = GradingEngine.calculate_grade(raw_overall_percent)

        if has_failed:
            overall_grade = 'U'

        display_overall_percent = "-" if has_failed else f"{overall_percent}%"
        display_overall_grade = "-" if has_failed else overall_grade

        if is_class_4_to_8 and has_absent_4_to_8:
            display_overall_percent = "ABSENT"
            display_overall_grade = "ABSENT"

        h = self.draw_grid_row(c, current_y, ['Total', str(total_max_marks), str(GradingEngine.custom_round(grand_total)), display_overall_percent, display_overall_grade], col_widths, is_bold=True, center_first_col=True)
        current_y += h + 15

        att_days = self.term_data.get("attendedDays") or self.student.get("attendedDays")
        term_total_days = self.term_data.get("totalWorkingDays") or self.config.get("totalWorkingDays")
        att_metrics = GradingEngine.get_attendance_metrics(att_days, term_total_days)
        att_days_str = str(att_days) if att_days is not None else "-"
        total_days_str = str(term_total_days) if term_total_days else "-"
        combined_attendance = f"{att_metrics['attendanceStr']} ({att_days_str}/{total_days_str})"
        
        left_x = self.LAYOUT["leftX"]
        right_edge = self.LAYOUT["rightEdge"]
        right_col_start_x = right_edge - 210

        # Line 1: Overall Percentage & Grade
        c.setFont("Helvetica-Bold", 10)
        c.drawString(left_x, current_y, "Overall Percentage:")
        c.setFont("Helvetica", 10)
        c.drawString(left_x + 130, current_y, display_overall_percent)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(right_col_start_x, current_y, "Overall Grade:")
        c.setFont("Helvetica", 10)
        c.drawString(right_col_start_x + 95, current_y, display_overall_grade)
        
        current_y += 18
        
        # Line 2: Attendance & Remarks
        c.setFont("Helvetica-Bold", 10)
        c.drawString(left_x, current_y, "Attendance:")
        c.setFont("Helvetica", 10)
        c.drawString(left_x + 130, current_y, combined_attendance)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(right_col_start_x, current_y, "Attendance Remarks:")
        c.setFont("Helvetica", 10)
        c.drawString(right_col_start_x + 120, current_y, att_metrics['attendanceRemarkStr'])
        
        current_y += 18
        
        # Line 3: Class Teacher's Remarks
        c.setFont("Helvetica-Bold", 10)
        c.drawString(left_x, current_y, "Class Teacher's Remarks:")
        teacher_remarks = GradingEngine.get_teacher_remarks(overall_grade)
        c.setFont("Helvetica", 10)
        
        import textwrap
        lines = textwrap.wrap(teacher_remarks, width=80)
        for line in lines:
            c.drawString(left_x + 140, current_y, line)
            current_y += 14
        
        current_y += 60
        self.draw_signatures(c, current_y, "Class Teacher's Signature", "Incharge's Signature", "Principal's Signature")

        c.save()


class AnnualReport(BasePdfReport):
    @property
    def is_booklet(self):
        return True

    def set_page_side(self, side):
        W = 445
        fold_line_x = 576 

        if side == 'left':
            self.LAYOUT["leftX"] = (fold_line_x - W) / 2
            self.LAYOUT["rightEdge"] = self.LAYOUT["leftX"] + W
            self.LAYOUT["tableWidth"] = W
        else:
            self.LAYOUT["leftX"] = fold_line_x + (fold_line_x - W) / 2
            self.LAYOUT["rightEdge"] = self.LAYOUT["leftX"] + W
            self.LAYOUT["tableWidth"] = W

    def build(self, output_filename):
        page_width, page_height = landscape(A3)
        raw_c = canvas.Canvas(output_filename, pagesize=(page_width, page_height))
        c = TopDownCanvas(raw_c, page_height)
        
        # SHEET 1
        self.set_page_side('left')
        c.setFont("Helvetica-Bold", 18)
        title = "GRADING CRITERIA"
        title_w = c.stringWidth(title, "Helvetica-Bold", 18)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - title_w) / 2, 218, title)
        
        c.setFont("Helvetica", 12)
        sess_str = f"SESSION {self.session_label}"
        sess_w = c.stringWidth(sess_str, "Helvetica", 12)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - sess_w) / 2, 218 + 20, sess_str)

        criteria = [
            {'g': 'A*', 'r': '94.56% - 100%'}, {'g': 'A-1', 'r': '89.56% - 94.55%'},
            {'g': 'A', 'r': '79.56% - 89.55%'}, {'g': 'B', 'r': '69.56% - 79.55%'},
            {'g': 'C', 'r': '59.56% - 69.55%'}, {'g': 'D', 'r': '49.56% - 59.55%'},
            {'g': 'E', 'r': '39.56% - 49.55%'}, {'g': 'U', 'r': 'Below 39.56%'}
        ]

        row_y = 218 + 80
        for index, item in enumerate(criteria):
            col_x = self.LAYOUT["leftX"] + 60 if index % 2 == 0 else self.LAYOUT["leftX"] + 300
            center_y = row_y
            
            c.setLineWidth(1.5)
            c.setStrokeColor(HexColor('#000000'))
            # Increased star size slightly
            c.drawStar(col_x, center_y - 2, 5, 23, 11)
            
            c.setFont("Helvetica-Bold", 10)
            g_w = c.stringWidth(item['g'], "Helvetica-Bold", 10)
            # Adjusted vertical offset for text to center it inside the star
            c.drawString(col_x - (g_w)/2, center_y - 5, item['g'])
            
            c.setFont("Helvetica", 11)
            c.drawString(col_x + 30, center_y, item['r'])
            
            if index % 2 != 0:
                row_y += 80

        # Right Side (Cover Profile)
        self.set_page_side('right')
        
        logo_path = os.path.join(BASE_DIR, "assets", "school_logo.png")
        if os.path.exists(logo_path):
            logo_width = 320
            logo_height = 105
            # Center the logo in the right column
            logo_x = self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - logo_width) / 2
            c.drawImage(logo_path, logo_x, 80, logo_width, logo_height)
        else:
            c.setFont("Helvetica-Bold", 20)
            logo_text = "SCHOOL LOGO"
            logo_w = c.stringWidth(logo_text, "Helvetica-Bold", 20)
            c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - logo_w) / 2, 100, logo_text)
        
        c.setFont("Helvetica-Bold", 16)
        c_title = "STUDENT'S PROFILE"
        c_title_w = c.stringWidth(c_title, "Helvetica-Bold", 16)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - c_title_w) / 2, 545, c_title)
        
        c.setFont("Helvetica-Bold", 12)
        c_sess = f"Session {self.session_label}"
        c_sess_w = c.stringWidth(c_sess, "Helvetica-Bold", 12)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - c_sess_w) / 2, 565, c_sess)
        
        cover_y = 585
        cover_label_x = self.LAYOUT["leftX"] + 35
        cover_value_x = self.LAYOUT["leftX"] + 176.5
        spacing = 32.8
        
        def draw_cover_row(label, value, y_pos, right_label=None, right_value=None):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(cover_label_x, y_pos, label)
            c.setFont("Helvetica", 14)
            c.drawString(cover_value_x, y_pos, str(value))
            if right_label:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(self.LAYOUT["leftX"] + 247.5, y_pos, right_label)
                c.setFont("Helvetica", 14)
                c.drawString(self.LAYOUT["leftX"] + 360.5, y_pos, str(right_value))

        draw_cover_row("Student's CID:", self.student.get("cid", "-"), cover_y)
        cover_y += spacing
        draw_cover_row("Student's Name:", self.student.get("name", "-"), cover_y)
        cover_y += spacing
        draw_cover_row("Father's Name:", self.student.get("fatherName", "-"), cover_y)
        cover_y += spacing
        draw_cover_row("Grade:", self.config.get("gradeLevel", "-"), cover_y, "Section:", self.config.get("section", "-"))

        c.showPage()
        
        # SHEET 2
        # Left Side (Assessment Result)
        self.set_page_side('left')
        current_y = 98
        
        c.setFont("Helvetica-Bold", 16)
        title2 = f"{self.target_semester.upper()} ASSESSMENT RESULT"
        title2_w = c.stringWidth(title2, "Helvetica-Bold", 16)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - title2_w) / 2, current_y, title2)
        current_y += 25
        
        c.setFont("Helvetica", 12)
        sess_str = f"SESSION {self.session_label}"
        sess_w = c.stringWidth(sess_str, "Helvetica", 12)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - sess_w) / 2, current_y, sess_str)
        current_y += 45
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], current_y, "Student's Name:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 90, current_y, self.student.get("name", "-"))
        current_y += 20
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], current_y, "Father's Name:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 90, current_y, self.student.get("fatherName", "-"))
        current_y += 20
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], current_y, "Grade:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 40, current_y, self.config.get("gradeLevel", "-"))
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"] + 150, current_y, "Section:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 195, current_y, self.config.get("section", "-"))
        
        cid_val = str(self.student.get("cid", "-"))
        cid_val_w = c.stringWidth(cid_val, "Helvetica", 10)
        cid_lbl_w = c.stringWidth("CID No: ", "Helvetica-Bold", 10)
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["rightEdge"] - cid_val_w, current_y, cid_val)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["rightEdge"] - cid_val_w - cid_lbl_w, current_y, "CID No: ")
        current_y += 20
        
        left_subjs = len([s for s in self.config.get("subjectMap", {}).values() if "drawing" not in str(s).lower()])
        left_table_h = 35 + (left_subjs * 25) + 25
        right_evals = len(self.config.get("evaluationMap", {}))
        right_table_h = 35 + (right_evals * 25)
        shared_bottom_y = current_y + max(left_table_h, right_table_h) + 15
        
        base_p3_cols = [115, 55, 65, 75, 65, 70]
        scale3 = self.LAYOUT["tableWidth"] / 445
        p3_cols = [w * scale3 for w in base_p3_cols]
        sum_except_last_p3 = sum(p3_cols[:-1])
        p3_cols[-1] = self.LAYOUT["tableWidth"] - sum_except_last_p3
        
        h = self.draw_grid_row(c, current_y, ['Subject', 'Max\nMarks', 'Term\nMarks', 'Obtained\nMarks', 'Per %', 'Grade'], p3_cols, is_bold=True, is_header=True)
        current_y += h
        
        safe_grade_level = str(self.config.get("gradeLevel", "")).strip().upper()
        class_4_to_8_tokens = ['IV', 'V', 'VI', 'VII', 'VIII', '4', '5', '6', '7', '8']
        is_class_4_to_8 = any(safe_grade_level == t or f"CLASS {t}" in safe_grade_level or f"GRADE {t}" in safe_grade_level or safe_grade_level.endswith(f" {t}") for t in class_4_to_8_tokens)

        grand_total = 0
        total_max_marks = 900
        has_failed = False
        has_absent_4_to_8 = False

        for key, subject_name in self.config.get("subjectMap", {}).items():
            if "drawing" in subject_name.lower():
                continue
                
            subject_val = self.term_data.get(key, "-")
            subject_total = "-"
            subject_percent_display = "-"
            grade = "-"
            
            is_exempt = isinstance(subject_val, str) and subject_val.upper() in ("EXEMPT", "EXCUSED")
            is_absent = isinstance(subject_val, str) and subject_val.upper() == "ABSENT"

            if is_class_4_to_8 and is_exempt:
                subject_total = "EXCUSED"
                subject_percent_display = "EXCUSED"
                grade = "EXCUSED"
                total_max_marks -= 100
                h = self.draw_grid_row(c, current_y, [subject_name, '0', 'EXCUSED', subject_total, subject_percent_display, grade], p3_cols)
                current_y += h
            elif is_class_4_to_8 and is_absent:
                subject_total = "ABSENT"
                subject_percent_display = "ABSENT"
                grade = "ABSENT"
                has_absent_4_to_8 = True
                has_failed = True
                h = self.draw_grid_row(c, current_y, [subject_name, '100', 'ABSENT', subject_total, subject_percent_display, grade], p3_cols)
                current_y += h
            elif is_exempt:
                subject_total = "EXEMPT"
                subject_percent_display = "100%"
                grade = "A*"
                grand_total += 100
                h = self.draw_grid_row(c, current_y, [subject_name, '100', subject_val, subject_total, subject_percent_display, grade], p3_cols)
                current_y += h
            else:
                f_score = 0 if subject_val in ("ABSENT", "-") else float(subject_val) if str(subject_val).replace('.', '', 1).isdigit() else 0
                subject_total = subject_val if subject_val in ("ABSENT", "-") else f"{f_score:.1f}"
                subject_percent_display = f"{GradingEngine.custom_round(f_score)}%"
                grade = GradingEngine.calculate_grade(f_score)
                grand_total += f_score
                
                if grade == 'U':
                    has_failed = True
                h = self.draw_grid_row(c, current_y, [subject_name, '100', subject_val, subject_total, subject_percent_display, grade], p3_cols)
                current_y += h
                
        raw_overall_percent = (grand_total / total_max_marks * 100) if total_max_marks > 0 else 0
        overall_percent = GradingEngine.custom_round(raw_overall_percent)
        overall_grade = GradingEngine.calculate_grade(raw_overall_percent)

        if has_failed:
            overall_grade = 'U'

        display_overall_percent = "-" if has_failed else f"{overall_percent}%"
        display_overall_grade = "-" if has_failed else overall_grade

        if is_class_4_to_8 and has_absent_4_to_8:
            display_overall_percent = "-"
            display_overall_grade = "-"

        h = self.draw_grid_row(c, current_y, ['Total', str(total_max_marks), f"{grand_total:.1f}", f"{grand_total:.1f}", display_overall_percent, display_overall_grade], p3_cols, is_bold=True)
        current_y += h
        
        current_y = shared_bottom_y
        att_days = self.term_data.get("attendedDays", self.student.get("attendedDays"))
        term_total_working_days = self.term_data.get("totalWorkingDays", self.config.get("totalWorkingDays"))
        att_metrics = GradingEngine.get_attendance_metrics(att_days, term_total_working_days)
        
        att_days_str = att_days if att_days else "-"
        total_days_str = term_total_working_days if term_total_working_days else "-"
        combined_attendance = f"{att_metrics['attendanceStr']} ({att_days_str}/{total_days_str})"
        
        doc_y = current_y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], doc_y, "Attendance:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 130, doc_y, combined_attendance)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["rightEdge"] - 215, doc_y, "Attendance Remarks:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["rightEdge"] - 100, doc_y, att_metrics['attendanceRemarkStr'])
        doc_y += 20
        
        rank_val = self.term_data.get(self.config.get("rankKey", "Rank"), "-")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], doc_y, "Rank:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 130, doc_y, str(rank_val))
        doc_y += 20
        
        teacher_remarks = GradingEngine.get_teacher_remarks(overall_grade)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], doc_y, "Class Teacher's Remarks:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 130, doc_y, teacher_remarks)
        doc_y += 20
        
        promotion_remarks = self.term_data.get(self.config.get("promotionRemarksKey", "Promotion Remarks"), "")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], doc_y, "Promotion Remarks:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 130, doc_y, str(promotion_remarks))
        doc_y += 20
        
        self.draw_signatures(c, 725, "Class Teacher's Signature", "Principal's Signature", "Incharge's Signature")
        
        # Right Side (Annual Evaluation Report)
        self.set_page_side('right')
        eY = 98
        
        c.setFont("Helvetica-Bold", 16)
        title_er = "ANNUAL EVALUATION REPORT"
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - c.stringWidth(title_er, "Helvetica-Bold", 16)) / 2, eY, title_er)
        eY += 25
        
        c.setFont("Helvetica", 12)
        sess_str = f"SESSION {self.session_label}"
        sess_w = c.stringWidth(sess_str, "Helvetica", 12)
        c.drawString(self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - sess_w) / 2, eY, sess_str)
        eY += 45
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], eY, "Student's Name:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 90, eY, self.student.get("name", "-"))
        eY += 20
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], eY, "Father's Name:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 90, eY, self.student.get("fatherName", "-"))
        eY += 20
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], eY, "Grade:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 40, eY, self.config.get("gradeLevel", "-"))
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"] + 150, eY, "Section:")
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["leftX"] + 195, eY, self.config.get("section", "-"))
        
        cid_val = str(self.student.get("cid", "-"))
        cid_val_w = c.stringWidth(cid_val, "Helvetica", 10)
        cid_lbl_w = c.stringWidth("CID No: ", "Helvetica-Bold", 10)
        c.setFont("Helvetica", 10)
        c.drawString(self.LAYOUT["rightEdge"] - cid_val_w, eY, cid_val)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["rightEdge"] - cid_val_w - cid_lbl_w, eY, "CID No: ")
        eY += 20
        
        eval_cols = [self.LAYOUT["tableWidth"] - 80, 80]
        h = self.draw_grid_row(c, eY, ['Evaluation', 'Grade'], eval_cols, is_bold=True, is_header=True)
        eY += h
        
        for key, eval_name in self.config.get("evaluationMap", {}).items():
            eval_grade = self.term_data.get(key, "-")
            h = self.draw_grid_row(c, eY, [eval_name, eval_grade], eval_cols, center_first_col=True)
            eY += h
            
        eY = shared_bottom_y
        grade_headers = ['A', 'B', 'C', 'D', 'E']
        grade_remarks_arr = ['Excellent', 'Very Good', 'Good', 'Average', 'Satisfactory']
        g_table_width = 280
        g_left_x = self.LAYOUT["leftX"] + (self.LAYOUT["tableWidth"] - g_table_width) / 2
        g_col_width = g_table_width / 5
        
        c.setLineWidth(1)
        c.rect(g_left_x, eY, g_table_width, 15)
        for i, g in enumerate(grade_headers):
            if i > 0:
                c.line(g_left_x + (i * g_col_width), eY, g_left_x + (i * g_col_width), eY + 15)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(g_left_x + (i * g_col_width) + (g_col_width - c.stringWidth(g, "Helvetica-Bold", 9))/2, eY + 4, g)
        eY += 15
        
        c.rect(g_left_x, eY, g_table_width, 15)
        for i, r in enumerate(grade_remarks_arr):
            c.setFont("Helvetica", 9)
            c.drawString(g_left_x + (i * g_col_width) + (g_col_width - c.stringWidth(r, "Helvetica", 9))/2, eY + 4, r)
            if i > 0:
                c.line(g_left_x + (i * g_col_width), eY - 15, g_left_x + (i * g_col_width), eY)

        eY += 30
        
        import textwrap
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(self.LAYOUT["leftX"], eY, "Principal's Remarks:")
        raw_principal_remarks = GradingEngine.get_principal_remarks(overall_percent, self.student.get("name"), rank_val, overall_grade)
        
        c.setFont("Helvetica-Oblique", 10)
        
        # Approximate width constraint (max ~80-85 characters for 445pt width)
        wrapped_lines = textwrap.wrap(f'"{raw_principal_remarks}"', width=80)
        for idx, line in enumerate(wrapped_lines):
            c.drawString(self.LAYOUT["leftX"], eY + 15 + (idx * 15), line)
            
        self.draw_signatures(c, 725, "Class Teacher's Signature", "Principal's Signature", "Incharge's Signature")
        
        c.save()
        print(f"Generated Annual: {output_filename}")
