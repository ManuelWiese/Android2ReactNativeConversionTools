# Android2ReactNative conversion tools

Port Android resources to ES6 classes.
At the moment porting of colors and strings is supported.

Example usage:
```
python3 convertResources.py ExampleColors.xml
```

```
const colors = {
    White: "#FFFFFF",
    Blue: "#0000FF",
    LightBlue: "#5555FF",
    Black: "#000000",
    Red: "#FF0000",
    DarkRed: "#770000",
    Gray: "#999999",
    DarkGray: "#696969",
    Green: "#007700",
    DarkGreen: "#004400",
    BlueGreen: "#148065",
    Yellow: "#777700"
};

export default colors;
```

