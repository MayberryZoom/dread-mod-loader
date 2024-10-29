import shutil
from ftplib import FTP
from pathlib import Path
from traceback import format_exception

from mercury_engine_data_structures.file_tree_editor import OutputFormat
from PySide6.QtWidgets import QDialog, QErrorMessage, QMessageBox, QWidget

from dread_mod_loader.gui.generated.export_dialog_ui import Ui_ExportDialog
from dread_mod_loader.logger import LOG
from dread_mod_loader.settings import UserSettings, user_settings

# The temp local path to use for FTP export
# This needs to be resolved so a relative_to() call in MEDS doesn't get confused, and it's easiest to do it now
temp_path = Path("temp").resolve()

ftp_error_text = "Could not connect to FTP. Please ensure you have entered the connection information correctly."

class ExportParams:
    def __init__(self, romfs_path: Path, exefs_path: Path, exefs_patches_path: Path,
                 output_format: OutputFormat = OutputFormat.ROMFS, ftp: bool = False) -> None:
        self.romfs_path = romfs_path
        self.exefs_path = exefs_path
        self.exefs_patches_path = exefs_patches_path
        self.output_format = output_format
        self.ftp = ftp

class ExportDialog(QDialog, Ui_ExportDialog):
    def __init__(self, settings: UserSettings, settings_dialog_class,
                 disabled_settings: list[str], parent: QWidget) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.settings = settings
        self.settings_dialog = settings_dialog_class(self, self.settings, disabled_settings)
        self.export_params = None

        # Set up general UI
        self.export_combo_box.changed_callback = self._change_export_method
        self.export_stacked_widget.setCurrentIndex(user_settings["default_export_combo_box"])

        # Set up Switch UI
        self.switch_tab.setCurrentIndex(user_settings["default_switch_method"])

        self.ftp_anonymous_checkbox.clicked_callback = self._check_anonymous
        self._check_anonymous(user_settings[self.ftp_anonymous_checkbox.setting_name])

        # Set up file dialog buttons
        self.input_romfs_button.line_edit = self.input_romfs_line_edit
        self.ryujinx_path_button.line_edit = self.ryujinx_path_line_edit
        self.advanced_romfs_button.line_edit = self.advanced_romfs_line_edit
        self.advanced_exefs_button.line_edit = self.advanced_exefs_line_edit
        self.advanced_exefs_patches_button.line_edit = self.advanced_exefs_patches_line_edit

        # Add callback to validated line edits
        validated_line_edits = [
            self.input_romfs_line_edit,
            self.ryujinx_path_line_edit,
            self.ftp_ip_line_edit,
            self.ftp_port_line_edit,
            self.ftp_username_line_edit,
            self.advanced_romfs_line_edit,
            self.advanced_exefs_line_edit,
            self.advanced_exefs_patches_line_edit,
        ]

        for line_edit in validated_line_edits:
            line_edit.update_callback = self._validate_export_options

        # Validate default input
        self._validate_export_options()

        # Initialize error dialog
        self.error_dialog = QErrorMessage(self)
        self.error_dialog.setWindowTitle("Error")

# Special handling for specific widgets

    def _change_export_method(self, index: int) -> None:
        self.export_stacked_widget.setCurrentIndex(index)

        self._validate_export_options()

    def _change_switch_method(self, index: int) -> None:
        user_settings["default_switch_method"] = index

        self._validate_export_options()

    def _check_anonymous(self, checked: bool) -> None:
        if checked:
            self.ftp_username_line_edit.setText("")
            self.ftp_username_line_edit.set_valid(True)

            self.ftp_password_line_edit.setText("")
            self.ftp_password_line_edit.set_valid(True)

        self.ftp_username_line_edit.setEnabled(not checked)
        self.ftp_password_line_edit.setEnabled(not checked)

        self._validate_export_options()

# User input validation

    def _validate_export_options(self) -> bool:
        is_valid = True
        export_method = self.export_combo_box.currentText()

        # General checks
        romfs_files_to_check = [
            "config.ini",
            "system/files.toc",
            "packs/players/samus.pkg",
        ]

        if not self.input_romfs_line_edit.validate_files(romfs_files_to_check):
            is_valid = False

        # Ryujinx checks
        if export_method == "Ryujinx":
            ryujinx_files_to_check = [
                "system/prod.keys",
                "bis",
            ]

            if not self.ryujinx_path_line_edit.validate_files(ryujinx_files_to_check):
                is_valid = False

        # Switch checks
        elif export_method == "Switch":
            switch_method = self.switch_tab.currentWidget()

            if switch_method == self.ftp:
                if not self.ftp_ip_line_edit.validate_not_empty():
                    is_valid = False
                if not self.ftp_port_line_edit.validate_not_empty():
                    is_valid = False
                if not self.ftp_anonymous_checkbox.isChecked() and not self.ftp_username_line_edit.validate_not_empty():
                    is_valid = False

            elif switch_method == self.usb and not self.usb_combo_box.currentText():
                    is_valid = False

        # Advanced checks
        elif export_method == "Advanced":
            if not self.advanced_romfs_line_edit.validate_not_empty():
                is_valid = False
            if not self.advanced_exefs_line_edit.validate_not_empty():
                is_valid = False
            if not self.advanced_exefs_patches_line_edit.validate_not_empty():
                is_valid = False

        # Final
        self.export_button.setEnabled(is_valid)
        return is_valid

