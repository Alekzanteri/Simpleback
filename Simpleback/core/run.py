#run.py
from Simpleback.core.simplesite import *
import razorback as rb
from razorback.weights import mest_weights
from razorback.prefilters import cod_filter
from Simpleback.core.plot import *

def simpleback(ts_folder, freq_rule=None, cod=0.3, nper=250.0, overlap=0.3, min_factor=5.0, max_factor=1.0, freqs=15):
    
    """This is master function of simpleback fast field prosessing code.
   ts_folder is folderpath of prosessing data.
   freq_rule can be defined if there is more than one measuring frequency in ts_folder. Use frequency you want to use as an argument here.
   cod is value for cod filter. Bigger number means smoother curve.
   nper is length of prosessing window. Biggger number means more smooth curve and longer prosessing time.
   overlap is overlap between prosessing windows.
   min_factor defines how low periods are used. Smaller mumber means lower periods.
   max_factor defines hoq high periods are used. Bigger number means higher periods.
   freqs is amount of different frequencies used in prosessing.
   Have fun ;)
   """
    
    #reading site and makeing simplesite object
    site=simplesite(ts_folder, freq_rule=freq_rule)
    site.cod=cod
    site.nper=nper
    site.overlap=overlap
    site.min_factor=min_factor
    site.max_factor=max_factor
    site.freq_amount=freqs
    
    #preparing prosessing
    site.prepare_signalset()
    site.cut_timeseries()
    site.calculate_freqs(min_factor=min_factor, max_factor=max_factor, freqs=freqs)
    
    print(site.signalset)#print info about used dataset
    
    #actual prosessing
    site.ImpME = rb.utils.impedance(site.signalset, site.freqs, weights= mest_weights,prefilter=cod_filter(cod),
                                    fourier_opts=dict( Nper= nper,  overlap=overlap))
    
    #plotting results
    fig=plot_response(site)
    return(fig)