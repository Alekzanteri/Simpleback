#simplesite.py
import glob
import razorback as rb
from Simpleback.core.calibration import *
import numpy as np

class simplesite:
    
    """Simplesite class creates python object of mt-data in a given folder. 
    """
    
    def __init__(self, ts_folder, freq_rule):
        """
        self.inv is razorback inventory(data).
        self.site is sitename default for simpleback is "fieldiste".
        self.freqs is frequency array for prosessing.
        self.signalset is prepared timeseries.
        self.ImpMe is prosessed data.
        self.ts_len=length of self.signalset timeseries.
        self.sampling=sanpling rate of the data.
        """
        if(freq_rule==None):
            files=glob.glob(f'{ts_folder}\*.ats') #list of data files in given folder
        else:
            files=glob.glob(f'{ts_folder}\*{freq_rule}H.ats')
        pattern = "**\*_T{channel}_*.ats"
        tag_template = "fieldsite_{channel}"
        inv = rb.Inventory()#creating empty inventory
        print(rb.utils.tags_from_path(files, pattern, tag_template))#filling the inventory
        for fname, [tag] in rb.utils.tags_from_path(files, pattern, tag_template):
            calib = calibration(fname)  # getting calibration for data file
            signal = rb.io.ats.load_ats([fname], [calib])  # loading data file
            inv.append(rb.SignalSet({tag:0}, signal))  # tagging and storing the signal
        inv.filter('fieldsite*').pack()
        
        self.inv=inv#data
        self.site='fieldsite'#sitename
        self.freqs=None
        self.signalset=None
        self.ImpMe=None
        self.ts_len=None
        self.sampling=None
        self.cod=None
        self.nper=None
        self.overlap=None
        self.min_factor=None
        self.max_factor=None
        self.freq_amount=None
        
    def prepare_signalset(self):
        """Function for preparing signalset for preprosessing and prosessing"""
        patterns = (f"{e}*" for e in [self.site])
        signalset = self.inv.filter(*patterns).pack()
        tags = signalset.tags
        tags["E"] = tags[f"{self.site}_Ex"] + tags[f"{self.site}_Ey"]
        tags["B"] = tags[f"{self.site}_Hx"] + tags[f"{self.site}_Hy"]
        self.signalset=signalset
        self.sampling=self.signalset.sampling_rates[0]
        return
    

    def cut_timeseries(self):
        """This function cuts timeseries to 1h if it is longer than 1h 30 mins. Last 30mins are not used in long datasets."""
        # if timeseries is longer than 1h 30min it is cut to 1 h. Last 30mins are not used
        if(self.signalset.stops[0]-self.signalset.starts[0])/60/60>1.5:
            start_time=self.signalset.stops[0]-90*60
            stop_time=self.signalset.stops[0]-30*60
            self.signalset=self.signalset.extract_t(start_time, stop_time)
        self.ts_len=(self.signalset.stops[0]-self.signalset.starts[0])/60/60#ts length is saved
        return
    

    def calculate_freqs(self, min_factor=5, max_factor=1, freqs=15):
        """This function calculates frequency array for prosessing using time series length and sampling frequncy."""
        max=1/2*self.sampling*max_factor
        min=(self.ts_len/min_factor*1/2)**-1
        self.freqs=np.logspace(np.log10(min), np.log10(max), freqs)
        return

        
def sensor(ats_file):
    """This function is for getting metadata from a ats file."""
    header = rb.io.ats.read_ats_header(ats_file) #razorback function for ats file data importation
    chan = header['channel_type'].decode()
    stype = ''.join(c for c in header['sensor_type'].decode() if c.isprintable())
    snum = header['sensor_serial_number']
    sampling_rate = header['sampling_rate']
    Lat = header['ADU_Lat']
    Long = header['ADU_Long']
    Elev = header['ADU_Elev']    
    x1, y1, z1 = header['x1'], header['y1'], header['z1']
    x2, y2, z2 = header['x2'], header['y2'], header['z2']
    L = ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**.5
    return chan, L, stype, snum, sampling_rate, Lat, Long, Elev


def calibration(ats_file):
    """Function for choosing calibration files for coils and for getting dipol length."""
    chan, L, stype, snum, sampling_rate, Lat, Long, Elev = sensor(ats_file)
    if chan in ('Ex', 'Ey'):
        sitename = 'fieldsite'
        return L
    elif chan in ('Hx', 'Hy', 'Hz'):
        calib_name = f"{stype}{snum:02d}.TXT"
        return metronix(calib_name, sampling_rate)
    raise Exception(f"Unknown channel name: {chan}")