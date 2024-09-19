# Introduction to chip packaging and decapping

Integrated circuits (ICs) are delicate silicon-based structures that require protection from environmental factors like moisture, dust, and mechanical stress. Without packaging, the silicon dies would be exposed and highly vulnerable to damage. Early on, before advanced packaging became common, many systems used Chip-on-Board (COB) techniques where the silicon die was bonded directly onto the PCB and then covered with a protective epoxy blob.

These “COB blobs” offered minimal protection and were often used in low-cost devices where size and durability weren’t critical.

To ensure the durability and longevity of the chips, the concept of IC packaging evolved, providing mechanical protection, heat dissipation, and easier handling during assembly. The IC package plays a crucial role in connecting the internal chip to the external environment, usually through metal leads or solder balls that link the chip to a printed circuit board (PCB).

The structure of most modern IC packages is relatively straightforward:

- **Die:** The core silicon IC where all the operations happen.
- **Die Attach/Die Pad:** A platform that holds the die in place.
- **Wire Bonds or Flip-Chip Connections:** Connecting the die to external leads or pads.
- **Lead frame or interconnect:** Connecting the wire bonds to the leads or solder balls that attach to the PCB
- **Encapsulant (Epoxy):** The protective material covering the die and wires, which is typically made of tough epoxy resin often mixed with fillers like glass beads to enhance durability.

![Example of IC packages](/Other/Images/packages.png)

# Leaded Packages

Leaded packages, such as Dual In-Line Packages (DIP) and Small Outline Integrated Circuits (SOIC), are among the oldest and most recognizable formats. These packages have metal leads extending out from the sides, which are soldered to a PCB. They were widely used in early electronics due to their ease of handling and soldering, but their larger size and bulk made them less suitable for modern, compact electronics.

![SOIC-8 package](/Other/Images/soic8.jpg)

As electronics evolved, the leaded packages got more crowded and smaller, resulting in the introduction of Small-outline package (SOP), a miniaturized version of SOIC and Quad-flat package (QFP) which saw leads poking out from all of the four sides of the package.

In leaded packages, the die is encapsulated in epoxy with the leads (usually made of copper or tin) extending out for easy connection to a circuit board. However, these packages take up significant space on the PCB, which is a major drawback as devices become smaller and more densely packed with components. Consequently, leaded packages are becoming less common, particularly in high-density applications.

## Quad Flat No-lead (QFN) and Similar Packages

The Quad Flat No-lead (QFN) package is one of the most widely used formats today, thanks to its compact form factor and efficient heat dissipation. QFNs are leadless packages where the chip’s contacts are exposed on the underside of the package with much smaller footprint than traditional leaded packages.

![QFN-40 package](/Other/Images/qfn40.jpg)

The structure of QFNs still includes the die mounted onto a lead frame, but the leads are encapsulated underneath, making the package thinner and more space-efficient. The use of QFNs and similar leadless packages has become especially popular in mobile devices, wearables, and other applications where space is at a premium.

##Ball Grid Array (BGA)

The Ball Grid Array (BGA) package represents a further evolution in packaging. Instead of leads or pads, BGAs use a matrix of solder balls on the underside of the package to connect to the PCB. This design offers several advantages:

- Smaller footprint: By placing the connections under the chip, BGAs save significant space on the PCB.
- Improved thermal performance: The package design facilitates better heat dissipation.
- Higher pin count: BGAs allow for more connections without increasing the package size, making them ideal for high-performance chips.

![BGA-24 package](/Other/Images/bga24.jpg)

BGAs are commonly used in microprocessors, RAM, GPUs, and other high-density chips. The array of solder balls underneath and their smaller size makes them more challenging to handle and solder manually, often requiring specialized equipment for rework.

## Chip-Scale Packages (CSP) and Wafer-Level Chip-Scale Packages (WLCSP)

As the demand for smaller, more efficient devices grows, packaging technology has reached a point where the package itself is barely larger than the chip. Chip-Scale Packages (CSP) are defined as packages where the package size is no more than 20% larger than the die itself.

![WLCSP package](/Other/Images/wlcsp.jpg)

The most recent development of CSP is the Wafer-Level Chip-Scale Package (WLCSP). In WLCSP, the die is packaged directly at the wafer level before being cut and placed into devices. This reduces the packaging overhead to almost nothing, making WLCSP the smallest and most space-efficient package available. WLCSPs are widely used in mobile phones, sensors, and other ultra-compact electronics where size is critical.

