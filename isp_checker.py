#!/usr/bin/env python3

import argparse
import datetime
import os

import matplotlib.pyplot as plt

import pandas

import plotly
import plotly.graph_objs as go

import speedtest


def DownloadTest(my_isp: str = None):
    """
    Run the download test and return download, upload and ping values

    @param: Nothing

    @return: Download and upload values in Mbits/second and ping value in ms
    """
    try:
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
    except speedtest.ConfigRetrievalError:
        res = {'timestamp': f"{datetime.datetime.utcnow().isoformat()}Z",
               'download': -1.0,
               'upload': -1.0,
               'ping': -1.0,
               'client': {'isp': my_isp}
               }

    # We could return the entire json element,
    # it's just as simple to read/plot in python, but lets not
    return res['timestamp'], res["download"], res["upload"], res["ping"], res["client"]["isp"]


def PrintTestResults(my_isp: str = None):
    """
    Initiate the speed test and return the results with a timestamp

    @param: Nothing

    @return: str with timestamp and speed test results
    """
    timestamp, down, up, ping, isp = DownloadTest(my_isp)
    Mbits = 1024*1024
    return "{},{},{:.2f},{:.2f},{:.2f},".format(timestamp, isp, ping, down/Mbits, up/Mbits)


def WriteTestResults(outfile):
    """
    Append the test results to <outfile>, creating the file if it doesn't exist

    @param: The file to write to

    @return: Nothing
    """
    HEADER = "Timestamp,ISP,Ping (ms),Download (Mbit/s),Upload (Mbit/s),Comments\n"

    if os.path.exists(outfile) is not True:
        f = open(outfile, "w")
        f.write(HEADER)

    f = open(outfile, "a")
    f.write(PrintTestResults() + '\n')


def ReadDatafile(infile):
    """
    Read the given data file into a pandas dataframe,
    then extract the required columns for plotting

    @param: The data file to read

    @return: A panda dataframe containing date and download speed
    """
    data = pandas.read_csv(infile, parse_dates=['Timestamp'],
                           date_parser=lambda x: pandas.to_datetime(x))

    requiredColumns = ['Timestamp', 'Download (Mbit/s)', 'Comments']
    data = data[requiredColumns]
    niceNames = {'Timestamp': 'Date', 'Download (Mbit/s)': 'Speed Results', 'Comments' : 'Comments'}
    data = data.rename(columns=niceNames)

    return data


def StaticPlot(data):
    """
    Use matplotlib functionality to plot the data

    @param: The panda dataframe to plot

    @return: Nothing
    """
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 7))

    currentAxes = axes[0]

    currentAxes.set_xlabel("Speed [Mbits/s]")
    currentAxes.set_ylabel("Count")
    data.hist(ax=currentAxes, bins=30)

    currentAxes = axes[1]

    dl_max = data['Speed Results'].max()+5
    currentAxes.set_ylim(bottom=0.0, top=dl_max)
    currentAxes.set_ylabel("Speed [Mbits/s]")

    currentAxes.set_xlabel("Date")

    data.plot(x='Date', y='Speed Results', ax=currentAxes, legend=False)

    plt.tight_layout()
    plt.show()


def DynamicPlot(data):
    """
    Use plotly functionality to create a dynamic plot of the data

    @param: The panda dataframe to plot

    @return: Nothing
    """
    trace = go.Scatter(hovertext=data['Comments'],
                       x=data['Date'],
                       y=data['Speed Results']
                       )

    layout = go.Layout(
        xaxis=dict(title='Date', zeroline=False, rangeslider=dict(visible=True)),
        yaxis=dict(title='Download Speed [Mbits/s]', zeroline=False),

        title='Internet download speeds',
        showlegend=False
    )

    fig = go.Figure(data=[trace], layout=layout)
    plotly.offline.plot(fig,
                        validate=False,
                        filename='ispchecker_plotly.html',
                        auto_open=False
                        )


def main(args):
    """
    High level function to read, parse and plot the data

    @param: An instance of argparse, contain the give options

    @return: Nothing
    """
    options = args.parse_args()

    if options.infile is not None:
        data = ReadDatafile(options.infile)

        if options.static:
            StaticPlot(data)
        else:
            DynamicPlot(data)
    else:
        if options.outfile is not None:
            WriteTestResults(options.outfile)
        else:
            print(PrintTestResults(options.provider))


def parse_arguments():
    """
    Encapsulate the use of argparse

    @param: None

    @return: An instance of argparse
    """
    parser = argparse.ArgumentParser(description="Track internet download speed")

    # Required
    # None

    # Optional
    parser.add_argument("-o", "--outfile",
                        help="File to write results to [default:%(default)s]",
                        default=None,
                        type=str)

    parser.add_argument("-i", "--infile",
                        help="File to read and plot [default:%(default)s]",
                        default=None,
                        type=str)

    parser.add_argument("-s", "--static",
                        help="Create static graphs(s) rather than a dynamic html page [default:%(default)s]",
                        dest="static",
                        action="store_true")

    parser.add_argument("-p", "--provider",
                        help="Value to use as ISP if the connection is down",
                        default="Virgin Media",
                        type=str)
    return parser


if __name__ == '__main__':
    main(parse_arguments())
