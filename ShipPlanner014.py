# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import math
import bpy_extras.io_utils
import os

bl_info = {
	"name": "Pioneer Ship Planner",
	"author": "Szilard Balint (nozmajner)",
	"version": (0,1,4),
	"blender": (2, 70, 0),
	"location": "Properties -> Scene -> Ship Planner",
	"description": "Calculates ship stats for Pioneer Space Simulator",
	"warning": "",
	"wiki_url": "N/A",
	"tracker_url": "N/A",
	"category": "Scene"}

gee = 9.81
def sum_mass(hull, fuel, cap, cargo_cap):	
	result = [hull+fuel+cap, hull+fuel, hull+fuel+cargo_cap] 
	return result

def acc(mass, thrust):
	acc_full = (thrust/mass[0]/gee) #mass*1000 volt
	acc_empty = (thrust/mass[1]/gee)
	
	if acc_full <= 0.0001:
		result_full = "<0.0001"
	else:
		result_full = acc_full
	
	if acc_empty <= 0.0001:
		result_empty = "<0.0001"
	else:
		result_empty = acc_empty
		
	result = [result_full, result_empty]
		
	return result

def deltav(ev, mass, fuel_cap):
	dv = (float(ev))*(math.log(float(mass+fuel_cap)/mass))
	if dv <=0.0001:
		result = "<0.0001"
	else:
		result = dv
	return result


 #Operator example
class VesselExport(bpy.types.Operator): # , bpy_extras.io_utils.ExportHelper .ExportHelper feldobja az export ablakot, ha megnyomom a gombot
	"""Export shipdef.lua"""
	bl_idname = "object.simple_operator"
	bl_label = "Export shipdef"
	filename_ext = ".lua"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		print("Krumpli") 
		scene = bpy.data.scenes["Scene"]
#		file = open(filepath, 'w', encoding="ansi", newline = "\n")
		file = open(os.path.splitext(bpy.data.filepath)[0] + ".lua", 'w', newline = "\n")
		fw = file.write
		fw("-- Copyright © 2008-2014 Pioneer Developers. See AUTHORS.txt for details \n-- Licensed under the terms of CC-BY-SA 3.0. See licenses/CC-BY-SA-3.0.txt\n-- Generated with Pioneer Ship Planner Blender Addon\n\n")
		# writing define
		fw("define_ship {\n")
		#writing ship data
		fw("\tname = '" + scene.ShipName + "',\n")
		fw("\tship_class = '" + scene.ShipClass + "',\n")
		fw("\tmanufacturer = '" + scene.ManufacturerName + "',\n")
		fw("\tmodel = '" + scene.ModelName + "',\n")
		fw("\tprice = " + str(scene.Price) + ",\n")
		fw("\n")
		fw("\tforward_thrust = " + str(int(scene.FWD*1000)) + ",\n")
		fw("\treverse_thrust = " + str(int(scene.BWD*1000)) + ",\n")
		fw("\tup_thrust = " + str(int(scene.UP*1000)) + ",\n")
		fw("\tdown_thrust = " + str(int(scene.DWN*1000)) + ",\n")
		fw("\tleft_thrust = " + str(int(scene.LEFT*1000)) + ",\n")
		fw("\trigh_thrust = " + str(int(scene.RIGHT*1000)) + ",\n")
		fw("\tangular_thrust = " + str(int(scene.ANG*1000)) + ",\n")
		# mass and capacity
		fw("\n")
		fw("\thull_mass = " + str(scene.HullMass) + ",\n")
		fw("\tfuel_tank_mass = " + str(scene.FuelMass) + ",\n")
		fw("\tcapacity = " + str(scene.Capacity) + ",\n")
		if scene.Capacity > scene.CargoCap:	
			fw("\tmax_cargo = " + str(scene.CargoCap) + ",\n")
		else:
			fw("\tmax_cargo = " + str(scene.Capacity) + ",\n")
		fw("\tmin_crew = " + str(scene.Min_crew) + ",\n")
		if scene.Max_crew < scene.Min_crew:
			fw("\tmax_crew = " + str(scene.Min_crew) + ",\n")
		else:
			fw("\tmax_crew = " + str(scene.Max_crew) + ",\n")
		if scene.Cabin != 50:
			fw("\tmax_cabin = " + str(scene.Cabin) + ",\n")
		# engines
		fw("\n")
		fw("\thyperdrive_class = " + str(scene.Hyperdrive) + ",\n")
		if scene.Max_Engine < scene.Hyperdrive:
			fw("\tmax_engine = " + str(scene.Hyperdrive) + ",\n")
		else:
			fw("\tmax_engine = " + str(scene.Max_Engine) + ",\n")
		fw("\teffective_exhaust_velocity = " + str(int(scene.EV*1000)) + ",\n")
		# equipment
		fw("\n")
		fw("\tmax_laser = " + str(scene.Max_laser) + ",\n")
		fw("\tmax_missile = " + str(scene.Max_missile) + ",\n")
		if scene.Lasercooler != 1:
			fw("\tmax_lasercooler = 0,\n")
		if scene.Fuelscoop != 1:
			fw("\tmax_fuelscoop = 0,\n")
		if scene.Cargoscoop != 1:
			fw("\tmax_cargoscoop = 0,\n")
		if scene.Shield != 9999:
			fw("\tmax_shield = " + str(scene.Shield) + ",\n")
		if scene.Scanner != 1:
			fw("\tmax_scanner = 0,\n")
		if scene.Radarmapper != 1:
			fw("\tmax_radarmapper = 0,\n")
		if scene.Hypercloud != 1:
			fw("\tmax_hypecloud = 0,\n")
		if scene.Max_ecm != 1:
			fw("\tmax_ecm = 0,\n")
		if scene.Atmoshield != 1:
			fw("\tmax_atmoshield = 0,\n")
		if scene.Cargolifesupport != 1:
			fw("\tmax_cargolifesupport = 0,\n")
		if scene.Autopilot != 1:
			fw("\tmax_autopilot = 0,\n")
		fw("}")
		file.close()
		
		return {'FINISHED'}
	

