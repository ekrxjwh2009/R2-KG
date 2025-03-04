import sys, os
import pandas as pd
import ast

def compute_metrics_ensemble(csv_file, output_csv="./results/filtered_data_split.csv"):

    try:
        df = pd.read_csv(csv_file)
        if set(["qid", "predictions", "gt_label"]) - set(df.columns):
            raise ValueError("CSV doesn't have header columns")
    except (pd.errors.ParserError, ValueError):
        df = pd.read_csv(csv_file, header=None)
        if df.shape[1] != 3:
            raise ValueError("CSV file column number doesn't match")
        df.columns = ["qid", "predictions", "gt_label"]
    

    df["qid"] = df["qid"].astype(int)
    df["gt_label"] = df["gt_label"].astype(bool)
    

    df["predictions"] = df["predictions"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    

    def resolve_prediction(predictions):
        predictions = [str(p).strip().lower() for p in predictions]
        if "abstain" in predictions or len(set(predictions)) > 1:
            return "Abstain"
        return predictions[0] in ["true", "1"]  
    
    df["final_prediction"] = df["predictions"].apply(resolve_prediction)

    df.to_csv(output_csv, index=False)
    
    # Abstain
    valid_df = df[df["final_prediction"] != "Abstain"].copy()
    
    # coverage 
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples
    
    valid_df["final_prediction"] = valid_df["final_prediction"].astype(int)
    y_true = df.loc[valid_df.index, "gt_label"].astype(int)
    y_pred = valid_df["final_prediction"]
    
    # Hit metric
    hit = (y_true == y_pred).mean()
    

    return {
        "Coverage": coverage,
        "Hit": hit
    }


def merge_files(file_paths, output_csv="./results/filtered_data_split.csv"):

    dfs = [pd.read_csv(file, header=None, names=['id', 'prediction', 'gt_label']) for file in file_paths]
    merged_df = pd.concat(dfs)

    merged_df['prediction'] = merged_df['prediction'].apply(lambda x: [str(x)])

    grouped_df = merged_df.groupby(['id', 'gt_label'])['prediction'].sum().reset_index()

    grouped_df = grouped_df[['id', 'prediction', 'gt_label']]

    grouped_df.to_csv(output_csv, index=False, header=False)
    return grouped_df


if __name__ == '__main__':
    # python metric.py file1 file2 file3 outputpath
    # OR
    # python metric.py file1 outputpath
    # outputpath should be .csv format
    filelist = sys.argv[1:-1]
    outputpath = sys.argv[-1]

    for f in filelist:
        assert os.path.isfile(f), 'File not exist : {0}'.format(f)
    
    if '.csv' not in outputpath: fp = outputpath + '.csv'
    else: fp = outputpath

    grouped_df = merge_files(filelist, fp)
    metrics = compute_metrics_ensemble(fp, fp)
    print(metrics)