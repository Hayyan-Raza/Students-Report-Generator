import math
import re

class GradingEngine:
    @staticmethod
    def custom_round(number):
        if not math.isfinite(number):
            return 0
        return math.floor(number + 0.5)

    @staticmethod
    def calculate_grade(percentage):
        if percentage >= 94.555: return 'A*'
        if percentage >= 89.555: return 'A-1'
        if percentage >= 79.555: return 'A'
        if percentage >= 69.555: return 'B'
        if percentage >= 59.555: return 'C'
        if percentage >= 49.555: return 'D'
        if percentage >= 39.555: return 'E'
        return 'U'

    @staticmethod
    def get_teacher_remarks(overall_grade):
        if overall_grade in ("A*", "A-1"): return "Congratulations for Superb Result!"
        if overall_grade == "A": return "Excellent performance. Keep it up!"
        if overall_grade == "B": return "Good effort, keep striving for excellence."
        return "Work harder for the next term."

    @staticmethod
    def get_principal_remarks(overall_percent, student_name, rank_val, overall_grade):
        full_name = student_name if student_name else "Student"
        rank_str = str(rank_val or "").strip()
        r = float('nan')

        match = re.match(r'^(\d+)', rank_str)
        if match:
            r = int(match.group(1))

        if overall_grade != 'U' and not math.isnan(r) and 1 <= r <= 3:
            rank_remarks = {
                1: [
                    f"Congratulations for Superb Result!\n{full_name} is showing enthusiasm and accurate effort for better result which can shown by their result as per my view they are a great example for others.",
                    f"Congratulations for Marvelous Result!\n{full_name} is an enthusiastic learner, their effective participation also shown by their result. Must continue the same.",
                    f"Congratulations {full_name} on achieving {rank_str} position! Your hard work, dedication, and passion for learning have earned you this outstanding achievement. Keep shining!"
                ],
                2: [
                    f"Congratulations for Fantastic Result!\n{full_name} has great potential and brings fine contribution toward achieving the goal. Must continue the same.",
                    f"Congratulations for Terrific Result!\n{full_name} has great ability to work hard toward achieving the goal, continue the same.",
                    f"Heartiest congratulations to {full_name} on securing {rank_str} position! Your consistent effort and perseverance have paid off. Keep up the good work and strive for excellence!"
                ],
                3: [
                    f"Congratulations for Enormous Result!\n{full_name} has great prospective and showing active contribution toward achieving the goal. Must continue the same.",
                    f"Congratulations for Wonderful Result!\n{full_name} has been consistently progressing, shown a good attitude about trying to achieve the best. Must continue the same.",
                    f"Congratulations {full_name} on achieving {rank_str} position! Your hard work and determination have earned you this recognition. Keep pushing yourself to reach new heights!"
                ]
            }
            return rank_remarks[r][0]

        grade_remarks = {
            'A*': [
                f"Congratulations for achieving A* Result!\n{full_name} is a hard working student must continued to blossom as the year progressed.",
                f"Heartiest congratulations {full_name} on achieving an outstanding 'A*' grade! Your exceptional academic performance is a testament to your dedication and hard work. Keep excelling!"
            ],
            'A-1': [
                f"Congratulations for achieving \"A-1\" Result!\n{full_name} has great ability to work hard toward achieving the good result, continue the same in future.",
                f"Congratulations {full_name} on achieving an outstanding 'A-1' grade! Your outstanding academic achievement is a shining example of excellence. We are proud of you!"
            ],
            'A': [
                f"Congratulations for achieving \"A\" Grade Result!\n{full_name} is a sparkling child their positive effort can help them to upgrade the result.",
                f"Congratulations {full_name} on achieving an excellent 'A' grade! Your hard work and commitment to academic excellence have truly paid off. Well done!"
            ],
            'B': [
                f"Congratulations for achieving \"B\" Grade Result!\n{full_name} is a bright child their effort must be in accurate direction to help them to upgrade the result.",
                f"Congratulations {full_name} on achieving a commendable 'B' grade! Your efforts are appreciated, and with continued hard work, we are confident you will reach even greater heights."
            ],
            'C': [
                f"{full_name} is good in studies but extra support of Parents and Teacher might upgrade their result in future.",
                f"Well done {full_name} on achieving a satisfactory 'C' grade! We encourage you to continue working hard and striving for improvement. You have the potential to excel!"
            ],
            'D': [
                f"{full_name} is a capable student but required to improve their weak subject area.",
                f"{full_name}, although your 'D' grade result may not be what you hoped for, it's an opportunity to reflect and improve. Let's work together to set goals and strategies for future success."
            ],
            'E': [
                f"{full_name} is capable to proves their abilities more, extra support required to sparkle the academic condition.",
                f"{full_name}, your 'E' grade result indicates that you faced challenges this year. Let's schedule a meeting to discuss a plan for improvement and provide additional support to help you succeed."
            ],
            'U': [
                f"{full_name} is a progressing child but a poor examination marks have resulted in a failing grade. Need extra hard working to get good result in future."
            ]
        }

        if overall_grade in grade_remarks:
            return grade_remarks[overall_grade][0]

        return f"{full_name} should continue working on maintaining consistent performance across all subjects."

    @staticmethod
    def get_attendance_metrics(attended_days, total_working_days):
        attendance_str = "-"
        attendance_remark_str = "-"
        
        try:
            total_working_days = float(total_working_days) if total_working_days else 0
        except ValueError:
            total_working_days = 0
            
        if total_working_days > 0 and attended_days is not None and str(attended_days).strip() != "":
            try:
                att_days = float(attended_days)
                if not math.isnan(att_days):
                    att_percent = GradingEngine.custom_round((att_days / total_working_days) * 100)
                    attendance_str = f"{att_percent}%"
                    
                    if att_percent >= 90: attendance_remark_str = "Marvellous"
                    elif att_percent >= 80: attendance_remark_str = "Excellent"
                    elif att_percent >= 70: attendance_remark_str = "Good"
                    elif att_percent >= 60: attendance_remark_str = "Satisfactory"
                    else: attendance_remark_str = "Need to be regular"
            except ValueError:
                pass
                
        return {"attendanceStr": attendance_str, "attendanceRemarkStr": attendance_remark_str}

