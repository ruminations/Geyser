# The Geyser™ Project

- [Synopsis](#synopsis)
- [Roadmap](#roadmap)
- [Intellectual Property](#intellectual-property)
- [Requirements](#requirements)
- [Design](#design)
- [Novelty and Non-Obviousness](#novelty-and-non-obviousness)
- [Prototype](#prototype)
- [Testing](#testing)
- [Empirical Experience](#empirical-experience)
- [Notes and TODO](#notes-and-todo)
- [Glossary](#glossary)

----------
## Synopsis

The Geyser™ Project is an effort to redesign and build from scratch the extruder assembly (popularly known as the 'hot end') of an FFF 3D printer.  The purpose of the project is to rectify inadequacies of existing designs in order to substantially speed the development of process parameters that are repeatable, reliable, and amenable to high print speeds.  The body of decades of pre-existing industrial plastics extrusion knowledge and experience will be applied to implement this rectification.

The lexicon used in these documents is taken from that large body of knowledge and experience.  That lexicon pre-dates 3D printing and often differs from the ad-hoc language adopted by the various informal 3D printing communities.  The historical terminology will be prefered in all cases, to the exclusion of recent re-definitions by the 3D printing communities.  Many of those re-definitions confuse and obfuscate, sometimes for merely philistine promotional purposes.  A glossary at the end of this page documents and clarifies these varying usages, prominently noting prefered usage.

The overiding importance of closed loop control in the extruder assembly with respect to print quality dictates that no consideration whatsoever shall be given to the following artificial design constraints that handicap conventional efforts:

* attempts to retain compatibility with existing designs
* requirements that the design be producible solely on a FFF printer
* avoidance of custom constructs merely for cost efficiency

In consequence, the resulting design is likely to cost a few hundred dollars to manufacture, in contrast to around fifty dollars for existing designs.  In volume, naturally, the design could be cost competitive.  A highly precise effector is so important that it likely would produce superior prints even using mechanically inferior (and less expensive) motion control assemblies, and that justifies excluding these legacy considerations.

#### Contact
See:

> [Contact Link](https://github.com/ruminations/Contact)

#### Project Status:

Stage 2: practical design

----------
## Roadmap

1. preliminary design
2. practical design
3. prototype fabrication
4. bench testing
5. adaptation to, and deployment on, a pre-existing FFF 3D printer
6. empirical testing
7. deployment of an FFF 3D printer design tailored to the Geyser extruder

----------
## Intellectual Property

Intellectual property has three aspects:

#### Trademark

The term 'Geyser' is hereby claimed, on 15 August 2018, as the trade-name for an extruder assembly for FFF additive manufacturing, as documented by the revision history of this repository.  That term may later be expanded to include a full FFF 3D printer design.

All rights are reserved, and at such time that the project produces a stable prototype, formal registration will be pursued.

#### Copyright

The documentation as well as the specific expression of representations embodied by these documents is material subject to copyright law.  Copyright is hereby claimed, on 15 August 2018, for all documentation and specific expressions in this repository.

The material is licensed under the ASSAIL license.  For licensing details see:

> [ASSAIL License Text](https://github.com/ruminations/Licenses/blob/master/ASSAIL/ASSAIL.txt)

#### Patent

Patent law governs generalized geometric and physical aspects of a design that lend benefits adjudged to be novel and non-obvious in the cultural milieu prevailing at the time the embodied ideas are publicly revealed.

As an example, the so-called 'Bowden tube' on many FFF 3D printers was invented by an Irishman, Ernest Monnington Bowden (1860 - 1904).  An abstraction of the ideas embodied by that geometry was patented in 1896 (English Patent 25,325 and U.S. Pat. No. 609,570).  At the time, the ideas were adjudged both novel and non-obvious, so E. M. Bowden was able to license the design to The Raleigh Cycle Company of Nottingham on 12 January 1900, one of whose directors was Frank Bowden (no relation).  It is arguable that even then, the validity of the patent might have been challenged on the grounds that the ideas are obvious.  Now such a patent would clearly fail to be granted.

At some level, everything is obvious, and in modern times that notion is all the more true.  The pursuit of a patent is an extremely expensive enterprise, a luxury only well heeled organizations can afford.

There are certainly novel ideas disclosed in the unique geometries presented in this repository.  It might perhaps be possible to successfully pursue a patent on some of them.  From this date of first publication, 2 September 2018, there is a grace period of one year in the patent law of most nations, providing an opportunity to file for a provisional patent.  If there is someone with suitable legal training interested in pursuing that, collaboration is possible.  Otherwise, on 2 September 2019, the novelty embodied by the geometry disclosed here will become defacto public knowledge.

The only real value in obtaining patent papers is the right to exclude.  The only really interesting right to exclude is the right to exclude restrictive and proprietary commercial interests from exploiting the general population.  This is the appeal of Richard Stallman's GPL: it uses the right to exclude offered by copyright law to require inclusion by excluding those who would exclude - sheer genius.

Copyright may be obtained merely by authoring something and asserting a claim of copyright.  There is no cost as copyright only governs a specific expression of ideas and does not preclude re-expression in distinct forms by others.  A patent claims right to more abstract and general expressions, as defined by the patent document's 'claims' section.  The fewer and less specific the claims, the stronger the patent.  Given this general nature, official review and approval is necessary, and that is expensive.

As such, few, if any, once having obtained a patent, exercise their right to exclude in order to enforce inclusivity.  There will come a day when a strong patent is so licensed, and the world will change.  That will probably not happen with this project, but any collaboration that successfully pursues patent papers will result in licensing for the purpose of enforcing inclusivity.

----------
## Requirements

1. closed loop temperature control
2. infrared temperature sensing
3. closed loop pressure control
4. inductive die heating
5. integrated elevated temperature, vortical flow, cooling fang
6. steam cooling medium derived from waste heat
7. programmable control electronics integrated in the cartridge holder
8. quick-change cartridge, analogous to an Aloris toolpost or pin registered optics
9. controller area network (CAN) communications interface

In short, the extruder assembly is to be a self contained mechanical module.  When supplied with filament and electrical power, the module shall be capable of receiving commands that simply specify material, temperature, and rate of extrusion, in order to uniformly and consistently deposit a precise volume of material in each voxel.

The rate of extrusion may then be easily correlated with carriage velocity both during times of acceleration and times of steady movement, thereby facilitating high quality printing, devoid of cavities and burbles.  The first requirement is presently the only feature implemented by commonly available 3D printers.

Changing die orfice, filament diameter, material, or color in such a setting is easily accomplished by exchanging cartridges - that is, the extruder cartridge is considered tooling - it is neither unique, nor is it considered intrinsically part of the 3D printer.  Some shops will require but a single cartridge, others will need a full complement of cartridges.  The goal is to make a 3D printer a professional machine tool, no different than, for example, a toolroom lathe or a milling machine, by taking a systems design approach.

----------
## Design

Design data is presented in the form of `.svg` and `.scad` files.  Specific geometric information is contained in the text of those files along with some useful commentary.  `.svg` files may be found in the `images` directory.  `.scad` files may be found in the `openSCAD` directory.  All detail is subject to change.

The following is a sectional drawing of the extruder assembly:

![Extruder Assembly Section](./images/extruder_section.svg)

The strain gauge washers are detailed in this `.svg`:

![Strain Gauge Layout](./images/strain_gauge.svg)


#### Components

The components visible in the sectional drawing are substantially all circular and coaxial in cross section.  These components are as follows:

* The _filament_ in the sectional diagram is brown, becoming red in its molten transition region, and dark orange where it is molten.

* The _cartridge_ (silver with powder blue gradient fill) is a cylinder of stock  1-1/2 " type 304 schedule 80s stainless steel pipe (nominal diameter 1.9", and 0.200" nominal wall thickness).  It establishes a fixed reference frame attached to the printer carriage.  The inside is finished to 40.0 mm with a reamer so that  the gauge washers fit with a tight clearance tolerance.  The outside is finished to 46.0 mm for accurate registration with the cartridge holder.  That produces a precise 3.0 mm wall thickness.  The top end of the exterior is threaded with M40x1 for 8 millimeters.

> There are 2 slots at the bottom of the cartridge, to exhaust evolved steam through the fang (not shown) at the bottom.

> Austenitic stainless steel is 'non-magnetic'.  This means its relative permeability is only a little more than unity.  Nevertheless, it does contain iron.  In the geometry described here, there is a full loop with no gaps of material containing iron - the die, the gauge washers, and the cartridge.  This helps shield the inductive heating coils by providing a slightly preferential path for magnetic flux.

* The _die_ (steel blue) is machined from stock dimensional 12 mm diameter drill rod (tool steel), and as such is a ferro-magnetic and electrically conductive material with relatively high resistivity and heat capacity (thermal mass).  Inductive heating is achieved via both ohmic losses in induced currents and hysteresis losses in induced magnetic fields.  It is finished with black oxide for corrosion resistance and good thermal radiance for the optical sensors.

> The top end carries an aluminum heat sink (not shown) that mates with the standard metric taper pin shank (1:50 included angle) of the die.  This facilitates fabrication with common tools and provides a jam fit for good thermal coupling.

> The sienna orifice is a tungsten carbide insert.  It is installed using the same method for placing valve seats in engine blocks: the insert is cooled in liquid nitrogen so that it shrinks.  When placed in the 2 mm bore it warms to form an interference fit with the tool steel.  This yields a highly thermally conductive orifice whose geometry endures abrasive materials.  The orifice itself is best formed by electrical discharge machining (EDM).  Alternatively, for less demanding use, the orifice may be formed in the tool steel with two drilling operations, or may be a hardened tool steel insert.

* Three _infrared optical fibers_ extend to the right from the die in the section.  These carry thermal radiation from the die to electro-optical pyrometer components mounted on an external PCB that is mounted in the cartridge holder attached to the carriage.  While these appear aligned with the inductive coil leads, they are actually oriented 90° from those leads to avoid external mechanical interference with the pyrometer PCB.  The pyrometers, in turn, permit very precise and highly localized temperature monitoring.

> There are many exotic methods for making an infrared optical fiber.  Among those, the simplest and most economical are the hollow tube 'leaky wave guides'.  We simplify further - we neither have to worry about bends nor propagation beyond 3 cm.  Our infrared optical fiber is simply a 1.2 mm borosilicate capillary (salmon), with 0.69 mm core (peach puff) slipped into a stainless steel #15H (heavy wall) hypodermic tube (slate gray), leaving a minimum of .0028" (.07 mm) clearance. Both are mass produced, extremely inexpensive, commodity items, available in standardized sizes.

> For a prototype, the borosilicate may be fixed in place with a small amount of cyano-acrylate adhesive applied to the outside exterior end of the capillary before insertion.  More professionally, the capillary can be melted closed on one end.  Then the hypotube is inductively heated.  Applying air pressure at the other end of the capillary expands it to adhere to the inside of the hypotube.  After cooling, the glass is trimmed to the length of the hypotube.

> The short length gives a clear sight acceptance angle of 4°.  The natural opacity of boro-silicates in the infrared spectrum, coupled with smooth surfaces and the natural reflectivity of glass at shallow angles broadens this somewhat, perhaps to about 8°.  Of course significant fractions of the light entering at larger angles, perhaps up to an additional 20°, will pass to the pyrometer.  That yields an effective numerical aperture approaching 0.25, considered in terms of the physics, in contrast to the refractive index formula, which has no solution for hollow wave guides.

* The _strain gauge washers_ (slate gray) are machined from stock dimensional 304 stainless steel, and are therefore 'non-magnetic' at room and operating temperatures.  The washers are coated with boron-nitride, a high temperature electrically insulating finish that is available in a spray can and is baked on after application.  The thin section is 1 mm thick and so is slightly flexible.  The strain gauge conductive pattern is printed on both sides on the surface of the thin section.  The geometry of the gauge is depicted in `strain_gauge.svg`, with the inside face to the left and the outside face to the right.

> Initially these patterns will be formed in copper foil annuli, pressed into the boron-nitride carrier solvent prior to baking. Post baking, the gauge itself is  etched from the foil using common PCB lithographic processes.  Ultimately, these patterns should be etched from a sputtered titanium nitride layer in order to improve the gauge factor, typically 2 for copper but about 6 for titanium nitride, which is comparatively resistive.

> The process permits feed throughs, so each washer is wired into a half bridge in-situ and the three signal contacts are available on a standard Berg style .1" on center 3-pin modular header on the washer face inside the cartridge.  Wiring to control electronics passes through the cartridge wall.  The small gold squares in the diagram correspond to the header pins, which are trimmed flush on the outside and extend vertically on the inside.

>  A 90° groove, 2 mm across the corners is machined and centered in the washer edge.  The bottom washer is fixed in place by a #24 piano wire gauge (.0551" or 1.4 mm) stainless steel wire that feeds in through a hole in the cartridge drilled tangent to the groove.  A short 90° bend on the end of the wire prevents it from fully entering the cartridge, facilitating dissassembly.  The bend recesses in a pocket milled about the hole so it does not protrude.  Any steam that passes through the small clearance to the cartridge is caught in the vortex flow emanating from the fang and so is immaterial.  The top washer is fitted with a 1.0 mm x 18 mm viton (teflon) O-ring seal to prevent steam from escaping vertically.  The die/heatsink washer sub-assembly is pre-loaded by tightening the cap (not shown) to a torque specification.  The center of the cap holds the Bowden tube fitting, rigidly referenced to the cartridge.

> The washers carry an oil impregnated bronze bushing that serves as a bearing for the die sub-assembly.  This permits the die to freely rotate in order to accomodate manipulating the orientation of a non-circular orifice.

* The upper part of the die carries an aluminum heat sink (not shown) with fins in the form of helical strakes.  The complex geometry may be formed by casting with the pattern created by 3-D printing.  The center hole is then finished with a standard taper pin reamer to match the corresponding taper machined on the die.  This makes a jam fit for good thermal contact.  It is critical that the heat sink have mechanical clearance to the cartridge, but that clearance gap should be small - perhaps half a millimeter.  Therefore, the raw casting should be oversize, with a precise diameter imposed by a finish cut on a lathe.

* The inductive coils are schematically shown.  They are 4 1/2 turn double pancake coils.  The lower coil is constructed from 12 gauge copper wire, sheathed in 3/32" i.d. silicone tubing with an 1/8" o.d, that provides high temperature electrical insulation.  The upper coil is formed from 20 gauge nylon coated magnet wire.

> The lower coil is to be driven at 4 kHz.  This has two benefits:

> - It is within the 100% skin effect limit of 4150 kHz for 12 gauge wire
> - It provides deep eddy currents heating the die

> The lower coil is used to maintain the process extrusion temperature set point, typically a few tens of degrees above the melting point of the filament.

> The upper coil is the primary of a transformer with the die as the magnetic core.  The aluminum heat sink is the single turn, short circuited secondary.  The upper coil dissipates power in this secondary, together with some electromagnetic losses in the die.  It is used to maintain a temperature near 100 °C at the top of the die.  Small variations in temperature control the volume of evolved cooling steam.

> The high power feeds extend through the cartridge to the left and right, suspending their respective coils.  They do not interfere with movement of the die/heatsink sub-assembly.

* The lower and upper parts of the die are sheathed by two lengths of 14 mm ID 16 mm OD silicone tubing (maroon).  The tubes are held in place and open by ferrules made from 5 mm lengths of stock 9/16" OD thin wall brass tubing (goldenrod).  The top and bottom ferrules bear on the bronze bearings and clear the die so that the die sub-assembly is free to rotate, as is the bronze bearing.

>  The lower tube provides thermal insulation for the hot end of the die.  The tubes are perforated in three places to support the infrared fibers.  More importantly, the tubes shroud the apertures so that only radiation from the die can propagate to the pyrometers, avoiding spurious temperature readings caused by reflections off of other components.

> The tubes also restrict the entry of cooling steam into the hollow fibers. Indeed, the induced flow near the open annuli between the tubes and the heatsink will tend to draw gas out of the clearance cavity.  The elevated temperature in the cavity raises its nominal pressure in accordance with the ideal gas law.  An exterior boot on the fibers shroud the pyrometers and prevent heated interior gas from escaping and cool exterior air from entering and corrupting readings.

> Finally, the two ferrules on the lower tube act as single turn shorted transformer secondary coils for the primary heating coil.  The induced currents produce a counter magnetic field in the die, spatially offset.  This pinches and intensifies the primary field produced by the primary coil, focusing induced heating in the die metal directly in the center of the primary heating coil, limiting field lines, and therefore induction, in the cartridge.

* The Bowden tube terminates in a commodity female Luer lock fitting of the type commonly used in medical systems.  The mating two piece male Luer lock fitting is threaded into the center of the cap.  The Luer taper provides an economical gas tight connection that may be rapidly secured or released by hand by turning the male hub two or three times.

#### Theory of operation

The die and heatsink sub-assembly is free floating within the cartridge.  The strain gauge washers are pre-loaded by tightening the cap which holds the Bowden tube fitting to a torque specification.

Therefore, equilibrium of forces requires that the force imposed on the filament by the filament feeder is balanced by an increased strain on the bottom washer and a diminished strain on the top washer.  This equilibrium is communicated by the solid (brown) part of the filament acting as a piston, the plastic part (red) acting as piston sealing rings, and the liquid part (orange) acting as a hydraulic fluid in equilibrium.

The hydraulic pressure is imposed upon the interior part of the orifice insert flanking the orifice hole, pushing the die and heatsink assembly slightly downward, cupping the bottom washer and uncupping the top washer slightly, imposing elastic deformation on the strain gauge conductive paths.

The two gauges at the bottom are in thermal equalibrium and the two gauges at the top are in thermal equilibrium, nulling any temperature coefficient intrinsic to the gauge wires.  The four gauges are connected in a full bridge, doubling the intrinsic gauge factor.  The center of the bridge is connected to a differential instrumentation amplifier, nulling any common mode cross talk picked up from the inductive heating coils.

There is a thermal gradient from the hot end of the die to the hot end of the heat sink.  Cooling steam flows downward in a counterflow arrangement through the heat sink, setting up another thermal gradient, referenced to the boiling point of water.  The three pyrometers monitor these gradients.  For PLA, the transition temperature is about 165°C.  The hot end of the die would be maintained at about 185°C, and the hot end of the heat sink would be maintained at about 145°C.  That stabilizes the position of the molten transition in the die.

Water is provided via a needle valve into an annular trough at the top of the heat sink, analogous to the mechanism that maintains fuel level in a carburator bowl.  An annular stainless steel mesh pressed into the top of the trough prevents splashing, and the bottom of the trough is scored to create the effect of an annular boiling stone.

When 1 gram of 100°C water (1.04344 cc) boils at standard atmospheric pressure (101.325 kPa), the steam tables tell us it expands in volume by a factor of 1603.64 to 1673.3 cc.  This is slightly less than the expected steam volume, 1701.1 cc, if water were a non-polar ideal gas at 100°C.  Opposite exposed charges on a water molecule attract one another, slightly compressing the gas relative to the ideal.

Since the cartridge is effectively sealed, evolved steam has no where to go but to stream downward along the helical strakes, where it absorbs heat from the progressively higher temperatures in the strakes.  The steam swirls in the lower cartridge cavity and flows out of the cartridge slots and into the fang.  The profile of the fang follows a venturi, so velocity increases and pressure drops.  The volume and velocity of gas (steam) is significant and so creates a whirlpool of steam with the orifice at its center when it exits from the lower fang openings.

Knowing the temperature, and hence the viscosity of the molten PLA, together with the pressure of the liquid in the die, and knowing the diameter of the orfice, the rate that molten material flows from the orifice is determined and known.

By correlating instantaneous pressure with instantaneous carriage velocity, constant material delivery is achieved.  In turn, the instantaneous pressure is controlled by the 'piston', i.e. the solid part of the filament, and that in turn is controlled by the filament feeder position.  By turning the filament feeder backward, zero relative pressure may be achieved, effectively turning the flow of material off.  By turning the feeder backward even more, a dynamic negative pressure can even be created, effectively cutting an incipient 'string' prior to rapid carriage movement.

Thus closed loop control of pressure is achieved, and thereby exacting control over the rate of delivery of molten material from the extruder assembly.  In turn, just the right amount of material is consistently delivered, dynamically correlated with carriage travel, without gaps or burbles.

Steam emanating from the integral fang keeps previously printed material proximal to the new voxels at an elevated temperature.  This anneals the printed material, mitigating residual strain in the printed material.  Moreover, the warm material forms a more secure bond with newly deposited voxels by making better use of the limited heat capacity of the molten plastic.  This mitigates de-lamination issues.  The vortical flow of the outflow from the fang creates an 'eye of the hurricane' at the die orifice, leaving still molten material undisturbed, and indeed, providing some aerodynamic stabilization and localization to that molten material.

The geometry of the steam flowing from the fang follows that of a Ranque-Hilsch tube, more commonly known as a vortex tube.  A vortex tube is a fluid dynamic heat pump commonly used with compressed air to supply augmented cooling to a cutting tool's point of contact.  Even with the comparatively low steam pressures in the fang and the open geometry about the die orfice, there will be a radial thermal gradient induced, with the 'eye of the hurricane' held a few degrees Celsius below the steam at the periphery of the cartridge.  Thus there is a very real heat pumping effect, actively moving heat from the orifice to the periphery, establishing a consistent cooling rate upon newly extruded plastic.

Thus latent heat of fusion is more effectively delivered to the already printed material, softening, and perhaps slightly melting it to form a good bond.  The steam ultimately condenses on lower portions of the part and on the build platform, so drainage and fluid recycling is necessary.  This is no different than machine tools, which typically use a continuous flow of cooling cutting oil at the cutting tool.

Note that the die and heat sink sub-assembly is free to rotate on its strain washers, since non-contact infrared sensors and inductive heating coils do not interfere.  Therefore, the orifice need not be circular.  A rectangular orifice can be dynamically maintained orthogonal to the printing path, effectively printing three or four lateral layers simultaneously.  It may also be oriented aligned with the printing path to rapidly lay down infill, where cosmetic appearance is not critical.  Other orifice orientations might have some use for visible cosmetic effects, for example, laying down material after the fashion of an italic calligraphic pen nib.  Orientation may be controlled by fitting the heatsink with a Halbach array and the cartridge with a non-slotted stator winding, creating a  servo in-situ.

Finally, it may be desirable to evacuate the die cavity to avoid all possibility of entrained air bubbles.  With this design, that requires great care, for a vacuum introduces one atmosphere of pressure into the force balance equations wherever the vacuum impinges on an unbalanced surface.

----------
## Novelty and Non-Obviousness

As mentioned, everything at some level is obvious.  Certainly all the ideas here have precedent.  Within the FFF eco-system, some of these ideas are apparently not obvious, for within that eco-system, manifestations do not exist.  The focus of this section will be on novelty and the benefits that novelty bestows within the confines of the FFF eco-system.  Perhaps the greatest novelty is the orchestration of the ideas as a whole, yielding benefit that exceeds what might be possible for each used alone.

#### External Strain Gauge Pressure Measurement

It is this element of the design that embodies the chief novelty and non-obviousness.  The key novelty is measuring the molten plastic pressure without needing to have a 'tiny pressure gauge' in contact with the plastic.

* simple and accurate
* amenable to mass production
* mechanically robust
* freedom from any mechanical interference with extrusion processes

In a sense, when highly abstracted, this novelty is nothing more than an infinitesimal Bowden cable.  The underlying physical mechanism (laws of physics and mathematics may not be patented) is the same balance of forces that lends utility to a Bowden cable.  In this case, the 'cable' is the die, and the 'sheath' is the cartridge.  It is the novel geometry, hydraulic coupling, infinitesimal movement, and custom strain gauges that embodies the physics as a patentable 'invention'.

----------
## Prototype

To be amended.

----------
## Testing

To be amended.

----------
## Empirical Experience

To be amended.

----------
## Notes and TODO

1 The design is essentially conceptually complete.  Some minor practical changes are being introduced during the comparatively laborious process of documentation.

2 Create SCAD file for die and heatsink sub-assembly and include images in README.

3 Create SCAD file for fang.

4 Determine specific geometry of steam cooling.

5 Diagram Bowden tube, vacuum, and steam attachments and associated O-rings.

6 Settle on quick release mechanism and design carriage mounting bracket.

7 Design small signal sensor electronics.

8 Design power drive electronics.

9 Select a SOC for the control system and design PCB.

10 Code the control system.

----------
## Glossary

The purpose of this glossary is to distinguish between historical plastics industry usage and modern 3D printing community usage.  Historical usage is prefered in all cases and is used exclusively in this repository.  Modern distortions are highlighted by ~~strike out~~ text.

* __Bowden Tube__

    More properly called a 'Bowden Cable', this is a tube through which filament is fed by the feeder into the extruder.  The forces present in the filament and the tube are in equilibrium, with the filament under compression and the tube under tension.  In FFF both are ductile plastic, unlike the original Bowden cable, so spontaneous feed induced by the relief of strain induced in the plastic by those forces is the origin of the need for 'coasting'.

* __~~Coasting~~__

   The artificial need to allow for the relief of Bowden tube strain when bringing the printing carriage to a halt.  With closed loop pressure control, the effect of coasting is automatically applied by the decaying pressure set point correlated to carriage speed.

* __Die__

    The tooling component of an extruder that defines the cross section of the extruded plastic.

* __Extruder__

    Historically, the assembly that heats plastic feedstock to a molten state and applies pressure to force it through a die.  That is the prefered meaning.  Modern usage that uses this term to refer to the feeder is deprecated.

* __Extrusion__

    A cross sectional profile that may be manufactured by an extruder equipped with a suitable die.  The profile need neither be circular nor simply connected.

* __Fang__

  A '_Fan G_ ang' that is used to cool extruded plastic by blowing air on it.  The expression is German: 'gang' is the word for 'passage' or 'duct', and 'fan' still means just 'fan'.  The visual appearance of two ducts flanking an extruder is that of a pair of 'fangs', which is English, but every German is also familiar with English.

  Common sense suggests that such a duct design would be guided by fluid dynamics, so this is the prefered form, not '~~petsfang~~'.  Cooling the extruded plastic is standard and necessary historical practice, either by air or liquid.  In the context of 3D printing, however, there are some novel issues, so it is entirely appropriate to use a neologism instead of merely calling it a 'duct'.  Since 'fang' is a generic term, not a marketing term, it is suitable and prefered.

* __Feeder__

  A mechanism to control the amount of plastic feedstock introduced to the extruder.  Currently in 3D printing, feedstock is typically in filament form.

* __FFF__

  _F_ used _F_ ilament _F_ abrication, one of many variations on the idea of 3D printing.

* __Filament__

  A form of extrusion that has a solid circular cross section.  It is typically used as plastic feed stock in FFF printing, but is more costly than granules.

* __Granule__

  An inexpensive commodity plastic feedstock used historically in extrusion operations.  3D printers may be easily adapted to granular feedstock, given a suitable extruder design.

* __~~Hot End~~__

  Historically, this is called the _extruder_, which is prefered usage and ~~hot end~~ is deprecated.

* __~~Nozzle~~__

  Historically, this is called the extrusion _die_, which is prefered usage and ~~nozzle~~ is deprecated.

* __Orifice__

    The opening in the die that defines the cross section of the extrusion.

* __~~Petsfang~~__

  A fang design promoted by David Petsel that became popular in early 2018.  The 'novel' feature of a ~~petsfang~~ seems to be that some rudimentary fluid dynamic calculations guided the design, so the cooling air flow is more or less laminar.  Since this is a marketing ploy, the term _fang_ is preferred.  Moreover, the efficacy of the fluid dynamics of this design is not without criticism by reputable engineers, and the fluid dynamic calculations, to all appearances, are not available for independent review.

* __~~Retraction~~__

  Operating the feeder in reverse in order to withdraw feed pressure in the extruder.  Retraction is an artificial need created by the failure to apply extrusion pressure with a closed loop control system.  With closed loop pressure control, retraction is a transparent operation, automatically and dynamically applied, no different in principle than forward feed.

* __Stringing__

  The undesirable print defect consisting of small diameter strings extending from a place where printing is halted for a rapid movement to a new postion to continue printing.

