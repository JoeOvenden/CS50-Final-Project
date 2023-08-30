# Interactive Educational Physics Website on the Laws of Motion
#### Video Demo: https://www.youtube.com/watch?v=otZPBmIoCY8&t=6s&ab_channel=JonathanOvenden
#### Description: The website contains a physics simulation designed to help students understand the meaning and implication of the laws of motion, an asteroid game and 4 lessons on some of the laws of motion.

&nbsp;
## **Physics Simulation /static/scripts/simulator.js**

### **General**

The simulation comprises a 2D display of a ball that can be picked up and thrown. The ball experiences the effects of gravity, drag, friction, buoyancy and loss of energy upon bouncing against a floor or wall.

The simulation has settings available to the user that can change the following properties:
- The strength of gravity
- The density of the fluid that the ball is in
- The density of the ball
- The coefficient of rolling friction of the ball against the floor
- The percentage of the ball's energy that is lost on it bounce against a surface
- The ball's radius with the option to keep either the density or mass constant

There are buttons which can:
- Pause the simulation
- Reset the simulation, meaning clear the chart, set the ball's velocities to 0 and it's position to the middle of the canvas. The time since the last reset is displayed below the simulation.
- Set the height of the ball. Doing so will also set the ball's velocities to 0 and optionally reset the simulation.

There also some checkboxes that change:
- Whether the ball should bounce on the ceiling, that is, should the simulation be bounded above.
- Whether the simulation will pause or not when the ball collides with a surface. The idea of this setting is to make it easier to experiment. An example would be if you wanted to see how long it took the ball to drop from a certain height with different fluid densities. With this setting toggled on it becomes much easier because the simulation will pause and you can then the time since last reset. 
- Whether the simulation should reset when the user sets the balls height.
As well as a toggle for whether the ball should bounce against the top border of the simulation, i.e. should there be a ceiling.

They also have the ability to change the simulation zoom. At default the simulation has a scale of 100 pixels: 1 metre and this can be changed with the zoom slider.

The simulation is rendered using the CanvasRenderingContext2D interface as part of the HTML Canvas API and the user changes settings via HTML input elements.

Simulation.js contains three classes: Simulation, InputHandler, Ball and Simulation.

&nbsp;&nbsp;
## **InputHandler Class**

InputHandler upon construction adds event listeners to all the html buttons and some to the window that look out for mouse actions.

&nbsp;&nbsp;
## **Ball Class**

The Ball class is used to create and handle the ball in the simulation. It has properties such as coordinates, velocities and accelerations for x and y, radius, mass, density, volume, a boolean determining whether the ball is being held by the user and a boolean determining whether the ball is at rest upon a surface.

Most of the properties of the ball are measured in SI units, for example the velocities are measured in metres per second, the mass in kilograms and so on, however the x and y coordinates are measured in pixels. To avoid frequent conversion between pixels and metres for the radius, radiusPixels holds the value of the radius measured in pixels and radiusMetres, the value in metres.

To convert a value from metres to pixels, Simulation.metresToPixels is used and to convert from pixels to metres, Simulation.pixelsToMetres is used.

The Ball class is the largest class due to the fact that most of the physics computations take place here.

### **Ball.surfaceAtRestOn**
It was useful to determine whether or not the ball is still dynamic in the y direction or whether or not it has come to an equilibrium resting upon a surface. For instance without this feature I ran into the problem that even when the ball seemingly came to rest upon a surface, it still displayed a nonzero y velocity due to it bouncing and experiencing gravity. 

With this feature added, when the ball is at rest upon a surface, it no longer bounces or experiences gravity, buoyancy or drag in the y direction, and it's y velocity will always be zero.

The ball is determined at rest upon a surface if for the last 10 frames the ball was within 1cm of the surface.

### **update()** 
update() is responsible for updating the ball's position, velocity and also it's physical properties that can be changed on the webpage and then drawing the ball to the canvas. It also calls the methods for checking whether the ball should be at rest upon a surface and for handling being grabbed by the user.

### **updatePos()**
updatePos() changes the ball's x and y coordinates according to it's velocities. Note that the velocities are in metres per second where as x and y are in pixels so first the velocities must be converted to pixels per second. 

### **updateVelocity()** 
updateVelocity() calls the methods required for handling gravity, buoyancy, drag, friction and bouncing. 

The velocity values before updateVelocity has processed are stored and these are then used to calculate the acceleration that happened in that frame, which are then stored to be optionally displayed but the chart. 

Also calculating drag and friction uses the previous velocity values.

### **grab()**
grab() moves the ball to where the user's mouse is, ensures that it does not go inside any walls, and stores the ball's position to be used upon release to calculate velocity.

### **checkOnSurface()**
checkOnSurface() checks whether the ball should be considered as at rest upon a surface as detailed above under Ball.surfaceAtRestOn.

