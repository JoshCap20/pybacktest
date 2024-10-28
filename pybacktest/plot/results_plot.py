import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os

### TMP CHAT GPT SOLUTION
## WILL ENHANCE/FIX LATER
## JUST FOR SANITY CHECK CURRENTLY


def plot_backtest(data: pd.DataFrame, output_filename: str, show_plot: bool = False):
    """
    Dynamically plots each stock's data from a MultiIndex DataFrame.
    For each stock, it plots the close price, volume, and separate subplots for indicators like MACD and RSI.
    """
    stocks = data.columns.get_level_values(0).unique()

    for stock in stocks:
        stock_data = data[stock]

        # Identify different types of indicators by keyword in column names
        price_related_indicators = [
            col
            for col in stock_data.columns
            if "Close" in col or "SMA" in col or "EMA" in col
        ]
        rsi_column = next((col for col in stock_data.columns if "RSI" in col), None)
        macd_columns = [col for col in stock_data.columns if "MACD" in col]
        stochastic_columns = [
            col for col in stock_data.columns if "%K" in col or "%D" in col
        ]

        fig, axes = plt.subplots(
            4,
            1,
            figsize=(14, 12),
            gridspec_kw={"height_ratios": [3, 1, 1, 1]},
            sharex=True,
        )
        ax1, ax_rsi, ax_macd, ax_stochastic = axes

        # Plot the closing price and other price-related indicators on the main axis
        ax1.plot(
            stock_data.index,
            stock_data["Close"],
            label=f"{stock} Close",
            color="blue",
            linewidth=1.5,
        )
        for indicator in price_related_indicators:
            if indicator != "Close":  # Avoid plotting Close twice
                ax1.plot(
                    stock_data.index,
                    stock_data[indicator],
                    label=indicator,
                    linestyle="--",
                    linewidth=1,
                )

        ax1.set_ylabel("Price")
        ax1.set_title(f"{stock} Price and Indicators")
        ax1.legend(loc="upper left", fontsize="small")

        # Plot volume on a secondary y-axis on the main price chart
        ax2 = ax1.twinx()
        ax2.bar(
            stock_data.index,
            stock_data["Volume"],
            color="gray",
            alpha=0.3,
            width=1,
            label="Volume",
        )
        ax2.set_ylabel("Volume")
        ax2.get_yaxis().set_ticks([])

        # Plot RSI if available
        if rsi_column:
            ax_rsi.plot(
                stock_data.index,
                stock_data[rsi_column],
                label=rsi_column,
                color="purple",
                linewidth=1.5,
            )
            ax_rsi.axhline(
                70, color="red", linestyle="--", linewidth=0.7, label="Overbought"
            )
            ax_rsi.axhline(
                30, color="green", linestyle="--", linewidth=0.7, label="Oversold"
            )
            ax_rsi.set_ylabel("RSI")
            ax_rsi.set_ylim(0, 100)
            ax_rsi.legend(loc="upper left", fontsize="small")

        # Plot MACD, Signal Line, and Histogram on its own axis
        macd_line = next(
            (
                col
                for col in macd_columns
                if "MACD" in col and "Signal" not in col and "Histogram" not in col
            ),
            None,
        )
        signal_line = next((col for col in macd_columns if "Signal" in col), None)
        macd_histogram = next((col for col in macd_columns if "Histogram" in col), None)

        if macd_line and signal_line and macd_histogram:
            ax_macd.plot(
                stock_data.index,
                stock_data[macd_line],
                label="MACD",
                color="blue",
                linewidth=1.5,
            )
            ax_macd.plot(
                stock_data.index,
                stock_data[signal_line],
                label="MACD Signal",
                color="red",
                linewidth=1.5,
            )
            ax_macd.bar(
                stock_data.index,
                stock_data[macd_histogram],
                color="gray",
                alpha=0.5,
                label="MACD Histogram",
            )
            ax_macd.set_ylabel("MACD")
            ax_macd.legend(loc="upper left", fontsize="small")

        # Plot Stochastic Oscillator if available
        k_line = next((col for col in stochastic_columns if "%K" in col), None)
        d_line = next((col for col in stochastic_columns if "%D" in col), None)

        if k_line and d_line:
            ax_stochastic.plot(
                stock_data.index,
                stock_data[k_line],
                label="%K Line",
                color="orange",
                linewidth=1.5,
            )
            ax_stochastic.plot(
                stock_data.index,
                stock_data[d_line],
                label="%D Line",
                color="blue",
                linewidth=1.5,
            )
            ax_stochastic.axhline(
                80, color="red", linestyle="--", linewidth=0.7, label="Overbought"
            )
            ax_stochastic.axhline(
                20, color="green", linestyle="--", linewidth=0.7, label="Oversold"
            )
            ax_stochastic.set_ylabel("Stochastic")
            ax_stochastic.set_ylim(0, 100)
            ax_stochastic.legend(loc="upper left", fontsize="small")

        # Set x-axis date formatting and rotate labels for readability
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        fig.autofmt_xdate()

        # Display plot
        plt.tight_layout()
        os.makedirs(f"{output_filename}/plots", exist_ok=True)
        plt.savefig(f"{output_filename}/plots/{stock}.png", bbox_inches="tight")
        if show_plot:
            plt.show()
        plt.close()
