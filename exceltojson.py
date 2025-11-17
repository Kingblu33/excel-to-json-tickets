import sys
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox


class ExcelToJsonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel to JSON")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()

        self.button = QPushButton("Select Excel File")
        self.button.clicked.connect(self.select_file)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")

        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)

            tickets = []
            for index, row in df.iterrows():
                comment_body = (
                    f"Vin:{row.get('VIN')}\n"
                    f"Unit Number:{row.get('Unit')}\n"
                    f"technote:{row.get('Tech note on R')}\n"
                )

                ticket = {
                    "subject": "Sr Audit",
                    "priority": "normal",
                    # need to replace with actual group id
                    "group_id": "sadsadadsa",
                    "assignee_id": row.get("Assignee ID", default = 0),
                    "group_id": row.get("Group ID", default = 0),
                    "comment": {"body": comment_body}
                }

                tickets.append(ticket)

            final_json = {"tickets": tickets}

            with open("output.txt", "w",) as f:
                f.write(json.dumps(final_json, indent=2))

            QMessageBox.information(self, "Success", "output.txt has been created.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelToJsonApp()
    window.show()
    sys.exit(app.exec())
