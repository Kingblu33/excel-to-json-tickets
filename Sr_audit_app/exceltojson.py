import sys
import json
import os
import random
from dotenv import load_dotenv
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ExcelToJsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SR Audit NUKE(V3)")
        self.setFixedSize(450, 150)
        self.setWindowIcon(QIcon(resource_path('Sr_audit_app/trailer.png')))

        layout = QVBoxLayout()

        self.button = QPushButton("Select Excel File")
        self.button.clicked.connect(self.select_file)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")


        if not file_path:
            return
        file_name_ext = os.path.basename(file_path)
        fileName = os.path.splitext(file_name_ext)[0]
        # bs 

        
        load_dotenv(resource_path("Sr_audit_app/.env"))
       

        individual_ids = [int(id.strip()) for id in os.getenv("INDIVIDUAL_IDS").split(",")]
        group_id = int(os.getenv("Group_id"))
        # imp_profile_ids = [12329, 12330]

        try:
            df = pd.read_excel(file_path, sheet_name="Clean Report")

            tickets = []
            counter = 0 
            for index, row in df.iterrows():
                comment_body = (
                    f"Vin: {row.get('VIN')}\n\n"
                    f"Unit: {row.get('Unit')}\n\n"
                    f"SR: {row.get('SR#')}\n\n"
                    f"District: {row.get('RO Owner')}\n\n"
                    f"RO: {row.get('RO')}\n\n"
                    f"SN#: {row.get('SN#')}\n\n"
                    f"Tech Note: {row.get('Tech note on RO')}\n\n"
                    f"VDA Note: {row.get('VDA Note')}\n\n"
                    f"Installed TSP: {row.get('Installed TSP')}\n\n"
                    f"Transmitting TSP: {row.get('Transmitting TSP')}\n\n"
                    f"In-Service Date: {row.get('In service date')}\n\n"
                    f"Profile ID: {row.get('Profile ID')}\n\n"
                    f"Profile Name: {row.get('Translation')}\n\n"
                    f"Service Email: {row.get('SBM email based on RO Owner')}\n\n"
                    )
                
                # profile_id = row.get('Profile ID')
                assignee_id = individual_ids[counter % len(individual_ids)]
                counter += 1

                # if profile_id in imp_profile_ids:
                #     assignee_id = random.choice(individual_ids)
                #     print(assignee_id)

                    # Add tags for colby 
                ticket = {
                    "subject": "Sr Audit",
                    # "subject": "TEST - Sr Audit",
                    "priority": "normal",
                    "group_id": group_id,
                    "tags": ["Sr_Audit"],
                    "assignee_id":assignee_id,
                    "comment": {"body": comment_body}
                }

                tickets.append(ticket)

            final_json = {"tickets": tickets}

            with open(f"output({fileName}).txt", "w",) as f:
                f.write(json.dumps(final_json, indent=2))

            QMessageBox.information(self, "Success", f"output({fileName}).txt has been created.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

#pyinstaller --onefile --noconsole --icon=app.ico --add-data "trailer.png;Sr_audit_app" --add-data ".env;Sr_audit_app" exceltojson.py

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelToJsonApp()
    window.show()
    sys.exit(app.exec())