class DataProcessor:
    def __init__(self, raw_data, fallback_grade):
        self.raw_data = raw_data
        self.config = {
            "gradeLevel": fallback_grade,
            "section": "Jinnah",
            "totalWorkingDays": 0,
            "cidKey": None, "nameKey": None, "fatherKey": None, "termKey": None, "attendedDaysKey": None,
            "totalWorkingDaysKey": None, "rankKey": None, "promotionRemarksKey": None,
            "subjectMap": {},
            "evaluationMap": {}
        }
        self.students = {}
        self.parse_config()
        self.group_students()

    def parse_config(self):
        for row in self.raw_data:
            keys = list(row.keys())
            for i, key in enumerate(keys):
                val = row[key]
                if val == 'Class' and i + 1 < len(keys): self.config["gradeLevel"] = row[keys[i + 1]]
                if val == 'Section' and i + 1 < len(keys): self.config["section"] = row[keys[i + 1]]
                if val == 'Total Working Days' and i + 1 < len(keys):
                    try:
                        self.config["totalWorkingDays"] = float(row[keys[i + 1]])
                    except ValueError:
                        self.config["totalWorkingDays"] = 0

        header_row = next((r for r in self.raw_data if "CID" in r.values()), None)

        evaluation_metrics = [
            "Interaction with the Teacher", "Behaviour with the students", "Participation in co-curricular activities",
            "Punctuality / Regularity", "Neatness", "English Conversation", "Presentation / Project Work",
            "Hand Writing", "Home Assignment", "Conduct"
        ]

        exclude_keys = [
            "Total", "Total Earned", "Result", "Class Teacher's Remarks", "Principal's Remarks",
            "Promotion Remarks", "Rank", "Total Marks", "Term %", "Grand %",
            "Attended Days", "Total Subjects", "Total Working Days",
            "CID", "Name", "Father’s Name", "Father's Name", "Term", "Class", "Section"
        ]

        if header_row:
            for key, val in header_row.items():
                if val == "CID": self.config["cidKey"] = key
                elif val == "Name": self.config["nameKey"] = key
                elif val in ("Father’s Name", "Father's Name"): self.config["fatherKey"] = key
                elif val == "Term": self.config["termKey"] = key
                elif val == "Attended Days": self.config["attendedDaysKey"] = key
                elif val == "Total Working Days": self.config["totalWorkingDaysKey"] = key
                elif val == "Rank": self.config["rankKey"] = key
                elif val == "Promotion Remarks": self.config["promotionRemarksKey"] = key
                elif isinstance(val, str):
                    trimmed_val = val.strip()
                    if trimmed_val:
                        if trimmed_val in evaluation_metrics:
                            self.config["evaluationMap"][key] = trimmed_val
                        elif trimmed_val not in exclude_keys and "SEMESTER" not in trimmed_val.upper():
                            self.config["subjectMap"][key] = trimmed_val

    def group_students(self):
        last_cid, last_name, last_father = None, None, None

        for row in self.raw_data:
            term_val = row.get(self.config["termKey"]) if self.config["termKey"] else None
            current_row_cid = row.get(self.config["cidKey"])
            if current_row_cid and str(current_row_cid).strip().upper() in ('CID', 'CID NO', 'CID NO.', '__EMPTY'):
                continue
            
            if current_row_cid:
                last_cid = current_row_cid
                last_name = row.get(self.config["nameKey"])
                last_father = row.get(self.config["fatherKey"])

            if not last_cid or not term_val:
                continue

            term_val_clean = term_val.strip()
            
            if last_cid not in self.students:
                self.students[last_cid] = {
                    "cid": last_cid,
                    "name": last_name,
                    "fatherName": last_father,
                    "terms": {}
                }

            self.students[last_cid]["terms"][term_val_clean] = row

            if self.config["attendedDaysKey"] and row.get(self.config["attendedDaysKey"]):
                self.students[last_cid]["terms"][term_val_clean]["attendedDays"] = row[self.config["attendedDaysKey"]]
            
            if self.config["totalWorkingDaysKey"] and row.get(self.config["totalWorkingDaysKey"]):
                self.students[last_cid]["terms"][term_val_clean]["totalWorkingDays"] = row[self.config["totalWorkingDaysKey"]]
