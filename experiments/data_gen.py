import argparse

from data_load.dataloader import TranscriptsDataLoader

parser = argparse.ArgumentParser()

parser.add_argument(
    "--data_info_path",
    type=str,
    default="data/ect-v3_train.json",
    help="path to the train data info file",
)
parser.add_argument(
    "--ect_dir",
    type=str,
    default="data/train_ect",
    help="directory of the ECT train files",
)
parser.add_argument(
    "--financial_path",
    type=str,
    default="data/historical_outcomes-ect_train.json",
    help="path to the historical financial data file",
)
parser.add_argument(
    "--output_path",
    type=str,
    default="data/ect_train.json",
    help="path to save the dataset",
)

args = parser.parse_args()

loader = TranscriptsDataLoader(args)
data = loader.load()
loader.save_json(data, args.output_path)
