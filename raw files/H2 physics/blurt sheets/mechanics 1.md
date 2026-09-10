# mechanics blurt sheet 1
# 6/9/26

ch 1 quantities

standard form and prefixes

standard form is x10^n behind a number to conform to scientific notation for expressing incredibly small or large numbers in their proper SI units.
prefix: n
pico: -12
nano: -9
micro: -6
milli: -3
centi: -2
deci: -1
kilo: 3
mega: 6
giga: 9
tera: 12

random error (precision) is the variance in a set of data, and systemic error (accuracy) is the mean's deviation from the actual value.
precision is enhanced by taking more readings and accuracy is improved through zero-error deduction (e.g. geiger-meter readings need to be taken in the same environment without the radioactive source being measured)

absolute uncertainty is calculated by taking half the difference between high and low values to obtain a +- of the mean value. absolute uncertainty is in 1 s.f.

fractional uncertainty is absolute uncertainty over the reading. fractional uncertainty is in 2 s.f. and can be multiplied by 100% to get the percentage uncertainty

homogeneous equation vs true equation

a homogeneous equation is an equation that makes sense in the sense that all units and quantities match on both sides of the equation, but it may not be true; a true equation is a real, verified formula that has logically matching quantities on both sides. 

base quantities and derived units

base quantities are fundamental units of the world that cannot be further reduced. they are: time (s), space (m), mass (kg), current (I) and the rest are negligible. other units (such as force N) are derived from these base quantities to give a more comprehensive understanding of the quantity being measured. 

scalar vs vector; add and subtract by diagram

scalar is the magnitude only and vector is the magnitude with direction. vectors can be perceived using vector diagrams (both 2d and 3d) and added together to get a resultant vector that is akin to going through the motions of both vectors at once. subtraction of vectors gives a vector from the endpoint of one to the endpoint of another. 

resolve a vector; reconstruct from components

vectors can be resolved by splitting into horiozontal and vertical components with respect to whichever plane you need the component for. with the angle offset being alpha A as an acute angle between the plane and the vector, vector * cosA is the horizontal component and vector * sinA is the vertical component (should verify during a question using TOH CAH SOH trigo). if the horizontal and vertical components of a vector are known, it can be reconstructed back to its original and even obtain its angle offset from the plane using trigo. 

propagate uncertainty: sum vs product vs power

summation of quantities adds absolute uncertainties to get the absolute uncertainty of the resultant quantity
product of quantities compounds fractional uncertainty by adding fractional uncertainties together to obtain the fractional uncertainty of the resultant quantity.
when there are orders of power on a quantity, the order of power is used as a coefficient before that particular quantity's uncertainty (absolute or fractional) value before adding all the uncertainties together.

upper-lower bound when the function is awkward



ch 2 forces and moments

name every force on one FBD

weight, normal contact force and other externally acting forces (present where question tells you)
other externally acting forces can be: frictional, buoyant, electrical, magnetic, gravitational (weight is a subset of this), mechanical

Hooke's law: what the extension actually is

the extension x/m is the displacement of a spring system. each spring has a constant k/Nm^-1 that determines how much force is applied by the spring depending on the displacement. this gives us an equation of F=kx, and yes, it is a linear relationship because the force exerted by a spring is proportional to its extension. however, springs will physically fail once they reach their yield point and the linear relationship of F=kx ceases to be true. This point is the 'limit of proportionality', and after this point the displacement-force diagram only increases at a decreasing rate.

moment of a force about a point

moment = radius about point * force applied perpendicular to radius

couple vs torque of a couple

a couple is a pair of identical forces in opposite directions perpendicular to their radius to a point, producing identical moments about a point in the same rotational direction. The torque of a couple is the total moment produced by a couple. 

principle of moments
?

translational and rotational equilibrium together
translational equilibrium is achieved when all force vectors acting on an object sum to 0
rotational equilibrium is achieved when the sum of clockwise and anticlockwise moments about every axis is 0 


ch 3 motion and forces

distance vs displacement; speed vs velocity

speed and distance are scalar quantities while velocity and displacement are a vector quantities

acceleration from a v-t graph (gradient and area)

acceleration of an object is the gradient of the curve on a v-t graph (found by diffrientating v-t curve if it is non-linear). area under v-t graph from point to point gives displacement (integration). 

SUVAT: when it is legal

SUVAT equations are legal for portions where acceleration is constant 

Newton 1, 2, 3 in one line each

N1L: an object in motion will continue in motion unless if an external force acts upon it
N2L: force is the change in momentum over change in time
N3L: for every action there is an equal and opposite force reacting 

