# System sturcture

## Emulator (in Python)

Lite `GuestOS` system emulator was first written in Python before the system
implementation in Rust. It was done to prototype some elements used in `GuestOS`
to debug and test language-specific problems out of the whole system run.

`GuestOS.py` emulator does not contain the full system model, but only contains
the alternative and very limited implementation of the `metaL` language core.

This expression in [metaL](metaL.md)
```
`Hello // `World << `left >> `right
```
will be parsed to this like AST (in form of object graph)
```
<operator://> @7f42dad60550
	0 = <operator:`> @7f42dad60390
		0 = <symbol:Hello> @7f42dad60470
	1 = <operator:>>> @7f42dad60940
		0 = <operator:<<> @7f42dad60780
			0 = <operator:`> @7f42dad605f8
				0 = <symbol:World> @7f42dad606a0
			1 = <operator:`> @7f42dad607b8
				0 = <symbol:left> @7f42dad60860
		1 = <operator:`> @7f42dad60400
			0 = <symbol:right> @7f42dad609e8
```
and then evaluated to
```
<symbol:Hello> @7f42dad60470
	0 = <symbol:World> @7f42dad606a0
		symbol = <symbol:left> @7f42dad60860
		right = <symbol:right> @7f42dad609e8
```