# Mod settings

    def _show_mod_settings(self) -> None:
        self.settings_dialog.exec()

# Export functions

    def _set_export_params(self) -> None:
        export_method = self.export_combo_box.currentText()
        formatted_name = self.parent().name.replace(" ", "")

        # Ryujinx
        if export_method == "Ryujinx":
            mod_dir = Path(self.ryujinx_path_line_edit.text()) / "mods/contents/010093801237C000" / formatted_name

            self.export_params = ExportParams(
                mod_dir / "romfs",
                mod_dir / "exefs",
                mod_dir / "exefs"
            )

        # Switch
        elif export_method == "Switch":
            switch_method = self.switch_tab.currentWidget()

            if switch_method == self.ftp:
                output_root = temp_path
            else:
                output_root = Path(self.usb_combo_box.currentText())

            use_smm = self.smm_checkbox.isChecked()

            if use_smm:
                mod_dir = output_root / "mods/Metroid Dread" / formatted_name
                contents_path = "contents/010093801237C000"

                self.export_params = ExportParams(
                    mod_dir / contents_path / "romfs",
                    mod_dir / contents_path / "exefs",
                    mod_dir / "exefs_patches" / formatted_name
                )
            else:
                contents_dir = output_root / "atmosphere/contents/010093801237C000"

                self.export_params = ExportParams(
                    contents_dir / "romfs",
                    contents_dir / "exefs",
                    output_root / "atmosphere/exefs_patches/010093801237C000" / formatted_name
                )

            if switch_method == self.ftp:
                self.export_params.ftp = True

        # Advanced export
        elif export_method == "Advanced":
            selected_format = self.advanced_format_combo_box.currentText()
            output_format = None

            if selected_format == "ROMFS":
                output_format = OutputFormat.ROMFS
            elif selected_format == "PKG":
                output_format = OutputFormat.PKG

            self.export_params = ExportParams(
                Path(self.advanced_romfs_line_edit.text()),
                Path(self.advanced_exefs_line_edit.text()),
                Path(self.advanced_exefs_patches_line_edit.text()),
                output_format
            )

    def _export_button_pressed(self) -> None:
        export_valid = self._validate_export_options()

        if not export_valid:
            self.export_button.setEnabled(False)
            return

        try:
            self.export()
        except Exception as e:
            LOG.error(e)
            self.export_label.setText("")
            self.export_progress.setValue(0)
            self.error_dialog.showMessage("\n".join(format_exception(e)))
            raise e

    def export(self) -> None:
        self._set_export_params()

        if self.export_params.ftp:
            # FTP has an extra step, so the progress bar should increase less
            progress_steps = 25
            ftp_client = FTP()
        else:
            progress_steps = 33.33

        self.export_progress.setValue(0)

        self.export_label.setText("Starting")
        LOG.info("Starting export")
        self.parent().start(Path(self.input_romfs_line_edit.text()))
        self.export_progress.setValue(round(progress_steps * 1))

        self.export_label.setText("Patching")
        LOG.info("Patching")
        self.parent().patch()
        self.export_progress.setValue(round(progress_steps * 2))

        self.export_label.setText("Exporting")
        LOG.info("Saving game modifications")
        self.parent().export(self.export_params)
        self.export_progress.setValue(round(progress_steps * 3))

        if self.export_params.ftp:
            self.export_label.setText("Uploading")
            LOG.info("Uploading files")

            try:
                ftp_client.connect(self.ftp_ip_line_edit.text(), int(self.ftp_port_line_edit.text()))

                if self.ftp_anonymous_checkbox.isChecked():
                    ftp_client.login()
                else:
                    ftp_client.login(self.ftp_username_line_edit.text(), self.ftp_password_line_edit.text())
            except Exception:
                shutil.rmtree(temp_path, True)

                message_box = QMessageBox(
                    title="",
                    text=ftp_error_text,
                    parent=self
                )

                if message_box.exec():
                    self.export_label.setText("")
                    self.export_progress.setValue(0)
                    return

            try:
                nlists = {}

                for file in temp_path.rglob("*"):
                    relative_to_root = "/" + file.relative_to(temp_path).as_posix()
                    parent_path = file.parent.relative_to(temp_path).as_posix()

                    if parent_path not in nlists:
                        nlists[relative_to_root] = ftp_client.nlst(parent_path)

                    if file.is_file():
                        if relative_to_root not in nlists[relative_to_root]:
                            with file.open("rb") as file_buffer:
                                ftp_client.storbinary(f"STOR {relative_to_root}", file_buffer)
                    else:
                        if relative_to_root not in nlists[relative_to_root]:
                            ftp_client.mkd(relative_to_root)
            except Exception as e:
                LOG.error(e)
                raise e

            ftp_client.quit()

            shutil.rmtree(temp_path, True)


        LOG.info("Export complete")
        self.export_label.setText("Export complete")
        self.export_progress.setValue(100)
