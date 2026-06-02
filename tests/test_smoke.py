import os
import subprocess


def test_imports():
    import etl.utils
    import etl.extract_csv
    import etl.extract_api
    import etl.extract_web
    import etl.extract_pdf
    import etl.transform
    import etl.load
    import etl.train_model


def test_pipeline_runs():
    # run pipeline.py which uses sample_prices.csv
    res = subprocess.run(['python','pipeline.py'], capture_output=True, text=True)
    assert res.returncode == 0
    assert os.path.exists('output/combined_prices.csv')
    assert os.path.exists('output/prices.db')


def test_models_exist():
    assert os.path.exists('models/price_regressor.pkl')
    assert os.path.exists('models/price_classifier.pkl')
