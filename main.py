import wx
import subprocess

class BluetoothDeviceListFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(BluetoothDeviceListFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)

        # Title for the List
        list_title = wx.StaticText(self.panel, label="Bluetooth Devices", pos=(10, 10))

        # ListBox to display devices
        self.device_list = wx.ListBox(self.panel, size=(400, 300), pos=(10, 40))

        # Create a BoxSizer for button layout
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Fixed-size buttons with spacing
        self.connect_button = wx.Button(self.panel, label="Connect", size=(100, 30))
        self.connect_button.Bind(wx.EVT_BUTTON, self.on_connect)
        button_sizer.Add(self.connect_button, 0, wx.ALL, 5)  # Add with 5px spacing

        self.disconnect_button = wx.Button(self.panel, label="Disconnect", size=(100, 30))
        self.disconnect_button.Bind(wx.EVT_BUTTON, self.on_disconnect)
        button_sizer.Add(self.disconnect_button, 0, wx.ALL, 5)  # Add with 5px spacing

        self.remove_button = wx.Button(self.panel, label="Remove", size=(100, 30))
        self.remove_button.Bind(wx.EVT_BUTTON, self.on_remove)
        button_sizer.Add(self.remove_button, 0, wx.ALL, 5)  # Add with 5px spacing

        # Set the button sizer at the bottom
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(list_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        main_sizer.Add(self.device_list, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)  # Add 10px bottom border

        self.panel.SetSizer(main_sizer)

        # Frame settings
        self.SetSize((340, 400))
        self.SetTitle("Bluetooth Devices List")
        self.Centre()

        # Fetch devices
        self.fetch_devices()

    def fetch_devices(self):
        """Fetch Bluetooth devices using `bluetoothctl devices` and display them in the ListBox."""
        try:
            result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True, check=True)
            devices = result.stdout.strip().split("\n")

            self.device_list.Clear()
            for device in devices:
                if device:
                    self.device_list.Append(device)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error fetching Bluetooth devices: {e}", "Error", wx.OK | wx.ICON_ERROR)
        except FileNotFoundError:
            wx.MessageBox("bluetoothctl command not found. Please ensure it is installed.", "Error", wx.OK | wx.ICON_ERROR)

    def on_connect(self, event):
        """Connect to the selected Bluetooth device."""
        selection = self.device_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("Please select a device to connect.", "Error", wx.OK | wx.ICON_ERROR)
            return

        device_info = self.device_list.GetString(selection)
        device_mac = device_info.split(" ")[1]  # Extract the MAC address

        try:
            subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
            wx.MessageBox(f"Connected to device {device_mac}", "Success", wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error connecting to device: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_disconnect(self, event):
        """Disconnect the selected Bluetooth device."""
        selection = self.device_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("Please select a device to disconnect.", "Error", wx.OK | wx.ICON_ERROR)
            return

        device_info = self.device_list.GetString(selection)
        device_mac = device_info.split(" ")[1]  # Extract the MAC address

        try:
            subprocess.run(["bluetoothctl", "disconnect", device_mac], check=True)
            wx.MessageBox(f"Disconnected from device {device_mac}", "Success", wx.OK | wx.ICON_INFORMATION)
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error disconnecting from device: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_remove(self, event):
        """Remove the selected Bluetooth device."""
        selection = self.device_list.GetSelection()
        if selection == wx.NOT_FOUND:
            wx.MessageBox("Please select a device to remove.", "Error", wx.OK | wx.ICON_ERROR)
            return

        device_info = self.device_list.GetString(selection)
        device_mac = device_info.split(" ")[1]  # Extract the MAC address

        try:
            subprocess.run(["bluetoothctl", "remove", device_mac], check=True)
            wx.MessageBox(f"Removed device {device_mac}", "Success", wx.OK | wx.ICON_INFORMATION)
            self.fetch_devices()  # Refresh the list after removal
        except subprocess.CalledProcessError as e:
            wx.MessageBox(f"Error removing device: {e}", "Error", wx.OK | wx.ICON_ERROR)

class BluetoothApp(wx.App):
    def OnInit(self):
        self.frame = BluetoothDeviceListFrame(None)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = BluetoothApp()
    app.MainLoop()