# Voyager1

this program plots the Voyager 1 telemetry signal collected by the Breakthrough Listen group (UC Berkeley) with the Green Bank Telescope.
The data file can be downloaded here:
https://drive.google.com/open?id=1jtywUX3rDYQpu6-REgBn1Y95nZlm1CDh

This file is made of 28,623,963 double complex samples (64+64 bits) organized as [real(1),imag(1),real(2),imag(2),...] over a 97.6563 kHz bandwidth. The central carrier is emitted by the spacecraft at 8,415 MHz. This value DOES NOT take in account the Doppler shift due to the relative movement between the telescope and Voyager 1.

More info here:
https://descanso.jpl.nasa.gov/DPSummary/Descanso4--Voyager_new.pdf
