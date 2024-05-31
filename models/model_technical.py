import os

import mplfinance as mpf
import pandas as pd
import plotly.graph_objects as go
import pytz

from project_path import PROJECT_ROOT_DIR

TICKER_NAME_MAPPING = {
    '7731': 'Marx',
    '6932': 'Merdury'

}


def load_data(ticker_code: str,
              convert_timezone: bool = True,
              ) -> pd.DataFrame:
    """

    :param convert_timezone:
    :param ticker_code:
    Usage:
    >>> ticker_code = '7731'
    """
    file_path = os.path.join(PROJECT_ROOT_DIR, 'data', 'bbg_data.xlsx')
    df = pd.read_excel(file_path, sheet_name=ticker_code)
    df = df[['Unnamed: 0', 'LAST_PRICE', 'VOLUME', 'OPEN', 'HIGH', 'LOW']].rename(columns={'Unnamed: 0': 'date_time',
                                                                                           'OPEN': 'Open',
                                                                                           'LAST_PRICE': 'Close',
                                                                                           'HIGH': 'High',
                                                                                           "LOW": 'Low',
                                                                                           'VOLUME': 'Volume'

                                                                                           })
    df['date_time'] = pd.to_datetime(df['date_time'])
    for col in ['Close', 'Open', 'High', 'Low', 'Volume']:
        df[col] = pd.to_numeric(df[col])
    df = df.set_index('date_time')
    if convert_timezone:
        local_timezone = pytz.timezone('US/Eastern')
        df.index = df.index.tz_localize(local_timezone).tz_convert('Asia/Taipei')

    return df

# **** simple MACD ****
# *********************


# **** plotting ****
# ******************
def plot_candle_stick_mpl(ticker_code: str):
    plot_df = load_data(ticker_code)
    # apdict = mpf.make_addplot(sell_df['Price'], type='scatter', markersize=200, marker='^')
    mpf.plot(plot_df,
             type="candle",
             title=TICKER_NAME_MAPPING[ticker_code],
             style="yahoo",
             volume=True,
             figratio=(12.00, 5.75),
             returnfig=True,
             show_nontrading=False,
             # addplot=apdict
             )


def plot_candle_stick_plotly(ticker_code: str):
    """

    :param ticker_code:
    usage:
    >>> ticker_code = '7731'
    """
    plot_df = load_data(ticker_code)
    fig = go.Figure(data=[go.Candlestick(x=plot_df.index,
                                         open=plot_df['OPEN'],
                                         high=plot_df['HIGH'],
                                         low=plot_df['LOW'],
                                         close=plot_df['LAST_PRICE'])
                          ])

    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()
