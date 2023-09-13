import numpy as np
class calculate_distance ():
    def __init__ (self, latitude_e, longtitude_e, latitude_s, longtitude_s):
        self.latitude_e   = latitude_e
        self.latitude_s   = latitude_s
        self.longtitude_e = longtitude_e
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
        a_e,b_e,c_e = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_e), self.conver_to_decimal(self.longtitude_e))  # noqa: E501
        a_s,b_s,c_s = self.vektor_epi_sta(self.conver_to_decimal(self.latitude_s), self.conver_to_decimal(self.longtitude_s))  # noqa: E501
        delta = np.degrees(np.arccos((a_s*a_e)+(b_s*b_e)+(c_s*c_e)))*111.11
        return delta
    