# optical_multilayer

[![PyPI - Version](https://img.shields.io/pypi/v/optical-multilayer.svg)](https://pypi.org/project/optical-multilayer)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/optical-multilayer.svg)](https://pypi.org/project/optical-multilayer)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [About](#about)
- [Functionalities](#functionalities)
- [To Do](#todo)

## Installation

```console
pip install optical-multilayer
```

## License

`optical-multilayer` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## About

Created by David C. Heson, Jack Liu, and Dr. William M. Robertson over the 2022 MTSU Computational Sciences REU (NSF REU Award #1757493).

Codebase created to explore the optical properties of multilayers and optimize their design to achieve maximum sensibilities, using minimas of reflected light and RIU (Refractive Index Unit) as qualitative measurements. A new measurement called SWT (Shift With Thickness) was also introdued, which is defined as the degree or nanometer shift in the location of a Bloch Surface Wave when the bottom layer increases by 10 nanometers in thickness.

Currently, the entirety of the code is written in Python Anaconda 3-5.3.1.

For the scripted version, go to: https://github.com/davidcheson/optical_multilayer.

## Functionalities

The current functionalities of the program are:
<ul>
<li>Input any custom multilayer arrangement into the existing functions, including ones to dynamic indexes of refraction values.</li>
<li>Graph reflection and transmission coefficients across multilayers with changing angle or wavelength, for specific polarisation mode.</li>
<li>Graph the electric field profile accross a multilayer for a specific angle, wavelength, polarisation, and multilayer.</li>
<li>Calculate RIU and SWT values for specified multilayer arrangements.</li>
<li>Explore by force bruting a set of parameters for the multilayers, finding the best setups in terms of RIU/SWT and reflectivity dips.</li>
<li>Simulate the properties of a multilayer using a dynamic index of refraction, which is wavelength dependent and corresponds to a user-defined function.</li>
<li>More to come!</li>
</ul>

## To Do

<ul>
<li>Rewrite matrix calculations using Rust.</li>
<li>Explore how to do a gradient descent on parameter regions of interest.</li>
<li>Improve help and context messaging.</li>
<li>Condense and improve the electric field calculation.</li>
</ul>

Please refer any questions, comments, or suggestions to dch376@msstate.edu.
