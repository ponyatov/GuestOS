# System sturcture

## Emulator (in Python)



```
Hello // World << left >> right
```
will be parsed to
```
<operator://> @7f6144ee45f8
        0 = <symbol:Hello> @7f6144ee44e0
        1 = <operator:<<> @7f6144ee47b8
                0 = <symbol:World> @7f6144ee46d8
                1 = <operator:>>> @7f6144ee4940
                        0 = <symbol:left> @7f6144ee4860
                        1 = <symbol:right> @7f6144ee49e8
```
