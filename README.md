![Display-o-Tron 3000](display-o-tron-logo.png)

Library and examples for the Display-o-Tron 3000 and Display-o-Tron HAT Raspberry Pi add-on boards from Pimoroni

* Display-o-Tron 3000 ( for all Pi models ): http://shop.pimoroni.com/products/displayotron-3000
* Display-o-Tron HAT ( for A+, B+ and Pi 2 ): https://shop.pimoroni.com/products/display-o-tron-hat

##Using python?

We've created a super-easy installation script that will install all pre-requisites and get your Display-o-Tron up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type:

```bash
curl get.pimoroni.com/dot3k | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/dot3k`, but you can also check out the Basic and Advanced examples for both DotHAT and Dot3k in: [python/examples](python/examples)

We've also created a full [function reference](python/REFERENCE.md).

*Make sure you run the right examples for your product, if you've got a Display-o-Tron 3000 you should be using the examples in `/home/pi/Pimoroni/dot3k/dot3k` and if you have a Display-o-Tron HAT you should be using the ones in `/home/pi/Pimoroni/dot3k/dothat`*

##Other Languages

* NodeJS: https://github.com/jorisvervuurt/JVSDisplayOTron

##Resources

* http://www.lcd-module.com/eng/pdf/doma/dog-me.pdf - DOG LCD Datasheet ( Includes character table )

##Credits

* http://www.jan-holst.dk/pi-radio/pi-radio.html - for initial inspiration to do a Radio plugin

* http://rollcode.com/use-python-get-raspberry-pis-temperature/ - for guidance on getting CPU/GPU temp in Python

* https://github.com/facelessloser/Atmega_screen - for stock ticker plugin
