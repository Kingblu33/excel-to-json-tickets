import sys
import json
import os
import pandas as pd
from textwrap import dedent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon


class HINOTICKETS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hino Replacement Tickets")
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
            df = pd.read_excel(file_path, sheet_name = "Email",dtype=str)
            print(df)
            tickets = []
            results = df.groupby("LOC")
            print(results)

            for email, group in results:
                email_group = group["EMAIL"].iloc[0]
                shop_num = str(group["LOC"].iloc[0]).strip()
                units = group["VIN"].tolist()
                unit_group = ", ".join(str(unit) for unit in units)
                print(email_group, shop_num, unit_group)

                comment_body = dedent(f"""
                    Team,

                    The below units will need the Hino device replaced. Could you please provide me with a location to send the device(s)?

                    {unit_group}

                    Thank you,
                    Demmar Allen
                    Senior Onboard Connectivity Specialist/Digital Experience
                    E demmar.allen@penske.com

                    Penske
                    Rental | Leasing | Logistics
                    2675 Morgantown Road
                    Reading, PA 19607 USA

                    Web | Blog | Social
                """).strip()

                # num = random.randint(1, 5000)

                ticket = {
                    "subject": f"Hino Device Replacement: {shop_num}",
                    "priority": "normal",
                    "group_id": 22431148342167,
                    "requester": {
                        "email": "Thomas.Pham@penske.com",
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
    window = HINOTICKETS()
    window.show()
    sys.exit(app.exec())