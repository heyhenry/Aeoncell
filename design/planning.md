Wireframes Plan (Aeoncell): 

Register: 
	widgets:
		- app name (text)
		- register account(text)
		- username subtitle (text)
		- enter username (entry)
		- password subititle (text)
		- enter new password (entry)
		- confirm password subtitle (text)
		- confirm new password (entry)
		- error message (text)
		- register (button)
		- image on the right side of the window (image)

Login: 
	- widgets:
		- app name (text)
		- log in (text)
		- enter password (text)
		- password field (entry)
		- error message (text)
		- login (button)
		- forget password? (actonable text)
		- image on the left side of the window (image)

Dashboard:
	- features (potential and concrete)
		- vertical navbar
			- app  icon
			- icon and text for each page
				- dashboard/home
				- graphs
				- entry page (entry page will have a toggleable sliding button to switch between single and session entry)
				- achievements page
				- discover page 
				- settings page 
		- top center 
			- "Hello, username123"
			- quiet motivational quote (changes each login) (i.e. "Keep Moving, Stay Healthy")(below the "Hello" message)
				- ensure word limit
			- today's date
			- bell icon (next to "today's date")
				- can be used as a news/tips feed (use api and get small snippets of useful advice, info about nutrition, exercise, etc)
				- OR reminders/tasks in the form of a popup dialog box showing tasks to do with progress bars? 
		- profile card (stretches same length or alittle less than the vert navbar and situated on the right side of the window)
			- user profile image
			- full user name
			- potentially profession?
			- height
			- weight
			- age
			- monthly goals
				- sleep (i.e. 100 / 300 hours)
				- steps (i.e. 2,000 / 100,000 steps)
				- lose/gain weight (i.e. 3 / 6 kilos)
			- badge showcase? (latest 3)
		(**scrollable frame encompassing features** -> solution to the minimal window size mandate)
		- daily hydration tracker
		- daily steps tracker
		- daily sleep tracker
		- weather forecast
		- popular workouts (trending)
		- daily stats
		- badges
		- latest exercise entries
		- add an exercise entry / add an exercise session entry
		
Settings: 
	- Updateable fields
		- user image
		- Username
		- Full name
			- First name
			- Last name
		- current weight
		- goal weight
		- daily step goal
		- daily hydration goal
		- daily sleep goal 
		- current password
		- new password 
		- height 
		- age
		
stats:
	- tbd how but
	- charts/graphs on steps 
	- charts/graphs on exercise
	- charts/graphs on weight
	- charts/graphs on hydration
	- charts/graphs on sleep
	- more hopefully
	
achievements: 
	- list of all the achieveable badges and how
		- greyed out if not achieved
		- coloured if achieved
	- badges info:
		- name of achievements
		- desc of achievement
		- date achieved
		- progress bars
		
entry: 
	- single and session will have same form field, with slight differences in behaviour
		- i.e. session field will retain label input for each next entry instance in a session (since it could be: evening gym session, etc (to help group))
	- toggleable sliding button on the top right to switch between single and session entry pages
	- already worked on so no need to detail (may detail later for record keeping though)
	
discover: 
	- each point below in their respect section boxes or containers:
		- potentially showcase places to hike (source of knowledge)
		- nearest gyms and activity centers (source of knowledge, motivation)
		- potential events near you (source of knowledge, inspiration, motivation)
		- new workouts or latest trending workouts (source of knowledge, motivation, inspiration)
		- trending nutrition advice (source of knowledge)
		- cool achievements by fitness and alike athletes (source of motivation)
	