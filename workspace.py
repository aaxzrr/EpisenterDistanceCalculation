import numpy as np
from gmplot import gmplot
import webbrowser
from datetime import datetime
import pandas as pd
from IPython.display import display
class calculate_distance ():
    def __init__ (self, latitude_e, longtitude_e, latitude_s, longtitude_s):
        self.latitude_e   = latitude_e
        self.longtitude_e = longtitude_e
        self.latitude_s   = latitude_s 
        self.longtitude_s = longtitude_s
    
    def conver_to_decimal(self,coordinate_lan_lon):
        coordinate = coordinate_lan_lon.replace(" ", "")
        deg = int(coordinate[:coordinate.find('°')])
        min = int(coordinate[coordinate.find('°')+1:coordinate.find("'")])
        sec = float(coordinate[coordinate.find("'")+1:coordinate.find('"')-1])
        direc = coordinate[coordinate.find('"')+1:]
        
        decimal_degrees = deg + min/60 + sec/3600
        if direc in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        return decimal_degrees
        
    def conv_geografis_lan(self, latitude):
        tan_lanc = 0.993277*np.tan(np.radians(latitude))
        lanc = np.degrees(np.arctan(tan_lanc))
        return tan_lanc,lanc
    
    def vektor_epi_sta(self,latitude,longtitude):
        tan, lan = self.conv_geografis_lan(latitude)
        a = np.cos(np.radians(lan))*np.cos(np.radians(longtitude))
        b = np.cos(np.radians(lan))*np.sin(np.radians(longtitude))
        c = np.sin(np.radians(lan))
        return a,b,c
    
    def delta(self):
        a_e,b_e,c_e = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_e), 
                                          self.conver_to_decimal(self.longtitude_e))  
        a_s,b_s,c_s = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_s), 
                                          self.conver_to_decimal(self.longtitude_s))  
        cos_delta = (a_s*a_e)+(b_s*b_e)+(c_s*c_e)
        delta_cos = np.degrees(np.arccos(cos_delta))
        delta_km = delta_cos*111.11
        return cos_delta,delta_cos,delta_km
    
    def azimut(self):
        long_s=self.conver_to_decimal(self.longtitude_s)
        long_e=self.conver_to_decimal(self.longtitude_e)
        tan, lan_s = self.conv_geografis_lan(self.conver_to_decimal(self.latitude_s))
        tan, lan_e = self.conv_geografis_lan(self.conver_to_decimal(self.latitude_e))
        cos_delta,cos,km= self.delta()
        a_sin = np.degrees(np.arcsin((np.sin(np.radians(long_s-long_e))*
                                      np.sin(np.radians(90-lan_s)))/np.sin(np.radians(cos))))
        a_cos = np.degrees(np.arccos((np.cos(np.radians(90-lan_s))-cos_delta*
                                      np.cos(np.radians(90-lan_e)))/(np.sin(np.radians(cos))*np.sin(np.radians(90-lan_e)))))
        
        if lan_e < lan_s and long_e < long_s:
            a_real_sin = -a_sin
            a_real_cos = a_cos
            if a_real_cos == a_real_sin:
                a_real = a_real_cos
                b_azimut = 180+a_real
            return a_sin, a_cos, a_real, b_azimut
        if lan_e < lan_s and long_e > long_s:
            a_real_sin = 360 - (-a_sin)
            a_real_cos = 360 - (a_cos)
            if a_real_cos == a_real_sin:
                a_real = a_real_cos
                b_azimut = a_real-180
            return a_sin, a_cos, a_real, b_azimut
        if lan_e > lan_s and long_e > long_s:
            a_real_sin = 180 + (-a_sin)
            a_real_cos = 180 + (a_cos)
            if a_real_cos == a_real_sin:
                a_real = a_real_cos
                b_azimut = a_real-180
            return a_sin, a_cos, a_real, b_azimut
        if lan_e > lan_s and long_e < long_s:
            a_real_sin = 180 - (-a_sin)
            a_real_cos = 180 - (a_cos)
            if a_real_cos == a_real_sin:
                a_real = a_real_cos
                b_azimut = 180+a_real
            return a_sin, a_cos, a_real, b_azimut
        else:
            pass
        
    def create_map(self):
        station_lan = [self.conver_to_decimal(self.latitude_s)]
        station_long = [self.conver_to_decimal(self.longtitude_s)]
        episentrum_lan = [self.conver_to_decimal(self.latitude_e)]
        episentrum_long = [self.conver_to_decimal(self.longtitude_e)]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")  # Waktu saat ini sebagai string
        html_file = f'seismic_stations_map_{timestamp}.html'
        
        gmap = gmplot.GoogleMapPlotter(station_lan[0], station_long[0], 2)

        for lat, lon in zip(station_lan, station_long):
            gmap.marker(lat, lon, title="Station", color="blue")

        for lat, lon in zip(episentrum_lan, episentrum_long):
            gmap.marker(lat, lon, title="Episentrum", color="red")

        gmap.draw(html_file)
        webbrowser.open(html_file)
        
    def collect_results(self):
        a_sin, a_cos, a_real, b_azimut = self.azimut()
        cos_delta,delta_cos,delta_km = self.delta()
        vektor_epi_sta_e = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_e), 
                                               self.conver_to_decimal(self.longtitude_e))
        vektor_epi_sta_s = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_s), 
                                               self.conver_to_decimal(self.longtitude_s))
        tan_lanc_e, lanc_e = self.conv_geografis_lan(self.conver_to_decimal(self.latitude_e))
        tan_lanc_s, lanc_s = self.conv_geografis_lan(self.conver_to_decimal(self.latitude_s))
        station_lan = self.conver_to_decimal(self.latitude_s)
        station_long = self.conver_to_decimal(self.longtitude_s)
        episentrum_lan = self.conver_to_decimal(self.latitude_e)
        episentrum_long = self.conver_to_decimal(self.longtitude_e)
        
        convertion = {
            'Titik':['Episenter', 'Stasiun'],
            'Latitude':[episentrum_lan,station_lan],
            'Longitude':[episentrum_long,station_long],
            'Tan Geografis Lats': [tan_lanc_e,tan_lanc_s],
            'Geografis Lats': [lanc_e,lanc_s],
            'A': [vektor_epi_sta_e[0],vektor_epi_sta_s[0]],
            'B': [vektor_epi_sta_e[1],vektor_epi_sta_s[0]],
            'C': [vektor_epi_sta_e[2],vektor_epi_sta_s[2]],
        }
        azimut = {
            'Azimut Sin': [a_sin],
            'Azimut cos': [a_cos],
            'Azimut Real': [a_real],
            'Back Azimut': [b_azimut]
        }
        delta = {
            'Cos Delta': [cos_delta],
            'Delta': [delta_cos],
            'Delta (km)': [delta_km]
        }
        
        display(pd.DataFrame(convertion))
        display(pd.DataFrame(azimut))
        display(pd.DataFrame(delta))

        