class ShipPlanner(bpy.types.Panel):
		"""Ship stats planner utility for Pioneer"""
		bl_idname = "ShipPlanner"
		bl_label = "Ship Planner"			   
		bl_space_type = 'PROPERTIES'
		bl_region_type = 'WINDOW'
		bl_context = 'scene'
		#bl_options = { 'UNDO'}
			
		def draw(self, context):
			layout = self.layout
			scn = bpy.context.scene 
			scene = bpy.data.scenes["Scene"]
			
			#row_init = layout.row()			
			#row_init.operator("InitProps.bl_idname", text = "InitProps.bl_label")

			ship_box = layout.box()
			ship_box.label("Ship", icon = "AUTO")
			row_name = ship_box.row()
			row_name.prop(scn, 'ShipName', text = "Name")	#, '["Name"]')
			row_model = ship_box.row()
			row_model.prop(scn, 'ModelName')
			row_manufacturer = ship_box.row()
			row_manufacturer.prop( scn, 'ManufacturerName')
			row_class = ship_box.row()
			row_class.prop( scn, 'ShipClass')
			row_price = ship_box.row()
			row_price.prop(scn, 'Price')
			
			row_crew = ship_box.row()
			row_crew.prop(scn, 'Min_crew')
			row_crew.prop(scn, 'Max_crew')
			
			mass_box = layout.box()
			mass_box.label("Masses (t)", icon = "OBJECT_DATA")
			row_hull = mass_box.row()
			#row_hull.label("Hull mass")
			row_hull.prop(scn, 'HullMass')
			row_hull.prop(scn, 'FuelMass', text = "Fuel mass")
			
			row_cap = mass_box.row()
			#row_cap.label("Capacity")
			row_cap.prop(scn, 'Capacity')
			row_cap.prop(scn, 'CargoCap', text = "Cargo cap")
	
			mass = sum_mass(scene.HullMass, scene.FuelMass, scene.Capacity, scn.CargoCap) # calculate ship mass  
			row_masses = mass_box.row()
			row_masses.label(str("Full mass: " + str(mass[0]) + "t"))
			row_masses.label(str("Empty mass: " + str(mass[1]) + "t"))
			row_masses.label(str("Cargo mass: " + str(mass[2]) + "t"))
											
			########
			thr_box = layout.box()
			thr_box.label("Thrust (kN)", icon = "LAMP_SPOT")

			row1 = thr_box.row(align = True)
			#row1.label("Longitudal")
			row1.prop(scn, 'FWD', text = "fwd")
			row1.prop(scn, 'BWD', text = "bwd")
			
			row2 = thr_box.row(align = True)
			#row2.label("Acceleration:")
			acc_fwd = acc(mass, scene.FWD)
			acc_bwd = acc(mass, scene.BWD)
			row2.label("F: " + str(acc_fwd[0])[0:6] + " G / E: " + str(acc_fwd[1])[0:6] +" G")
			row2.label("F: " + str(acc_bwd[0])[0:6] + " G / E: " + str(acc_bwd[1])[0:6] +" G")

			row3 = thr_box.row(align = True)
			#row3.label("Vertical")
			row3.prop(scn, 'UP', text = "up")
			row3.prop(scn, 'DWN',text = "down")
			
			row4 = thr_box.row(align = True)
			#row4.label("Acceleration:")
			acc_up = acc(mass, scene.UP)
			acc_down = acc(mass, scene.DWN)
			row4.label("F: " + str(acc_up[0])[0:6] + " G / E: " + str(acc_up[1])[0:6] +" G")
			row4.label("F: " + str(acc_down[0])[0:6] + " G / E: " + str(acc_down[1])[0:6] +" G")
			
			row5 = thr_box.row(align = True)
			#row5.label("Horizontal")
			row5.prop(scn, 'LEFT', text = "left")
			row5.prop(scn, 'RIGHT', text = "right")
			
			row6 = thr_box.row(align = True)
			#row6.label("Acceleration:")
			acc_left = acc(mass, scene.LEFT)
			acc_right = acc(mass, scene.RIGHT)
			row6.label("F: " + str(acc_left[0])[0:6] + " G / E: " + str(acc_left[1])[0:6] +" G")
			row6.label("F: " + str(acc_right[0])[0:6] + " G / E: " + str(acc_right[1])[0:6] +" G")
			
			row7 = thr_box.row(align = True)
			#row5.label("Angular")
			row7.prop(scn, 'ANG', text = "angular")
			########									
			thr_box = layout.box()
			thr_box.label("Efficiency", icon = "IPO")

			row_EV = thr_box.row(align = True)
			row_EV.label("Exhaust velocity (km/s):")
			row_EV.prop(scn, 'EV', text = "ev")
			row_deltaV = thr_box.row(align = True)
			row_deltaV.label("DeltaV:")
			
			row_empty = thr_box.row(align = True)		   
			deltav_empty = deltav(scene.EV, scene.HullMass, scene.FuelMass)		 
			row_empty.label("Empty: " + str(deltav_empty)[0:10] + " km/s")

			row_full = thr_box.row(align = True)
			deltav_full = deltav(scene.EV, (scene.HullMass+scene.Capacity), scene.FuelMass)
			row_full.label("Full: " + str(deltav_full)[0:10] + " km/s")			

			row_maximum = thr_box.row(align = True)
			deltav_max = deltav(scene.EV, scene.HullMass, (scene.FuelMass+scene.CargoCap))
			row_maximum.label("Max: " + str(deltav_max)[0:10] + " km/s")
   
			 ###########			
			
			equip_box = layout.box()
			equip_box.label("Equipment mounts", icon = "PLUGIN")
			
			row_hyperdrive = equip_box.row(align = True)
			row_hyperdrive.prop(scn, 'Hyperdrive', text = "Hyperdrive")
			row_hyperdrive.prop(scn, 'Max_Engine', text = "Max")
			
			row_wep = equip_box.row(align = True)
			row_wep.prop(scn, 'Max_laser', text = "Max laser")
			row_wep.prop(scn, 'Max_missile', text = "Max missile")
			
			row_cooling = equip_box.row(align = True)
			row_cooling.prop(scn, 'Lasercooler', text = "Laser cooling Booster")
			
			row_scoop = equip_box.row(align = True)
			row_scoop.prop(scn, 'Fuelscoop', text = "Fuel scoop")
			row_scoop.prop(scn, 'Cargoscoop', text = "Cargo scoop")
	
			row_scanner = equip_box.row(align = True)
			row_scanner.prop(scn, 'Scanner', text = "Scanner")
			row_scanner.prop(scn, 'Radarmapper', text = "Radar Mapper")
			
			row_hypercloud = equip_box.row(align = True)
			row_hypercloud.prop(scn, 'Hypercloud', text = "Hypercloud analyzer")
			
			row_ecm = equip_box.row(align = True)
			row_ecm.prop(scn, 'Max_ecm', text = "ECM")
			
			row_atmoshield = equip_box.row(align = True)
			row_atmoshield.prop(scn, 'Atmoshield', text = 'Atmo shielding')
			
			row_shield = equip_box.row(align = True)
			row_shield.prop(scn, 'Shield', text = 'Max Shield')
			row_shield.prop(scn, 'Energybooster', text = 'Energy Booster')
			
			row_cabin = equip_box.row(align = True)
			row_cabin.prop(scn, 'Cabin', text = 'Max Passenger Cabin')
			
			row_cargolife = equip_box.row(align = True)
			row_cargolife.prop(scn, 'Cargolifesupport', text = 'Cargo bay Life support')
			
			row_autopilot = equip_box.row(align = True)
			row_autopilot.prop(scn, 'Autopilot', text = 'Autopilot')
			
			row_autorepair = equip_box.row(align = True)
			row_autorepair.prop(scn, 'Autorepair', text = 'Hull Autorepair system')
			
			############################
			
			vessel_export = layout.box()
			vessel_export.label("Export", icon = "EXPORT")
			
			exportrow = vessel_export.row(align = True)
			exportrow.operator("object.simple_operator", text = "Export")
			
			
			
			

