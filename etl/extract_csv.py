import pandas as pd


def load_csv(path):
    df = pd.read_csv(path)
    return df


if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv)>1 else 'sample_prices.csv'
    print(load_csv(p).head())
