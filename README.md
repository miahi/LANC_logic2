# LANC decoder for Saleae Logic 2

Based on the LANC description here http://www.boehmel.de/lanc.htm

First add an Async Serial analyzer with bit rate 9600 and standard settings (8 bits per frame / 1 stop bit / no parity / Least Significant Bit First / No inversion / Normal mode) and select it as Input Analyzer for this decoder.

Columns in the decoder:
* inv: inverted (correct) bit value in hex. The LANC protocol uses inverted bits but the start bit is not inverted, so we need to invert every byte after the serial decoding 
* binary: binary value
* command: decoded command; all commands start with C# for easier filtering (just search for C# to list all decoded commands)
* status: decoded camera status (byte 4); all status messages start with S# for easier filtering 
* byte no: the byte number in the LANC frame; frames have 8 bytes