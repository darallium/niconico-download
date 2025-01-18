import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import sys

import yt_dlp
from multiprocessing import Process, freeze_support

import webbrowser

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def check_aria2c():
    if os.path.exists("aria2c.exe"):
        print(os.path.abspath("aria2c.exe"))
        return True
    else:
        return False


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        while not check_aria2c():
            msg_aria2c = CTkMessagebox(
                title="Error",
                icon="cancel",
                option_1="Ready",
                option_2="Exit",
                option_3="Open Browser",
                width=600,
                message="""
***Aria2c not found***. 
Please download it from https://github.com/aria2/aria2/releases/latest
And unzip the file
And place it in the same directory as this script.""",
            )

            response = msg_aria2c.get()
            if response == "Exit":
                self.destroy()
                sys.exit()
            if response == "Open Browser":
                webbrowser.open("https://github.com/aria2/aria2/releases/latest")

        self.title("nico-dlp GUI")
        self.geometry("700x600")

        self.config_file = "config.conf"
        self.config = self.load_config()
        self.create_widgets()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []  # ファイルがない場合は空のリスト

        config = {}
        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line:
                continue  # コメントと空行は無視
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
            else:
                config[line.strip()] = True  # フラグ形式のオプション

        return config

    def save_config(self):
        with open(self.config_file, "w") as f:
            for key, value in self.config.items():
                if value is True:  # フラグ形式
                    f.write(f"{key}\n")
                else:
                    f.write(f"{key} {value}\n")

    def create_widgets(self):
        # Output
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(pady=10, padx=20, fill="x")

        self.output_label = ctk.CTkLabel(self.output_frame, text="Output Template:")
        self.output_label.grid(row=0, column=0, sticky="w")
        self.output_entry = ctk.CTkEntry(
            self.output_frame,
            width=500,
            textvariable=ctk.StringVar(
                value=self.config.get(
                    "-o", "./Videos/%(channel)s/%(title)s-%(id)s.%(ext)s"
                )
            ),
        )
        self.output_entry.grid(row=0, column=1, padx=5)
        self.config["-o"] = self.output_entry.get()

        # Quality
        self.quality_frame = ctk.CTkFrame(self)
        self.quality_frame.pack(pady=10, padx=20, fill="x")

        self.quality_label = ctk.CTkLabel(self.quality_frame, text="Format:")
        self.quality_label.grid(row=0, column=0, sticky="w")
        self.quality_entry = ctk.CTkEntry(
            self.quality_frame,
            width=500,
            textvariable=ctk.StringVar(
                value=self.config.get("-f", "bestvideo[ext=mp4]+bestaudio/best")
            ),
        )
        self.quality_entry.grid(row=0, column=1, padx=5)

        # Downloader args
        self.downloader_args_frame = ctk.CTkFrame(self)
        self.downloader_args_frame.pack(pady=10, padx=20, fill="x")

        self.downloader_args_label = ctk.CTkLabel(
            self.downloader_args_frame, text="Downloader Args:"
        )
        self.downloader_args_label.grid(row=0, column=0, sticky="w")
        self.downloader_args_entry = ctk.CTkEntry(
            self.downloader_args_frame,
            width=500,
            textvariable=ctk.StringVar(
                value=self.config.get(
                    "--external-downloader-args", "-c -j 3 -x 3 -s 6 -k 1M"
                )
            ),
        )
        self.downloader_args_entry.grid(row=0, column=1, padx=5)

        # Checkboxes
        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.pack(pady=10, padx=20, fill="x")

        self.checkboxes = {
            "--add-metadata": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Add Metadata",
                variable=ctk.BooleanVar(value=self.config.get("--add-metadata", False)),
            ),
            "--embed-thumbnail": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Embed Thumbnail",
                variable=ctk.BooleanVar(
                    value=self.config.get("--embed-thumbnail", False)
                ),
            ),
            "--write-sub": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Write Subtitles",
                variable=ctk.BooleanVar(value=self.config.get("--write-sub", False)),
            ),
            "--all-subs": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="All Subtitles",
                variable=ctk.BooleanVar(value=self.config.get("--all-subs", False)),
            ),
            "--write-info-json": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Write Info JSON",
                variable=ctk.BooleanVar(
                    value=self.config.get("--write-info-json", False)
                ),
            ),
            "--get-comments": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Get Comments",
                variable=ctk.BooleanVar(value=self.config.get("--get-comments", False)),
            ),
            "--ignore-errors": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Ignore Errors",
                variable=ctk.BooleanVar(
                    value=self.config.get("--ignore-errors", False)
                ),
            ),
            "--continue": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="Continue",
                variable=ctk.BooleanVar(value=self.config.get("--continue", False)),
            ),
            "--no-overwrites": ctk.CTkCheckBox(
                self.checkbox_frame,
                text="No Overwrites",
                variable=ctk.BooleanVar(
                    value=self.config.get("--no-overwrites", False)
                ),
            ),
        }

        row = 0
        col = 0

        for checkbox in self.checkboxes.values():
            checkbox.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Save Button
        self.save_button = ctk.CTkButton(
            self, text="Save Config", command=self.save_config_click
        )
        self.save_button.pack(pady=20)

        # Download link
        self.download_frame = ctk.CTkFrame(self)
        self.download_frame.pack(pady=10, padx=20, fill="x")

        self.download_label = ctk.CTkLabel(
            self.download_frame, text="download video url:"
        )
        self.download_label.grid(row=0, column=0, sticky="w")
        self.download_entry = ctk.CTkEntry(
            self.download_frame,
            width=500,
            textvariable=ctk.StringVar(
                value="https://www.nicovideo.jp/watch/sm9"  # デフォルトのURL
            ),
        )
        self.download_entry.grid(row=0, column=1, padx=5)

        self.download_button = ctk.CTkButton(
            self, text="download", command=self.run_download
        )
        self.download_button.pack(pady=20)

    def save_config_click(self):
        self.config["-o"] = self.output_entry.get()
        self.config["-f"] = self.quality_entry.get()
        self.config["--external-downloader-args"] = self.downloader_args_entry.get()

        for key, checkbox in self.checkboxes.items():
            if checkbox.get() == 1:
                self.config[key] = True

        self.save_config()
        CTkMessagebox(title="Success", message="Config saved successfully!")

    def run_download(self):
        url = self.download_entry.get()
        p = Process(target=download_video, args=(url, self.config_file))
        p.start()


def download_video(url, config_file):
    ydl_opts = {
        "config_location": config_file,
    }
    ydl_opts = {
        "outtmpl": "./Videos/%(channel)s/%(title)s-%(id)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio/best",
        "external_downloader": "aria2c",
        "external_downloader_args": ["-c", "-j", "3", "-x", "3", "-s", "6", "-k", "1M"],
        "addmetadata": True,
        "embedthumbnail": True,
        "writesubtitles": True,
        "allsubtitles": True,
        "writeinfojson": True,
        "getcomments": True,
        "ignoreerrors": True,
        "continue": True,
        "nooverwrites": True,
    }
    print(f"Downloading {url}")
    print(f"Config file: {config_file}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # print config
        print(ydl.params)
        ydl.download([url])


def gui_run():
    freeze_support()
    app = App()
    app.mainloop()
    sys.exit()


if __name__ == "__main__":
    gui_run()