#class InitProps(bpy.types.Operator):
#   """Tooltip"""
#   bl_idname = "scene.init_my_prop"
#   bl_label = "Init properties"
#   
#   @classmethod
#	def poll(cls, context):
#		return context.scene
#   def execute(self, context):
#	   if context.scene.Capacity != 1:
#		   context.scene.Capacity = 1
#	   return {'FINISHED'}
		
	
#Registering the operator
			   
def register():	
	bpy.utils.register_class(ShipPlanner)
	bpy.utils.register_class(VesselExport)

	bpy.types.Scene.Valami = bpy.props.FloatProperty(   #ezzel hozom letre, tobbi feljebb
		name = "Valami",
		default = 0.0,
		description = "Ez bizony mar valami") 
	
	#######Ship box######
	bpy.types.Scene.ShipName = bpy.props.StringProperty(
		name = "Ship Name",
		default = "name",
		description = "Name of the ship, displayed in the game.")
	
	bpy.types.Scene.ManufacturerName = bpy.props.StringProperty(
		name = "Manufacturer",
		default = "opli",
		description = "Manufacturer, for logo selection. Valid values are the file names in the icons/manufacturers folder - without extension")


	bpy.types.Scene.ShipClass = bpy.props.StringProperty(
		name = "Ship class",
		default = "light_courier",
		description = "Ship class, for class icon display in the ship marker. Valid values are in the icons/shipclass folder")

	bpy.types.Scene.ModelName = bpy.props.StringProperty(
		name = "Model file",
		default = "model",
		description = "Name of the model file to be used. They are in the data/models/ folder")
	
	bpy.types.Scene.Price = bpy.props.IntProperty(
		name = "Price",
		default = 1,
		min = 1,
		description = "Base price of the ship.")
	
	bpy.types.Scene.Min_crew = bpy.props.IntProperty(
		name = "Min crew",
		default = 1,
		min = 1,
		description = "Minimum crew capacity of the ship.")
		
	bpy.types.Scene.Max_crew = bpy.props.IntProperty(
		name = "Max crew",
		default = 1,
		min = 1,
		description = "Maximum crew capacity of the ship.")


	#######Masses box######
	bpy.types.Scene.HullMass = bpy.props.IntProperty(
		name = "Hull mass",
		default = 1,
		min = 1,
		max = 1000000000,
		description = "Mass of the hull in tonnes.")
		
	bpy.types.Scene.FuelMass = bpy.props.IntProperty(
		name = "Fuel tank mass",
		default = 1,
		min = 1,
		max = 1000000000,
		description = "Capacity of the fuel tank in tonnes.")
		
	bpy.types.Scene.Capacity = bpy.props.IntProperty(
		name = "Capacity",
		default = 1,
		min = 1,
		max = 1000000000,
		description = "Equipment and cargo capacity of the ship in tonnes.")
		
	bpy.types.Scene.CargoCap = bpy.props.IntProperty(
		name = "Cargo capacity",
		default = 1,
		min = 1,
		max = 1000000000,
		description = "Cargo capacity in tonnes.")
	
	#######Thrust box#######
	bpy.types.Scene.FWD = bpy.props.FloatProperty(
		name = "FWD thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Forward thrust in kN's") 
		
	bpy.types.Scene.BWD = bpy.props.FloatProperty(
		name = "BWD thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Backward thrust in kN's") 
		
	bpy.types.Scene.UP = bpy.props.FloatProperty(
		name = "UP thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Upward thrust in kN's") 
		
	bpy.types.Scene.DWN = bpy.props.FloatProperty(
		name = "DOWD thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Downward thrust in kN's") 
		
	bpy.types.Scene.LEFT = bpy.props.FloatProperty(
		name = "LEFT thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Leftward thrust in kN's") 
		
	bpy.types.Scene.RIGHT = bpy.props.FloatProperty(
		name = "RIGHT thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Rightward thrust in kN's") 
		
	bpy.types.Scene.ANG = bpy.props.FloatProperty(
		name = "ANG thrust",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Angular thrust in kN's") 
		
	##########Efficiency box#########
	bpy.types.Scene.EV = bpy.props.FloatProperty(
		name = "ev",
		default = 1.0,
		min = 1.0,
		max = 1000000000.0,
		description = "Exhaust velocity in km/s") 
		
	##########Equipments#############
	bpy.types.Scene.Hyperdrive = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 13,
		description = "Default hyperdrive class.")

	bpy.types.Scene.Max_Engine = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 13,
		description = "Maximum hyperdrive class. 0 for no hyperspace capability")
		
	bpy.types.Scene.Max_laser = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 2,
		description = "Maximum number of cannons")
	
	bpy.types.Scene.Max_missile = bpy.props.IntProperty(
		default = 0,
		min = 0,
		max = 1000,
		description = "Maximum number of missiles")

	bpy.types.Scene.Fuelscoop = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Fuel scoop compatibility")

	bpy.types.Scene.Cargoscoop = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Cargo scoop compatibility.") 
	
	bpy.types.Scene.Max_ecm = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "ECM compatibility.") 
	
	bpy.types.Scene.Scanner = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Scanner compatibility.") 
		
	bpy.types.Scene.Radarmapper = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Radar mapper compatibility.")
		
	bpy.types.Scene.Hypercloud = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Hypercloud analyzer compatibility.")	 
	
	bpy.types.Scene.Autorepair = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Hull Autorepair sys compatibility.")	
		
	bpy.types.Scene.Energybooster = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Energy booster compatibility.")  
		
	bpy.types.Scene.Atmoshield = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Atmospheric shielding compatibility. Ships without it can't land or be bought on surface bases") 
		
	bpy.types.Scene.Cabin = bpy.props.IntProperty(
		default = 50,
		min = 0,
		max = 50,
		description = "Passenger cabin compatibility and max amount.")  
		
	bpy.types.Scene.Shield = bpy.props.IntProperty(
		default = 9999,
		min = 0,
		max = 9999,
		description = "Shield compatibility and max amount.")   
		
	bpy.types.Scene.Lasercooler = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Laser cooling booster compatibility.")
		
	bpy.types.Scene.Cargolifesupport = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Cargo bay life support compatibility.")  
		
	bpy.types.Scene.Autopilot = bpy.props.IntProperty(
		default = 1,
		min = 0,
		max = 1,
		description = "Autopilot compatibility.")   
	
			
