# ISPChecker

Wrapper script around the speedtest-cli [python module](https://pypi.org/project/speedtest-cli/), check out the repository [here](https://github.com/sivel/speedtest-cli).
This script provides a way to either test the speed of your internet connection, or if you have been saving data, plot the variation in speed over time.

## Installation & Setup

Make sure you have the necessary modules installed, simplest way is via [pip](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi).
Explicitly call the python 3 version and lets assume we want to install for the user only.

```bash
pip3 install --user -r requirements.txt
```

The [speedtest module](https://pypi.org/project/speedtest-cli/) will run the actual test, the others are used to read and plot the data.
That should be all that's required, run with the ```-h``` option to see usage and confirm no missing dependencies:

```bash
./isp_checker.py -h
usage: isp_checker.py [-h] [-i INFILE] [-o OUTFILE] [-s]

Track internet download speed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        File to write results to [default=None]
  -i INFILE, --infile INFILE
                        File to read and plot [default=None]
  -s, --static          Create static graphs(s) rather than a dynamic html
                        page [default:False]
```

## Usage

Running with no arguments will run a single speed measurement which, depending on your connection speed, can take up to 30 seconds to return the prompt.
Output will have the following format:

```bash
Timestamp,ISP,Ping (ms),Download (Mbit/s),Upload (Mbit/s),Comment
```

The ```-o``` option can be used to append the data to a specified file.
This should prove useful if you want to create a [long term monitor](#using-as-a-long-term-monitor).

The ```-i``` option can be used to display the data from the specified file.
Data is read into a [pandas](https://pandas.pydata.org/) dataframe then plot with [plotly](https://plot.ly/python/) so you can play with it (default), or more of a summary display graph is created with pandas standard plotting interface if you use the ```-s``` flag.
Currently the project assumes that the file to be plotted has either the same format as that produced with the ```-o``` option, or at the very least has columns labelled ```Timestamp``` and ```Download (Mbit/s)``` and ```Comments```.

## Using as a long term monitor

The primary goal of this project is to provide an easy way to collect data over a prolonged period of time to make sure you are getting the speed you are paying for.
To that end there is a script that can be used in a [cron table](https://en.wikipedia.org/wiki/Cron) to automate this process.
Add the following line to the crontab for the user to have the script run once an hour at the start of the hour.
I have assumed you've cloned this repo into your home directory (and that you are running on a [raspberry pi](https://www.raspberrypi.org/)), if not alter the path as required.
As a sanity check, you can run the [isp_cronjob.sh]() script manually to confirm things run as expected.

```bash
0 * * * * /home/pi/ISPChecker/isp_cronjob.sh
```
If you want a different frequency of testing, consult the [guru](https://crontab.guru/) if you need help with the syntax.
If you aren't sure how to setup a cronjob, [google it](https://askubuntu.com/questions/2368/how-do-i-set-up-a-cron-job).