One interesting challenge with WLCSPs, especially in the context of Laser Fault Injection (LFI), is the thinness of the molding compound. In some cases, the encapsulant is so thin that it might be sensitive to the laser even without decapping. This opens up possibilities for direct fault injection without the need to physically remove the package material, allowing for quicker and more efficient attacks on WLCSP chips compared to older, more robust packages.

# Packaging Composition

While there are various materials used in IC packaging, epoxy-based packages are by far the most common and notoriously challenging to deal with when attempting decapping. This is why, for the purpose of this post, we’ll focus solely on epoxy-based packaging. Understanding the composition of the epoxy and its interaction with other materials within the package is crucial when developing a decapping strategy, particularly if the goal is to keep the chip functional after decapping.

## What is Epoxy Packaging?

Epoxy packaging is the protective (almost always black) material to encapsulate the die, providing mechanical support, environmental protection, and electrical insulation. The epoxy-based packaging materials are extremely durable and heat resistant, making them ideal for long-term use in various applications. However, this durability is in our case a double-edged sword— while it protects the chip from external damage, it also makes decapping quite difficult.

Epoxy-based packaging is typically composed of the following elements:

**Epoxy Resin**
The main component of the package, the epoxy resin, serves as the binding agent that holds everything together. It forms the matrix in which other elements, such as fillers, are dispersed. Epoxy is highly resistant to chemicals, mechanical stress, and heat, which makes it difficult to remove.

**Fillers (e.g., Glass Beads, Silica)**
Fillers are added to improve the mechanical strength and thermal properties of the package. In most epoxy-based IC packages, silica or glass beads are commonly used as fillers. These materials not only enhance the durability of the package but also make it more resistant to thermal expansion, ensuring that the package doesn’t crack or deform under high temperatures. These fillers are incredibly hard, which complicates mechanical decapping processes like milling or grinding. They will cause excessive wear on milling tools.

**Molding Compounds (Additives and Modifiers)**
Epoxy-based packaging often contains additional modifiers and additives to tailor the mechanical properties of the encapsulant. These can include flame retardants, carbon black, plasticizers, and other materials that modify the properties of the package to suit the need. These compounds can for example increase the resistance of the package to acids and solvents, which is why chemical decapping techniques can be ineffective or slow.

## Challenges with Epoxy-Based Packages

The combination of tough epoxy resin and hard fillers like glass beads presents several challenges when attempting to decap a chip.

If too much force is applied during mechanical decapping, there’s a risk of damaging the delicate die underneath.

Epoxy resins are designed to withstand significant heat without deforming. This makes thermal decapping methods less effective, as the heat required to melt or soften the epoxy might exceed the tolerance of the IC itself, potentially destroying the chip.

The additives and modifiers used in the epoxy can make it resistant to chemical decapping methods (acids and solvents). While chemicals like nitric acid or sulfuric acid can dissolve the epoxy over time, the process is slow and dangerous, requiring strict control of the chemicals used.

The distribution of fillers within the epoxy can be non-uniform. In some areas, the concentration of glass beads or silica may be higher, which can lead to unpredictable results when mechanically or chemically decapping. Even when using a laser, high concentrations of filler material can cause uneven burns or refraction of the laser beam.

# Decapping Methods

Several methods exist for decapping epoxy-based packages, each with its own set of advantages, disadvantages, and risks. In this chapter, we’ll explore the most common techniques — chemical, mechanical, thermal, and laser decapping — and discuss where they are most applicable, as well as the likelihood of preserving chip functionality after the process.

## Chemical Decapping (Acids and Solvents)

Chemical decapping involves using acids or solvents to dissolve the epoxy encapsulant surrounding the die. This method has been used for decades, primarily due to its effectiveness in attacking the epoxy without needing direct mechanical intervention. The process typically uses nitric acid, sulfuric acid, or a combination of both to break down the packaging material.

The process itself is straightforward: the chip is submerged in acid, which eats away at the epoxy layer over time. Nitric acid dissolves the organic components of the epoxy, while sulfuric acid can assist by burning off any remaining residues. This method is highly effective for most packages, especially those that do not incorporate filler materials designed to enhance chemical resistance.

The main advantage of chemical decapping is that it requires minimal physical contact with the chip. Because the process is entirely chemical, there’s no risk of damaging the chip through mechanical means like grinding or cutting. It’s also relatively inexpensive compared to some of the other methods. **However, chemical decapping presents significant challenges. Handling strong acids like nitric or sulfuric acid is hazardous and requires specialized equipment and strict safety protocols. The fumes are toxic, and there is always the risk of over-exposing the chip to the acid, leading to irreparable damage. Furthermore, depending on the legislation it might not even be legal to own some these chemicals.**

