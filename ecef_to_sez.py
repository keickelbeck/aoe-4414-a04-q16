# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Converts the ECEF vector to the SEZ vector

# Parameters:
#  o_x_km: x-component of the ECEF origin of the SEZ frame in km
#  o_y_km: y-component of the ECEF origin of the SEZ frame in km
#  o_z_km: z-component of the ECEF origin of the SEZ frame in km
#  x_km: x-component of the ECEF vector in km
#  y_km: y-component of the ECEF vector in km
#  z_km: z-component of the ECEF vector in km
#  
# Output:
#  Prints the SEZ s-component (km), SEZ e-component (km), and SEZ z-component (km)
#
# Written by Kristin Eickelbeck
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.1363
E_E = 0.081819221456

# helper functions

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# initialize script arguments
o_x_km = float('nan') #x-component of the ECEF origin of the SEZ frame in km
o_y_km = float('nan') #y-component of the ECEF origin of the SEZ frame in km
o_z_km = float('nan') #z-component of the ECEF origin of the SEZ frame in km
x_km = float('nan') #x-component of the ECEF vector in km
y_km = float('nan') #y-component of the ECEF vector in km
z_km = float('nan') #z-component of the ECEF vector in km

# parse script arguments
if len(sys.argv)==7:
   o_x_km = float(sys.argv[1])
   o_y_km = float(sys.argv[2])
   o_z_km = float(sys.argv[3])
   x_km = float(sys.argv[4])
   y_km = float(sys.argv[5])
   z_km = float(sys.argv[6])

else:
   print(\
    'Usage: '\
    'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
   )
   exit()

# write script below this line
r_x_ecef = x_km - o_x_km  #ECEF x-componenet from SEZ origin
r_y_ecef = y_km - o_y_km  #ECEF y-componenet from SEZ origin
r_z_ecef = z_km - o_z_km  #ECEF z-componenet from SEZ origin

#find lat and long of SEZ origin by converting o_ECEF to LLH
# calculate longitude
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E


#rotations
s_km = r_x_ecef*math.cos(lon_rad)*math.sin(lat_rad) + r_y_ecef*math.sin(lon_rad)*math.sin(lat_rad) - r_z_ecef*math.cos(lat_rad)
e_km = -r_x_ecef*math.sin(lon_rad) + r_y_ecef*math.cos(lon_rad)
z_km = r_x_ecef*math.cos(lon_rad)*math.cos(lat_rad) + r_y_ecef*math.sin(lon_rad)*math.cos(lat_rad) + r_z_ecef*math.sin(lat_rad)

print(s_km)
print(e_km)
print(z_km)








