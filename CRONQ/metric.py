import sys, os
import pandas as pd
from ast import literal_eval

def compute_metrics_ensemble(csv_files, output_csv="./results/filtered_data_split.csv"):
    dfs = []
    
    for i, file in enumerate(csv_files):
        try:
            df = pd.read_csv(file)  
            if set(["qid", "prediction", "gt_label"]) - set(df.columns):
                raise ValueError(f"{file} CSV doesn't have header columns")
        except (pd.errors.ParserError, ValueError):
            df = pd.read_csv(file, header=None)
            if df.shape[1] != 3:
                raise ValueError(f"{file} CSV column number doesn't match")
            df.columns = ["qid", "prediction", "gt_label"]
        
        df = df.rename(columns={"prediction": f"prediction_{i}"})
        dfs.append(df)
    
    df = pd.concat(dfs, axis=1, ignore_index=False)
    df = df.loc[:, ~df.columns.duplicated()].copy()
    ordering = [col for col in df.columns if col != 'gt_label'] + ['gt_label']
    df = df[ordering]

    # GT Label
    def process_labels(label_str):
        if pd.isna(label_str):
            return set()
        try:
            labels = literal_eval(label_str) if isinstance(label_str, str) and label_str.startswith("[") else [label_str]
            return set(str(label).strip().lower().replace("'", "") for label in labels if label)
        except (SyntaxError, ValueError, AttributeError):
            return set()

    df["gt_label"] = df["gt_label"].apply(process_labels)
    
    # Prediction
    def process_predictions(pred, gt_labels):
        if pd.isna(pred):
            return {"abstain"}
        try:
            if isinstance(pred, float) or pred.strip().lower() == "abstain":
                return {"abstain"}
            
            # 1. Try parsing as a set or list first
            if isinstance(pred, str) and (pred.startswith("[") or pred.startswith("{")):
                pred_list = list(literal_eval(pred))  # Convert to list
        
            else:
                # 2. Check if the prediction is a single entity with a comma and matches a gt_label
                if pred.strip().lower() in gt_labels:
                    pred_list = [pred.strip()]
                else:
                    # 3. Split incorrectly formatted predictions
                    pred_list = [p.strip() for p in pred.split(",")]

            # 4. Ensure entity consistency based on gt_labels
            cleaned_preds = set()
            for pred_label in pred_list:
                pred_label = str(pred_label).strip().lower().replace("'", "")
                if any(pred_label in gt for gt in gt_labels):  # If it's part of a known entity, keep it together
                    for gt in gt_labels:
                        if pred_label in gt:
                            cleaned_preds.add(gt)
                else:
                    cleaned_preds.add(pred_label)

            return cleaned_preds
        except Exception:
            return {"abstain"}
    
    for i in range(len(csv_files)):
        prediction_col = f"prediction_{i}"
        df[prediction_col] = df.apply(lambda row: process_predictions(row[prediction_col], row["gt_label"]), axis=1)
 
    def find_common_prediction(row):
        predictions = [set(row[f"prediction_{i}"]) for i in range(len(csv_files)) if pd.notna(row[f"prediction_{i}"])]
        
        if not predictions:  # NaN 
            return {"abstain"}
        
        if any("abstain" in pred for pred in predictions):
            return {"abstain"}
        
        common_preds = set.intersection(*predictions) if predictions else set()
        return common_preds if common_preds else {"abstain"}
    
    df["final_prediction"] = df.apply(find_common_prediction, axis=1)

    df.to_csv(output_csv, index=False)
    
    # filtering
    valid_df = df[df["final_prediction"].apply(lambda x: "abstain" not in x)].copy()
    
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples if total_samples > 0 else 0
    
    y_true = valid_df["gt_label"]
    y_pred = valid_df["final_prediction"]
    
    def f1_per_sample(true, pred):
        if len(true) == 0 and len(pred) == 0:
            return 1
        tp = len(true & pred)
        fp = len(pred - true)
        fn = len(true - pred)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    sample_f1_scores = valid_df.apply(lambda row: f1_per_sample(row["gt_label"], row["final_prediction"]), axis=1)
    sample_wise_f1 = sample_f1_scores.mean()
    
    total_tp, total_fp, total_fn = 0, 0, 0
    for true_set, pred_set in zip(y_true, y_pred):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    hit = valid_df.apply(lambda row: 1 if len(row["gt_label"] & row["final_prediction"]) > 0 else 0, axis=1).mean()
    
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }


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

    metrics = compute_metrics_ensemble(filelist, fp)
    print(metrics)