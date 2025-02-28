import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from ast import literal_eval
from difflib import get_close_matches
from functools import reduce
from difflib import get_close_matches

def compute_metrics(csv_file, output_csv="filtered_data.csv"):

    try:
        df = pd.read_csv(csv_file)
        if set(["qid", "prediction", "gt_label"]) - set(df.columns):
            raise ValueError("CSV doesn't have header columns")
    except (pd.errors.ParserError, ValueError):
        df = pd.read_csv(csv_file, header=None)
        if df.shape[1] != 3:
            raise ValueError("CSV column number doesn't match")
        df.columns = ["qid", "prediction", "gt_label"]
    

    df["qid"] = pd.to_numeric(df["qid"], errors='coerce').dropna().astype(int)

    def process_labels(label_str):
        try:
            label_str = label_str.strip("{} ")  # 중괄호 제거
            labels = literal_eval(label_str) if label_str.startswith("[") else literal_eval('['+label_str+']')
            return set(str(label).strip().lower().replace("\"", "").replace("'", "").replace(" ", "_") for label in labels)
        except (SyntaxError, ValueError, AttributeError):
            return set()
    
    df["gt_label"] = df["gt_label"].apply(process_labels)

    def process_predictions(pred, gt_labels):
        try:
            pred = pred.strip("{} ")  # 중괄호 제거
            labels = literal_eval(pred) if pred.startswith("[") else literal_eval('['+pred+']')
            pred_set = set(str(label).strip().lower().replace("\"", "").replace("'", "").replace(" ", "_") for label in labels)
            

            for pred_label in list(pred_set):
                closest_match = get_close_matches(pred_label, gt_labels, n=1, cutoff=0.7)
                if closest_match:
                    pred_set.remove(pred_label)
                    pred_set.add(closest_match[0])
            
            return pred_set
        except Exception:
            return set()
    
    df["final_prediction"] = df.apply(lambda row: process_predictions(row["prediction"], row["gt_label"]), axis=1)
    
    # Abstain
    def is_abstain(pred):
        return len(pred) == 0 or "abstain" in pred or "error" in pred
    
    valid_df = df[~df["final_prediction"].apply(is_abstain)].copy()
    
    valid_df.to_csv(output_csv, index=False)
    
    # coverage 
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples if total_samples > 0 else 0
    
    # Multi-label F1 score
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
    
    # Micro-F1 score
    total_tp, total_fp, total_fn = 0, 0, 0
    for true_set, pred_set in zip(y_true, y_pred):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Hit metric
    hit = valid_df.apply(lambda row: 1 if len(row["gt_label"] & row["final_prediction"]) > 0 else 0, axis=1).mean()
    

    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }
    
    
def compute_metrics_ensemble(csv_files, output_csv="./filtered_data2.csv"):

    dfs = []
    for i, file in enumerate(csv_files):
        try:
            df = pd.read_csv(file)
            if set(["qid", "prediction", "gt_label"]) - set(df.columns):
                raise ValueError(f"{file}CSV doesn't have header columns")
        except (pd.errors.ParserError, ValueError):
            df = pd.read_csv(file, header=None)
            if df.shape[1] != 3:
                raise ValueError(f"{file}CSV column number doesn't match")
            df.columns = ["qid", "prediction", "gt_label"]
        df = df.rename(columns={"prediction": f"prediction_{i}"})
        dfs.append(df)
    
    df = pd.concat(dfs, axis=1, ignore_index=False)
    df = df.loc[:, ~df.columns.duplicated()].copy()  
    
    def process_labels(label_str):
        try:
            labels = literal_eval(label_str) if isinstance(label_str, str) else literal_eval('['+label_str+']')
            return set(str(label).strip().lower().replace("'", "").replace(" ", "_") for label in labels)
        except (SyntaxError, ValueError, AttributeError):
            return set()
    
    df["gt_label"] = df["gt_label"].apply(process_labels)
    
    def process_predictions(pred, gt_labels):
        try:
            if isinstance(pred, float) or pred.strip().lower() == "abstain":
                return set(["abstain"])
            # pred_list = literal_eval(pred) if isinstance(pred, str) and pred.startswith("[") else [pred]
            pred_list = literal_eval(pred) if isinstance(pred, str) and pred.startswith("[") else literal_eval('['+pred+']')
            pred_set = set(str(label).strip().lower().replace("'", "").replace(" ", "_") for label in pred_list)
            
            # most similar label with ground truth
            matched_preds = set()
            for pred_label in pred_set:
                closest_match = get_close_matches(pred_label, gt_labels, n=1, cutoff=0.7)
                matched_preds.add(closest_match[0] if closest_match else pred_label)
            return matched_preds
        except Exception:
            return set(["abstain"])
    
    for i in range(len(csv_files)):
        prediction_col = f"prediction_{i}"
        df[prediction_col] = df.apply(lambda row: process_predictions(row[prediction_col], row["gt_label"]), axis=1)
    
    def find_common_prediction(row):
        predictions = [row[f"prediction_{i}"] for i in range(len(csv_files))]
        if any("abstain" in pred for pred in predictions):
            return set(["abstain"])
        common_preds = set.intersection(*predictions)
        return common_preds if common_preds else set(["abstain"])
    
    df["final_prediction"] = df.apply(find_common_prediction, axis=1)
    
    # Abstain 
    valid_df = df[df["final_prediction"].apply(lambda x: "abstain" not in x)].copy()
    
    valid_df.to_csv(output_csv, index=False)
    
    # coverage
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples if total_samples > 0 else 0
    
    # Multi-label F1 score 
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
    
    #Micro-F1 score 
    total_tp, total_fp, total_fn = 0, 0, 0
    for true_set, pred_set in zip(y_true, y_pred):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Hit metric
    hit = valid_df.apply(lambda row: 1 if len(row["gt_label"] & row["final_prediction"]) > 0 else 0, axis=1).mean()
    
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }


    

# Example
#For 2agent method 
# metrics = compute_metrics("./results/single_agent/op_gpt-4o-mini_sup_gpt-4o_iter_15_pr_1_temp_0.95_topp_0.95.csv")
metrics = compute_metrics("/nfs_edlab/jschoi/KG-GPT_v2/MetaQA/results/single_agent/op_gpt-4o-mini_sup_gpt-4o_iter_15_pr_1_temp_0.95_topp_0.95.csv")
print(metrics)

#For Enesmeble methods, they make 3 files for each 3 trials.
metrics = compute_metrics_ensemble(["/nfs_edlab/jschoi/KG-GPT_v2/MetaQA/results/single_agent/op_gpt-4o-mini_sup_gpt-4o_iter_15_pr_1_temp_0.95_topp_0.95.csv",
                                    "/nfs_edlab/jschoi/KG-GPT_v2/MetaQA/results/single_agent/op_gpt-4o-mini_sup_gpt-4o_iter_15_pr_1_temp_0.95_topp_0.95.csv",
                                    "/nfs_edlab/jschoi/KG-GPT_v2/MetaQA/results/single_agent/op_gpt-4o-mini_sup_gpt-4o_iter_15_pr_1_temp_0.95_topp_0.95.csv"])
print(metrics)