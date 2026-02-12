# Introducing Pico-Beam! Laser Communication for the Raspberry Pi Pico!

### What is Pico-Beam?

Pico-beam is a simple laser communication system that runs on the Raspberry Pi Pico microcontroller. 
So far, the project allows for users to send and receive data using a laser and receiver. Data is 
transmitted by turning the laser diode on and off rapidly and uses a custom communication protocol
that includes synchronizing the transmitter and receiver and send data which is decoded on the
receiving end. At the moment, communication is only 1 way but we are working on a 2 way system.

### What are the specs?

These specs will not be scientific at all. These measurements are based off of rough observations.

Each packet consists of 48 bytes in total. 8 bytes are allocated to the header, 32 bytes for the payload 
and 8 bytes for parity/checksum.

The highest clock rate we have reliably achieved is 50Hz transmitting 50 bits per second. Faster speeds
are achievable but error rates increase and our code needs to be optimized to handle such speeds.
