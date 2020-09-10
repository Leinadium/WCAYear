# World Map of WCA Competitions

A Python script to visualize all the competitions announced at
worldcubeassociation.org

## Requeriments

matplotlib and cartopy, as well as requests, datetime and json.

## How to use

1. Download all requeriments. Edit INITIAL_DATE in main.py, and then run.

2. Enter 'U' to update competitions from WCA's API, or left empty if it is
already up to date. It will create all frames at frames/

3. To generate a video, you can use ffmpeg:
`ffmpeg -framerate 15 -i frames\frame%4d.png -c:v h264 -r 30 -s 1920x1080 test.mp4`

## Credits

..* (Mat Leornard)[https://medium.com/udacity/creating-map-animations-with-python-97e24040f17b]
..* (WorldCubeAssociation API)[https://www.worldcubeassociation.org/api/v0/]
..* matplotlib and cartopy documentation.