def unregister():
	bpy.utils.unregister_class(ShipPlanner)
	del bpy.types.Scene.ShipName
	del bpy.types.Scene.ModelName
	del bpy.types.Scene.ManufacturerName
	del bpy.types.Scene.ShipClass
	del bpy.types.Scene.Price
	del bpy.types.Scene.HullMass
	del bpy.types.Scene.FuelMass
	del bpy.types.Scene.Capacity
	del bpy.types.Scene.CargoCap
	del bpy.types.Scene.FWD
	del bpy.types.Scene.BWD
	del bpy.types.Scene.UP
	del bpy.types.Scene.DWN
	del bpy.types.Scene.LEFT
	del bpy.types.Scene.RIGHT
	del bpy.types.Scene.ANG
	del bpy.types.Scene.EV
	del bpy.types.Scene.Hyperdrive
	del bpy.types.Scene.Max_engine
	del bpy.types.Scene.Max_laser
	del bpy.types.Scene.Max_missile
	del bpy.types.Scene.Fuelscoop
	del bpy.types.Scene.Cargoscoop
	del bpy.types.Scene.Max_ecm
	del bpy.types.Scene.Scanner
	del bpy.types.Scene.Radarmapper
	del bpy.types.Scene.Hypercloud
	del bpy.types.Scene.Autorepair
	del bpy.types.Scene.Energybooster
	del bpy.types.Scene.Atmoshield
	del bpy.types.Scene.Cabin
	del bpy.types.Scene.Shield
	del bpy.types.Scene.Lasercooler
	del bpy.types.Scene.Cargolifesupport
	del bpy.types.Scene.Autopilot
	
			
if __name__ == "__main__":
	register()