Prolonged exposure to acids can also result in surface damage to the silicon die and leaving the chip in the acids for too long will dissolve the bond wires or leadframe, which will render the chip non-functional.

In summary, while chemical decapping can be effective for certain types of chips, it poses significant risks to the overall integrity of the chip. The likelihood of leaving the chip functional after the process is moderate at best (unless you are John McMaster or Travis Goodspeed).

## Mechanical Decapping

Mechanical decapping, as the name implies, involves physically removing the encapsulant by milling, grinding, or cutting it away. This method is good because it doesn’t require the dangerous chemicals associated with acid decapping, and it offers more direct control over the process. Mechanical decapping can be performed using cheap tools such as a Dremel rotary tool or a CNC mill (if you have access to one). Both tools allow precise material removal by grinding away the epoxy layer bit by bit.

This methodology is presented on the index page of this repository.

One of the main advantages of mechanical decapping is that it can be performed with relatively simple equipment, making it an attractive option for hobbyists or researchers who lack access to specialized tools or chemicals. Additionally, the risk of chemical damage to the die is eliminated since the process relies solely on physical force.

There are several drawbacks, the process is slow and labor-intensive, particularly when trying to avoid damaging the die. More importantly, there’s a significant risk of accidentally applying too much force or grinding too deeply, which could ruin the chip and make it unusable.

It is possible repeatedly to succeed with mechanical decapping with some caution and precision, but the margin for error is quite small.

## Thermal Decapping

Thermal decapping is less common than chemical or mechanical methods but can be used in certain circumstances where the package material is thermally sensitive. The process involves applying heat to the package to soften or melt the epoxy, allowing the encapsulant to be peeled away or softened for easier removal. This method can be applied using a heat gun, hot plate, or other thermal sources.

The primary advantage of thermal decapping is that it avoids direct chemical exposure or mechanical abrasion, both of which carry risks of damaging the die.

However, this method is not widely used due to its limitations. Most modern epoxy materials are formulated to be heat resistant, meaning that applying enough heat to soften the encapsulant would also destroy the silicon die or degrade the chip’s functionality. Heat can also cause warping or delamination of the package, making it difficult to achieve clean results. In short, thermal decapping has limited use in practical applications and offers a very low likelihood of leaving the chip functional after the process.

## Laser Decapping

Laser decapping is as the name suggest, using a laser beam to vaporize or ablate the encapsulant material. This method offers several advantages over chemical, mechanical, and thermal decapping techniques, primarily due to its precision and non-contact nature. With a properly tuned laser, the encapsulant can be removed layer by layer, allowing for a highly controlled decap process.

A laser with sufficient power can vaporize the epoxy and the glass beads without damaging the die. The laser beam and its power can be very precisely controlled, making it possible to decap the chip quickly without compromising its functionality. One of the most significant benefits of laser decapping is its speed. While chemical or mechanical decapping can take tens of minutes or even days, laser decapping can be completed in a matter of seconds.

The laser power and pulse duration must be carefully adjusted to avoid overheating the die or causing unwanted damage. While the process is more forgiving than mechanical methods, incorrect laser settings can still result in damage to the die or surrounding components.

Based on our testing, laser decapping offers the highest likelihood of leaving the chip functional after the process. The precision, speed, and non-contact nature of laser decapping make it the preferred choice for modern IC packages, especially when working with high-value or complex chips.

# Laser Decapping Using Our Low-cost LFI Rig

One of the most groundbreaking features of our low-cost Laser Fault Injection (LFI) rig is its dual functionality. The same rig that you use for LFI attacks can also be used for laser decapping, making it an incredibly versatile tool. This capability drastically simplifies the decapping process, as you can decap and then immediately move on to glitching the chip — no need to switch between different equipment or complicated setups. By using our rig, you save time, space, and the hassle of working with multiple devices.

Once the chip is secured, the rig’s 2W infrared laser can be used to quickly and effectively remove the epoxy encapsulant. In our experiments, we’ve found that it takes just three to six quick laser passes of about three seconds each to completely eat away the epoxy and expose the die pad. Once the die pad is revealed, it easily lifts off, giving you clean access to the die.

![Laser decapped chip](/Other/Images/laser-decap.jpg)