### **draw()**
Draws the ball on the canvas. x, y and radiusPixels are all in pixels so no conversion is needed.

### **get methods**
The following are methods for getting various physical properties of a ball.
- getDisplayX, returns the ball's rounded distance from the left wall in metres
- getHeightAboveGround, returns the ball's height above the ground in metres
- getDisplayY, returns the ball's rounded height above the ground in metres
- getCanvasY, takes a value measuring the the ball's height above the ground in metres and returns a value measuring the distance from the top of the canvas to the centre of the ball in pixels.
- getDisplayVelocityX, returns the ball's rounded x velocity in metres
- getDisplayVelocityY, returns the balls rounded y velocity in metres
- getDisplayAccelerationX, returns the balls rounded x acceleration in metres per second squared.
- getDisplayAccelerationY, returns the balls rounded y acceleration in metres per second squared
- getEnergy, returns the ball's energy in Joules
- getKineticEnergy, return's the ball's kinetic energy in joules
- getGraviatationalEnergy, returns the ball's gravitational potential energy in joules

&nbsp;&nbsp;
## **Simulation Class**

The Simulation class holds the physics parameters used in the simulation such as the strength of gravity and fluid density, information about what the chart should be displaying and the data itself, various simulation settings and also a few timers, for instance the time since the last simulation reset.

### **update()**

It's method update is the main loop of the simulation which after being called from the constructor will continually calls itself at a default rate of 60FPS. It does the following:
- Clears the canvas
- Set's the time of last update and time passed since the previous update
- Updates the ball
- If this simulation is not paused it stores some of the ball's information that is to be displayed in the chart.
- Updates the physical constants according to the html input elements
- Renders the chart
- Updates the ball's current displayed information such as it's position, velocity, mass, density
- Finally calls itself

### **Chart data**
posDataPoints, velDataPoints, accelDataPoints and energyDataPoints are arrays that store the positions, velocities, accelerations and energy data points for the ball. The energy data array is one dimensional where as the rest are 2 dimensional, containing 2 arrays: the first corresponding to the respective data for the x direction, the second for the y.

Each item inside the innermost arrays is a dictionary setup using the format the chart uses with value stored with the x key being the simulation runtime and for the y, the respective data value.

The user has the ability to limit the number of data points shown (and stored) and updateChart() is responsible for doing this.

### **metresToPixels() and pixelsToMetres()**
Converts a value measured in metres to a value measured in pixels and vice versa.

### **setUpdateTime()**
Before updating any of the balls, the simulation updates the property lastUpdate and timePassed such that lastUpdate is the time to which all balls should be updated to, and timePassed is the time that has passed since the last update.

As such balls will use timePassed to update themselves.

### **What I would change if I were redo it**
During the making of this script I didn't think of the fact that libraries most likely exist for lots of the things that I wrote myself. For instance, finding the intersection between a straight line and a circle, perhaps apply gravity, friction and drag, and maybe even intersection between multiple objects. If I were to extend this project in the future or do something similar, I would most likely look into available libraries first.

## **Extra features that could be added**
- The ability to change floor material and floor friction
- The ability to change the velocity of the fluid, as currently it is always at rest.
- Add more balls and allow them to collide.

### How the simulation manifests within the website
- multiple versions
- gets settings from html elements 

## **Lessons**
The website has 5 lessons on the following topics:
- Gravity
- Newton's first law
- Drag and friction
- Conservation of energy
- Buoyancy

Each lesson has it's own html page and they can be accessed via the navigation bar and every lesson except newton's first law has a version of the simulation with only the settings relevant to that topic. 

For example, the simulator on the gravity lesson page has only the setting to change the strength of gravity and the option to have the ball bounce against the ceiling.

## **Asteroids Game**
This asteroids game was made as part of my original plan which was to have a website containing lessons on many different topics and to have some form of interactive element in each topic. For asteroids the interactive element was going to be an asteroids game.

The idea was also to highlight that flying through space is very different from flying a plane of from how they show spaceships flying in movies (for instance spaceships have no need to bank).

After making the sequence of lessons that explained enough for someone to understand why a spaceship might move the way that it does in space (and importantly why the player's ship moves the way it does in the asteroids game), I decided to make the ball simulator to make the lessons more interesting. This slowly became the bigger and more complex part of the project, leaving the asteroids game slightly irrelevant, however I enjoyed creating it and it was still a decent part of my project and so I wil leave it here.

### **What I would do differently**
If I were to remake the asteroids game, I would research physics and mathematics libraries first instead of doing what I did and coding them myself. One feature that I considered adding was having the asteroids bounce off of each other which I think could add an enjoyable level of chaos to the game and there may exist a library that could help with that.