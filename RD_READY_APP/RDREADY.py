import sys
import json
import os
import random
import pandas as pd
from textwrap import dedent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon


class RDREADY5EMAILS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RDREADY NUKE")
        self.setFixedSize(450, 150)
        self.setWindowIcon(QIcon("RD_READY_APP/trailer.png"))

        layout = QVBoxLayout()

        self.button = QPushButton("Select Excel File")
        self.button.clicked.connect(self.select_file)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        file_name_ext = os.path.basename(file_path)
        fileName = os.path.splitext(file_name_ext)[0]

        try:
            df = pd.read_excel(file_path, sheet_name="Clean")

            tickets = []
            results = df.groupby("EMAIL")

            for email, group in results:
                email_group = group["EMAIL"].iloc[0]
                shop_num = str(group["SHOP"].iloc[0]).strip()
                units = group["UNIT"].tolist()
                unit_group = ", ".join(str(unit) for unit in units)

                comment_body = dedent(f"""
                    Dear Shop {shop_num},

                    We recently sent [one / multiple] device(s) to your shop as part of the OTH RDREADY5 campaign for trailer(s):

                    {unit_group}

                    We’re reaching out to ask that the device(s) be installed and connected as soon as possible so we can ensure proper connectivity and reporting.

                    If the installation has already been completed, thank you, and please feel free to ignore this message. Otherwise, let us know if you need any assistance.

                    We appreciate your help and cooperation.

                    Thank you,

                    Jon

                    Sr. Onboard Connectivity Specialist/Digital Experience
                """).strip()

                # num = random.randint(1, 5000)

                ticket = {
                    "subject": f"Reminder: OTH RDREADY5 Device Installation Needed {shop_num}",
                    "priority": "normal",
                    "group_id": 22431148342167,
                    "requester": {
                        "email": "Jonathan.Brein@penske.com",
                        "action": "put"
                    },
                    "comment": {
                        "body": comment_body,
                        "public": True
                    },
                    "email_ccs": [
                        {
                            "user_email": email_group,
                            "action": "put"
                        },
                        {
                            "user_email": "Jonathan.Brein@penske.com",
                            "action": "put"
                        },
                        {
                            "user_email": "Demmar.allen@penske.com",
                            "action": "put"
                        }
                    ]
                }

                tickets.append(ticket)

            final_json = {"tickets": tickets}

            with open(f"output({fileName}).txt", "w") as f:
                f.write(json.dumps(final_json, indent=2))

            QMessageBox.information(
                self,
                "Success",
                f"output({fileName}).txt has been created."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# rebuild command:
# pyinstaller --onefile --noconsole --icon=trailer.ico RDREADY.py
# pyinstaller --onefile --noconsole --icon=trailer.ico --add-data "trailer.png" RDREADY.py


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RDREADY5EMAILS()
    window.show()
    sys.exit(app.exec())