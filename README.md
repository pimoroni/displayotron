![Display-o-Tron 3000](display-o-tron-logo.png)

Library and examples for the Display-o-Tron HAT (_DotHAT_) and Display-o-Tron 3000 (_Dot3K_) Raspberry Pi add-on boards from [Pimoroni](https://pimoroni.com).

* Display-o-Tron HAT (for all Rasperry Pi models with 40-pin headers): https://shop.pimoroni.com/products/display-o-tron-hat
* Display-o-Tron 3000 (for all Raspberry Pi models): ~~http://shop.pimoroni.com/products/displayotron-3000~~ (no longer on sale)


## Using Python?

We've created a super-easy installation script that will install all pre-requisites and get your Display-o-Tron up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type:

```bash
curl -sS get.pimoroni.com/displayotron | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/displayotron`, but you can also check out the Basic and Advanced examples for both DotHAT and Dot3k in: [examples](examples)

We've also created a full [function reference](documentation/REFERENCE.md).

### Checking which Display-o-Tron product you have

Make sure you run the right examples for your product, if you've got a Display-o-Tron 3000 you should be using the examples in `/home/pi/Pimoroni/displayotron/dot3k` and if you have a Display-o-Tron HAT you should be using the ones in `/home/pi/Pimoroni/displayotron/dothat`*


The Display-o-Tron HAT looks like this:
![Display-o-Tron HAT image](https://cdn.shopify.com/s/files/1/0174/1800/products/Display-o-tron_HAT_1_of_2_1024x1024.JPG)

The Display-o-Tron 3000 looks like this:
![Display-o-Tron 3000 image](https://cdn.shopify.com/s/files/1/0174/1800/products/IMG_5944_1024x1024.png)


## Documentation & Support

* Getting started with Display-o-Tron 3000 - https://learn.pimoroni.com/tutorial/display-o-tron/getting-started-with-display-o-tron
* Tutorials - https://learn.pimoroni.com/?tag=display-o-tron
* Display-o-Tron 3000 Pinout - https://pinout.xyz/pinout/display_o_tron_3000
* Display-o-Tron HAT Pinout - https://pinout.xyz/pinout/display_o_tron_hat
* Get help - http://forums.pimoroni.com/c/support

## Other Languages

* NodeJS: https://github.com/jorisvervuurt/JVSDisplayOTron
* C/C++: https://github.com/akx/dot3k-c

## Resources

* http://www.lcd-module.com/eng/pdf/doma/dog-me.pdf - DOG LCD Datasheet ( Includes character table )

## Credits

* http://www.jan-holst.dk/pi-radio/pi-radio.html - for initial inspiration to do a Radio plugin
* http://rollcode.com/use-python-get-raspberry-pis-temperature/ - for guidance on getting CPU/GPU temp in Python
* https://github.com/facelessloser/Atmega_screen - for stock ticker plugin
