#!python3
#Description of piping used in the system
from natu.units import inch, ft, m, cm
Piping = [{'ID':1*inch,
			'OD':1*inch,
			'L':150*inch,
			'VJ':2.5,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':True, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':16*inch,
			'VJ':2.5,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':64*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':60*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':173*inch,
			'VJ':2.5,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':50.75*inch,
			'VJ':2*inch,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'OD':1*inch,
			'ID':1*inch,
			'L':18*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':True, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':155*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'SCH':5,
			'L':64*inch,
			'VJ':2*inch,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'OD':1*inch,
			'ID':1*inch,
			'L':83*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':True, #Corrugated or straight
			},
			
			{'D_nom':1,
			'SCH':5,
			'L':15*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'type':'tube',
			'wall':0.049*inch,
			'L':30*inch,
			'VJ':2.5,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			{'D_nom':1,
			'type':'tube',
			'wall':0.049*inch,
			'L':13*inch,
			'VJ':2.5,
			'Orientation':'Horizontal', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},
			
			{'D_nom':1,
			'type':'tube',
			'wall':0.049*inch,
			'L':30*inch,
			'VJ':2.5,
			'Orientation':'Vertical', #Handles vertical and horizontal cases
			'Corrugated':False, #Corrugated or straight
			},

			

		]