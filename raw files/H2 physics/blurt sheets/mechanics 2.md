# mechanics blurt sheet 2
# 8/9/26
# exam circumstance -> first moves / framework only
# red = no attack plan; yellow = plan known but one soft link

ch 1 quantities

they ask if an equation can be correct from units alone
homogenous equations may not be true equations as true equations have to be tested and proven in experiments

they give a derived unit and want base units
use equation for deriving the derived unit and reduce base units out of it

they give repeated readings and ask absolute uncertainty
find difference between lowest and highest and half to get absolute uncertainty, and round to 1 s.f. for summation of multiple quantities, absolute uncertainty stacks and adds together.

they give a product / quotient / power and want the uncertainty
in product and quotient, the resultant fractional uncertainty is the sum of the fractional uncertainties of other product or quotient quantities. power of a quantity becomes a coefficient of its uncertainty (both fractional and absolute calculations). to get absolute uncertainty of resultant quantity, multiply the other side by the total value of the resultant quantity (since fractional uncertainty is absolute uncertainty / quantity)

the function is awkward (trig, root, exp): how you get delta Q
linearise equation and find delta Q using the linear model

they mix random, systematic, precision, accuracy, resolution
random error dictates precision, which is variance of data about its mean. systematic error dictates accuracy, which is how close the mean is to the actual value. random error is reduced by taking more readings and reducing uncontrollable factors (e.g. taking longer reading so denominator of fractional uncertainty is larger), systematic error is reduced by accounting for zero-error and removing constant, controllable error sources from interference. resolution of an instrument is how precise its measurement can be, which determines what degree of measurement can be performed. higher resolution means measurements with more d.p. to work with (more precise and hence lower uncertainty)

vector sum or difference needed in 1-D or 2-D
vector sum is akin to applying the movement of one vector after the previous. can be summed using vector resolution, parallelogram method or triangle method. vector difference is the vector from the endpoint of one vector to another (this is more towards the discipline of math)

they give magnitude and angle: get components; or two components: get resultant
when given magnitude and angle of a vector, use trigo to find horizontal and vertical component with respect to the plane of the angle given. horizontal = x * cos(theta), vertical = x * sin(theta). for two components, resultant magnitude is obtained with pythagoras theorem with horizontal and vertical components, and angle is derived using trigo (ratio of components is tan(theta)) 

ch 2 forces and moments

static object / rod / ladder / boom: will it tip, slide, or stay
N2L: no change in velocity unless external force acts upon it.
N3L (if leaning/supported by another surface): equal and opposite reactive force for every force applied (i.e. friction, normal contact force).
static object stays when no external force acts upon it to make it move, and reactive forces keep it in equilibrium. 

spring stretch or compression: what length to use in Hooke
displacement of spring as x, and F=kx while limit of proportionality is not reached

moments about a point; why choose that pivot
moment = F x d where d is distance from pivot point. 

couple on a body: net force and net torque
couple is pair of equal forces in opposite directions, producing identical moments about a common pivot in the same rotational direction. net force is 0, net torque is sum of moments by the couple

rigid body in equilibrium: the two conditions and the FBD rule
body in equilibrium has net force = 0 and sum of clockwise and anticlockwise moments = 0. each body requires its own FBD, and its interaction forces with other bodies are drawn onto their own FBD. 

unknown contact force at a pivot or edge (direction not obvious)
use equilibrium as sum of all forces (horizontal and vertical components) and moments respectively = 0 and figure out the normal contact force from various parts in a system. 

ch 3 motion and forces

read an s-t, v-t, or a-t graph: what gradient and area mean
s-t gradient is velocity, v-t gradient is acceleration. a-t area is velocity, v-t area is displacement. diffrientiate and integrate to find gradient/area for sections where velocity is non-linear.

motion with constant a: which equations are legal
all SUVAT is legal as long as a is constant. on a graph where a takes on different values, SUVAT only applies for period of t where a is constant (a = dv/dt).

find resultant force when a or delta p is given
N2L: definition is F = dp/dt, but usually mass is constant do F = m * dv/dt and thus F = ma.

variable mass / rocket / jet / chain: which form of N2
for changing mass, momentum is changing regardless of velocity. use F = dp/dt

two or more connected bodies (string, pulley, person+crate)
FBD everything. connected to string = tension on string (that is usually unknown). pulley only translates string tension to other directions.

identify an N3 pair vs two forces on the same body
what on earth does this prompt mean
but N3L is equal and opposite force for every force 

ch 4 energy

work by a force along a path; force not along displacement
work done = force * distance where force used to calculate is along the direction of displacement. if force applied is not in the direction of displacement, use vector resolution to find the force acting along the distance and calculate using that. so this means that if a force is perpendicular to the displacement (such as circular motion) the work done by the force is 0.

speed change with no non-conservative work: which energy book
is energy transfer is lossless, conservation of energy (energy can neither be destroyed nor created) to find change in speed

near-Earth height change vs gravity far from Earth / orbit scale
near-earth uses mgh for GPE while orbit scale GPE is -GMm/r 

spring stores or returns energy: which store; which graph area
spring stores energy as EPE = kx^2 and returns as mechanical force (KE)

