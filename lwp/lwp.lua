-- Copyright © 2008-2013 Pioneer Developers. See AUTHORS.txt for details
-- Licensed under the terms of CC-BY-SA 3.0. See licenses/CC-BY-SA-3.0.txt

define_ship {
	name='Light Weapons Platform',
	model='lwp',
	forward_thrust = 25e5,
	reverse_thrust = 25e5,
	up_thrust = 1e5,
	down_thrust = 1e5,
	left_thrust = 1e5,
	right_thrust = 1e5,
	angular_thrust = 90e5,
	camera_offset = v(0,0,0),
	gun_mounts =
	{
		{ v(0,0,0), v(0,0,0), 0, 'HORIZONTAL' },
	},
	max_cargo = 3,
	max_laser = 1,
	max_missile = 2,
	max_cargoscoop = 0,
	max_fuelscoop = 0,
	capacity = 3,
	hull_mass = 1,
	fuel_tank_mass = 1,
	thruster_fuel_use = 0.5,
	price = 10000,
	hyperdrive_class = 0,
	max_engine = 0,
	max_ecm = 0, 
	max_scanner = 0, 
	max_radarmapper = 0, 
	max_hypercloud = 0, 
	max_hullautorepair = 0, 
	max_energybooster = 0, 
	max_atmoshield = 0, 
	max_fuelscoop = 0, 
	max_lasercooler = 0, 
	max_cargolifesupport = 0, 
	max_autopilot = 0,
	max_shield = 0,
	max_cabin = 0,
}