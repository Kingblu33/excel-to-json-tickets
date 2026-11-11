import sys
import json
import os
from dotenv import load_dotenv
import random
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon


class VPTICKETS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPTICKETS")
        self.setFixedSize(450, 150)
        self.setWindowIcon(QIcon('truck.png'))

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

        print(fileName)
        
        # print(len(file_path))
        load_dotenv()
        individual_ids = [int(id.strip()) for id in os.getenv("individual_ids").split(",")]
        print(individual_ids)
        # imp_profile_ids = [12329, 12330]



        try:
            df = pd.read_excel(file_path, sheet_name="Tickets")

            tickets = []
            for index, row in df.iterrows():
                comment_body = (
                    f"Vin: {row.get('VIN')}\n\n"
                    f"Unit: {row.get('Unit')}\n\n"
                    f"Make: {row.get('Make')}\n\n"
                    f"First API Date: {row.get('First API Date')}\n\n"
                    f"Latest API Date {row.get('Latest API Date')}\n\n"
                    f"API Call Message: {row.get('API Call Message')}\n\n"
                    f"API Status Message: {row.get('API Status Message')}\n\n"
                    f"Job Profile ID: {row.get('Job Profile ID')}\n\n"
                    f"Action: {row.get('Action')}\n\n"
                    )

                assignee_id = random.choice(individual_ids)

                ticket = {
                    "subject": "VP Dashboard Ticket Upload",
                    # "requester": {
                    #     "user_id": assignee_id,
                    #     "action": "put"
                    # },
                    "priority": "normal",
                    "group_id": 22431148342167,
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

# rebuild command: pyinstaller --onefile --noconsole --icon=app.ico exceltojson.py 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VPTICKETS()
    window.show()
    sys.exit(app.exec())