What sets this process apart is its speed and reliability. From start to finish, the entire decapping procedure takes less than a minute, with a repeatable success rate of close to 100%. This level of integration and efficiency makes our LFI rig one of the most capable tools available for both decapping and glitching, bringing high-end lab functionality into a cost-effective, compact setup.

We will start to collect and publish rig parameters and various notes under the decapping folder such as die pad location and size for each of the chips we have put underneath the rig. This should make it easier to repeat the process in the future when you want to attempt LFI for specific chip.

**IMPORTANT NOTE:** Before you try this ensure you have adequate fume extraction as the fumes emitted from the burning epoxy, fillers and additives in the coating can be very toxic to inhale. We are performing this in a sealed enclosure with Weller fume extractor that has active carbon filter.

**IMPORTANT NOTE2:** Fire hazards, as you are giving laser treatment for the epoxy, even though it has flame retardants, there is still a risk of combustion. Never leave the rig without supervision when doing this and have fire extinguisher at hand just in case.

# Step-by-step Guide

The first step in the process is that you need to acquire a few of the same chips you are working with. The reason for this is that before decapping you will need to know the structure of the chip. The most important thing to know is where the die pad is and what is its shape and size. This allows you to tune the decapping area for the laser to be just the right size and limit any possible damage.

## Research and Sacrificial Chip
Use either the laser or mechanical decapping to remove the epoxy from the entire bottom (or top if you are dealing with flip-chip BGA) of the chip until you get to the die pad. This should be done little by little to take note of anything that comes across in the layers. Once you hit the die pad, measure the size of it and see how it is attached to the leadframe. Sometimes you might have to go a bit deeper on the corners to fully reveal the mounting points. Take a careful note of the amount of passes you will have to do with the laser to get to this point.

## Trying On a Fresh Chip
Now that you know the die pad location, size and mounting style, you also know the amount of passes it is required to be done by the laser to get to the die pad, it is time to try it on a fresh chip. Perform the laser decap on a fresh chip using the settings collected from the previous step and adjust if necessary.

## Peel off the Die Pad
After the laser treatment the die pad should be visible and should in most cases peel of very easily with a sharp knife from one of the sides. Make sure you cut any mounting points before trying to peel the die pad off. The heat generated by the laser in most cases weakens the bond the epoxy has with the die pad making it really easy to peel off.

![Decapped chip with die pad removed](/Other/Images/laser-decap-process.png)

This is the only part where there is a risk of damaging something, if the die pad doesn’t peel of easily, use the laser to get a bit more material off around the sides of the die pad. Although Star Wars tells you to “use the force”, this is not the right place for it. The less you use physical force, the less risk of damage.

## Cleaning and Testing
Clean the exposed die using isopropanol alcohol (IPA) to get the thermal adhesive off and test that the chip still works. This is one of the reasons why it is good to have a fresh chip, you can have debug access to the chip and verify it works as intended.

![Die cleaned with IPA](/Other/Images/laser-decap-die.jpg)

## Rinse and Repeat
If the chip worked as it should then it is time to rinse and repeat the same process for the actual chip you want to attack. Once you have the die visible you can start attacking it using LFI.

# Laser Settings

Provided that you are using the same Sculpfun 2W IR laser we introduced in our setup, here are some baseline settings we have found to be a good starting point for most chips. Note, as each setup is slightly different depending on the lens choices etc the parameters can vary quite a bit.

**Laser power:** 80% PWM duty

**Vertical Hop:** 5

**Horizontal Hop:** such that it takes around 3–5 seconds to do one pass

**Number of passes:** 3–6, has been most of the time enough to reveal die pad

**Dimensions:** depending on your chip but in our experiments your settings should be pretty good if you do one pass of 4mm x 4mm area in about 3–5 seconds.


The 2W IR laser is not powerful enough (at least without significant amount of passes) to cut the die pad even though it is very thin copper. So the best thing is to just try and eat the epoxy off around the die pad and then peel the die pad off.

# Conclusion

In this post, we explored the intricacies of chip decapping, from understanding the various packaging formats and materials used in epoxy-based packages, to examining the pros and cons of different decapping methods such as chemical, mechanical, and thermal approaches. We then introduced the revolutionary ability of our low-cost LFI rig to perform laser decapping using the same 2W IR laser used for glitching. This dual-functionality not only simplifies the decapping process but makes it faster and more efficient than traditional methods, allowing users to decap a chip and immediately proceed to glitching within minutes. With this versatile rig, we’re breaking new ground in hardware security testing, making advanced techniques accessible to a broader audience.