N2L momentum form: when mass is not constant

when mass is not constant, momentum changes proportionately to mass change since p=mv and force changes even when velocity is constant

multi-body: one FBD per body, shared T and a

in a multi-body diagram, each body should be split up into singular bodies with their interaction forces drawn on each body as an external force. 

ch 4 energy

work as force along displacement; sign when force opposes motion

work done = force x distance
when force opposes motion, it is in the direction opposite to the motion and is thus negative

KE; work-energy theorem

KE = 1/2 * mv^2

GPE near Earth vs gravitational PE from infinity

GPE near earth is mgh, GPE from infinity is -GMm/r 

elastic PE as area under the F-x graph

EPE = 1/2 * kx^2

force from the potential gradient

F = -dU/dt

power and efficiency

power = joules/s = dW/dt

ch 5 projectiles

independence of axes

vertical velocity and horizontal velocity are independent of each other by vector resolution; both components are separately calculated

time of flight from the vertical equation

time of flight depends on the time taken for the vertical velocity to become negative due to constant gravitational force acting downward (use SUVAT to find)

landing angle is not launch angle

landing angle is relative to the place that the object drops at; if the landing point is lower than launch point, take current horizontal and vertical components of velocity to find the current velocity vector and the angle relative to the landing point (using trigo).

air resistance: flatten the parabola, earlier drop

air resistance opposes the motion vector. horizontal velocity decreases as the projectile travels, upward velocity decreases at an decreasing rate (air resistance directly proportional to velocity), downward velocity increases at a slower rate than without air resistance as air resistance is opposing the downward gravitational acceleration. This results in a faster peak and a slower drop.

ch 6 collisions

impulse as area under F-t and as change in momentum

impulse is the change in momentum dp. since F = dp/dt, integrating F-t curve gives dp, which in turn is impulse.

momentum conserved; KE only if elastic

law of conservation of momentum states that the sum of momentum in an isolated system stays constant. In an elastic collision, all KE is transferred with 0 losses and hence kinetic energy is fully conserved. 

max compression: same v, leftover KE to EPE

at the maximum compression in a collision with a spring system, both bodies coalesce into 1 body. new composite body takes on velocity of slower original body, and difference in total KE of original bodies and new composite body is KE converted into EPE in spring. upon release of EPE, mechanical force is exerted on both original bodies relative to their velocity, similar to that of explosion/recoil (equal and opposite force). when things get confusing, just COM and COE everything to balance it out.

explosion: COM unchanged, KE increases

explosion releases chemical potential energy as KE so KE of everything increases. due to COM, sum of momentum of all fragments sum to 0, so sum of horizontal and vertical momentum components are 0. 

relative velocity / reduced mass for max compression

? reduced mass ? 
during compression of spring in a colliding spring system where both bodies are moving in the same direction, the difference in velocities is the velocity of the faster object is the its velocity relative to the slower body. this reduces the problem down to a simple non-moving object while the other moves, before we add their relative velocity back. 

ch 7 circular

angular speed, period, frequency; centripetal acceleration formulae

frequency f = 1/T (T=period)
angular speed w = 2 * pi * f
centripetal acceleration = v^2/r

which force component is centripetal

force component that is perpendicular to the velocity vector pointing towards the centre of circular motion is the centripetal force.

conical pendulum: how tension splits

tension horizontal component is the centripetal force while vertical component is the force holding the object up

banking: how the normal splits

horizontal component of the normal (from vector resolution of normal contact force exerted on object by banked path) provides a portion of the centripetal force for circular motion. 

vertical loop: critical speed at top and bottom

in a vertical loop, gravitational acceleration is constantly acting downwards. centripetal acceleration at top of loop is provided by gravity 

ch 8 gravity

Newton's law of gravitation and field strength

the gravitational potential of a body is inversely proportional to its distance from another body and directly proportional to the other body's mass. field strength is inversely proportional to the square of its distance from another body and directly proportional to the other body's mass. 

gravitational potential and PE from infinity

gravitational potential = GM/r, GPE = GMm/r

escape vs circular orbit energy

escape occurs when the gravitational acceleration is less than the centripetal acceleration needed to maintain circular motion around a body. this means that gravitational potential energy has reached 0 and the object can escape to infinity

Kepler's third law from centripetal = gravity

ye i forgot this one lol
but what i do know is this kepler guy had a third edition satellite or something that went kinda far into space

geostationary: period, plane, direction

geostationary satellites are satellites that stay above a certain location on a planet, having the same angular velocity as the planet's own rotation. 