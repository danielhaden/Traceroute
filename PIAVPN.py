import subprocess

class PIAVPN:
    """Establishes VPN via Private Internet Access(PIA)"""

    execPath = r'C:\Program Files\Private Internet Access\piactl.exe'
    regions =  ["us-atlanta", "us-denver" , "us-texas", "us-houston", "us-chicago",
                "us-seattle", "us-silicon-valley", "us-west", "us-washington-dc", "us-east",
                "us-california", "us-new-york-city", "us-las-vegas", "us-florida", "ca-montreal",
                "ca-vancouver", "ca-toronto", "mexico", "uk-london", "uk-southampton",
                "uk-manchester", "ireland", "luxembourg", "denmark", "switzerland",
                "romania", "netherlands", "de-berlin", "de-frankfurt", "spain",
                "italy", "japan", "norway", "belgium", "france",
                "austria", "sweden", "poland", "new-zealand", "finland",
                "czech-republic", "hungary", "israel", "au-sydney", "au-perth",
                "au-melbourne", "singapore", "hong-kong", "uae"]

    def print_regions(self):
        for region in self.regions:
            print(region)

    def get_regions(self):
        return self.regions

    def disconnect(self):
        subprocess.call([self.execPath, "disconnect"])

    def connect_auto(self):
        subprocess.call([self.execPath, "connect"])

    def connect_to_region(self, region):
        self.disconnect()
        subprocess.call([self.execPath, "set", "region", region])
        self.connect_auto()