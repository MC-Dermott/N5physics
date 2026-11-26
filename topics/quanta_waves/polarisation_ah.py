"""AH — Polarisation."""
import math
import random

from topics.quanta_waves.common_ah import C, L, T, calc, explain_set, fmt, ltx, sig, uni

QT = "Polarisation"

NOTES = r"""
## Polarisation

$$n = \tan i_P$$

- **Plane-polarised** light: the electric field vector oscillates in **one plane** only.
- A **polariser** transmits light polarised in one plane. An **analyser** is a second polaroid used to test it:
  with plane-polarised light, rotating the analyser changes the intensity, with a minimum (zero) every 180°.
- To test whether a source is already polarised, use **one** analyser only: rotate it and look for a change in intensity.
- At **Brewster's angle** the light reflected from an insulator is plane-polarised. The reflected and
  refracted rays are then at 90° to each other.
"""

_MATERIALS = [("glass", 1.51), ("water", 1.33), ("Perspex", 1.49), ("diamond", 2.42), ("ice", 1.31), ("glycerol", 1.47)]


def gen_brewster(level="AH"):
    name, n = random.choice(_MATERIALS)
    ip = math.degrees(math.atan(n))
    kind = random.choice(["angle", "n", "refraction", "between"])
    if kind == "angle":
        return calc(QT, f"Calculate Brewster's angle for light in air reflecting from {name} (refractive index {n}).", ip, "°",
                    [r"n = \tan i_P", rf"{n} = \tan i_P", rf"i_P = {ltx(ip)}^\circ"],
                    wrong=[(math.degrees(math.asin(1 / n)), "That is the critical angle. Brewster: n = tan iP."),
                           (math.atan(n), "Your calculator is in radians.")], notes=NOTES)
    ig = round(ip + random.uniform(-1.5, 1.5), 1)
    if kind == "n":
        ans = math.tan(math.radians(ig))
        return calc(QT, f"Light reflected from a liquid is completely plane-polarised when the angle of incidence is {ig:g}°. "
                        f"Calculate the refractive index of the liquid.", ans, "",
                    [r"n = \tan i_P", rf"n = \tan {ig:g}^\circ = {ltx(ans)}"],
                    wrong=[(1 / math.sin(math.radians(ig)), "That uses the critical angle relationship. n = tan iP.")], notes=NOTES)
    if kind == "refraction":
        return calc(QT, f"Light strikes {name} (refractive index {n}) at Brewster's angle. Determine the angle of refraction.",
                    90 - ip, "°",
                    [r"n = \tan i_P", rf"i_P = {ltx(ip)}^\circ",
                     rf"\theta_r = 90 - i_P = {ltx(90-ip)}^\circ"],
                    wrong=[(ip, "That is Brewster's angle. The reflected and refracted rays are at 90°.")],
                    scaffold=[("What is Brewster's angle?", ip, "°"), ("What is the angle of refraction?", 90 - ip, "°")], notes=NOTES)
    total = sig(2 * ig, 4)
    ans = math.tan(math.radians(total / 2))
    return calc(QT, f"When the reflected light from a transparent block is plane-polarised, the angle between the incident "
                    f"and reflected rays is {total:g}°. Calculate the refractive index of the block.", ans, "",
                [rf"i_P = \frac{{{total:g}}}{{2}} = {total/2:g}^\circ", r"n = \tan i_P", rf"n = {ltx(ans)}"],
                wrong=[(math.tan(math.radians(total)), "Halve the angle: the angle of incidence equals the angle of reflection.")],
                scaffold=[("What is Brewster's angle?", total / 2, "°"), ("What is n?", ans, "")], notes=NOTES)


_EXPLAIN = [
    ("What is meant by plane-polarised light?",
     "Light in which the electric field vector oscillates in one plane only.",
     [("Light which travels in one plane only.", "'Travels' is not accepted: the field **oscillates** in one plane."),
      ("Light in which the electric field vector oscillates in one direction only.", "'Direction' is not accepted: say **plane**."),
      ("Light which oscillates along one axis only.", "'Axis' is not accepted: say **plane**.")],
     "Learn this wording."),
    ("A student wants to find out whether the light from a laptop screen is plane-polarised. Which method is correct?",
     "Hold one polaroid analyser in front of the screen, rotate it and look for a change in light intensity.",
     [("Place a polariser and then an analyser in front of the screen and rotate the analyser.",
       "With a polariser added, any light would appear polarised. Use the analyser only."),
      ("Look at the screen through a stationary polaroid.", "The polaroid must be rotated."),
      ("Rotate the screen and measure its power input.", "Observe the light intensity through an analyser.")],
     "One analyser, rotated, and the observation."),
    ("Plane-polarised light passes through an analyser which is rotated through 360°. What is observed?",
     "The intensity varies smoothly, falling to a minimum (zero) twice in the full turn.",
     [("The intensity is constant.", "That would happen with unpolarised light."),
      ("The intensity falls to zero once.", "Zero occurs every 180°."),
      ("The light switches suddenly between full brightness and darkness.", "The change is gradual.")],
     "Describe a gradual change."),
    ("An analyser views light reflected from glass while the angle of incidence is increased through Brewster's angle. "
     "The analyser is set to block light polarised at Brewster's angle. What is seen?",
     "The light gradually dims, cannot be seen at Brewster's angle, then gradually brightens again.",
     [("The light is bright until Brewster's angle, where it suddenly disappears.", "There is no sudden change."),
      ("The light gets steadily brighter throughout.", "It has a minimum at Brewster's angle."),
      ("Nothing changes, because reflected light is never polarised.", "It is polarised at Brewster's angle.")],
     "The change must be gradual."),
    ("Why can polaroid sunglasses reduce glare from a water surface?",
     "The reflected light is partly or completely plane-polarised, and the polaroid is oriented to absorb that plane.",
     [("The polaroid reflects all light from below.", "It acts as an analyser."),
      ("Water only reflects ultraviolet light, which polaroid blocks.", "The effect is polarisation by reflection."),
      ("The polaroid reduces the wavelength of the reflected light.", "Wavelength is unchanged.")],
     "Polarisation on reflection, strongest near Brewster's angle."),
    ("Can sound waves in air be polarised?",
     "No, because sound is a longitudinal wave.",
     [("Yes, using a suitably large polaroid.", "Only transverse waves can be polarised."),
      ("No, because sound travels too slowly.", "Speed is not the reason."),
      ("Yes, because sound can be reflected.", "Reflection does not make a longitudinal wave polarisable.")],
     "Only transverse waves can be polarised."),
]
gen_polarisation_explain = explain_set(QT, _EXPLAIN, NOTES)