given U(s) or U(r): get force direction and magnitude idea
? what does this prompt mean 

rate of energy transfer or efficiency of a machine
efficiency of a machine in energy transfer is the ratio of energy successfully transfered to total energy

ch 5 projectiles

projectile in air, no drag: how you split the problem
vector resolution to split projectile travel into vertical travel (up n down) and horizontal travel (purely travelling horizontally for as long as projectile stays in the air). during vertical motion, initial velocity u is vertical component of launch velocity, and acceleration is downwards gravitational acceleration. use SUVAT to solve.

find time to hit a given height or the ground (not same level)
from apex, find time taken to hit landing point in the vertical model. then incorporate horizontal component. use horizontal component and vertical component at point of landing to find angle of impact (using trigo)

air resistance present: qualitative changes to path and times
air resistance opposes velocity and is directly proportionate to it. going up, air resistance opposes the upward motion and therefore time going up is less. going down, air resistance opposes downward motion and projectile takes longer to fully go down. travelling forward, air resistance opposes horizontal motion so total distance travelled is less than without air resistance. 

ch 6 collisions

F-t pulse or hit: find impulse / average force / delta v
impulse is the change in momentum. since F = dp/dt, integrating F-t curve gives impulse over the period of time integrated as dp. average force is found by... averaging the force on the graph across t. when mass is constant, dp = m * dv. find dp and then divide by mass to obtain change in velocity. 

1-D or 2-D collision: what is always conserved; what to check for KE
momentum and energy are conserved. if no energy is lost as other forms (elastic collision), total KE stays constant. 

two masses with a spring between them: find max compression
for spring system collision, reduce system to a stationary collision system by using the relative velocity of the faster moving body with respect to the slower moving body. this 'extra' velocity is converted iinto EPE when the spring is fully compressed. use KE and EPE formulae to calculate what happens after that. after that, add the relative velocity of both bodies back in. during max compression, both bodies coalesce into 1 big body with the mass of both bodies combined. use COE to get the velocity of whatever else you need to. 

after the spring returns to natural length: how you get final speeds
assuming that the collision is lossless, by COE to find EPE fully converted back to KE, KE from EPE is distributed to both sides equally. to balance and verify, use COM for the before and after compression. 

explosion, recoil, or gun: COM and energy moves
by COM, sum of horizontal momentum and sum of vertical momentum are all individually 0. since KE comes from chemical potential energy, COE does not really apply unless they tell you the CPE of the blast. 

ch 7 circular

uniform horizontal circle: what provides mv^2/r
externally acting force provides centripetal force perpendicular to the velocity towards the centre of circular motion. in a uniform horizontal pendulum, this is the tension of the string providing the centripetal force. 

conical pendulum or banked track: resolve and assign centripetal
in conical pendulum, tension horizontal component is centripetal force and vertical component is tension required to hold the pendulum's weight. on a banked track, normal force horizontal component provides centripetal force and vertical component is the normal force that holds the weight (N3L). usually derived by taking vertical component which is fixed by the weight of the body, and using trigo to calculate horizontal component (or if you are lucky you get the normal force perpendicular to the banked slope). 

too fast / too slow on a bank with friction: which way friction points
when the velocity does not match the velocity required to stay on the bank (derived with centripetal acceleration found from previous section), body will slip further or closer to middle of bank (adjusting r to match centripetal acceleration provided). friction on bank opposes this and provides the slight extra force in the horizontal component to either add or subtract from the centripetal force, keeping the body on the same portion of the bank and preventing slippage.

vertical circle / loop: forces at top vs bottom; critical speed
at top, centripetal force provided by downward gravitational force and externally acting force (usually normal contact force for this) as both are pointing downwards, so centripetal force = g-force + ext-force. at bottom, gravitational force is in opposite direction of centripetal force so instead of helping provide centripetal force, it opposes it. externally acting force needs to compensate for this opposition, so at bottom, centripetal force = ext-force - g-force. ncf is the perceived feeling of weight by passengers when ext-force acts upwards, so passengers (roller coaster, loop-de-loop plane) feel more 'weight'. if things get confusing, N3L everything and everything will make sense.

ch 8 gravity

field or force between masses / at distance r from a planet
F = -GMm/r^2, field = -GM/r^2 

potential or PE; work to move a mass in a g-field
potential = -GM/r, PE = -GMm/r. potential energy is the amount of work that needs to be done to move a mass from that point to infinity 

circular satellite orbit: find v, T, or total energy
gravitational acceleration provides for centripetal acceleration for orbit. use derived centripetal acceleration to work out v and T using circular motion formulae. 

escape from a surface or orbit radius
to escape from orbit, total energy = 0, so KE needs to overcome GPE fully to escape to infinity. KE + GPE = 0 to escape.

Kepler / compare two orbits
kepler third law states that the square of period of orbit is directly proportional to the cube of radius of orbit, regardless of mass. 

geostationary: constraints the answer must satisfy
geostationary satellites are above a certain geographical location of a body that it is orbiting; angular velocity of orbit of geostationary satellite is the same as the angular velocity of the rotation of the body.