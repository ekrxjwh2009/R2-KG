import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
import ast

def compute_metrics_ensemble(csv_file):

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
    
    # Abstain
    valid_df = df[df["final_prediction"] != "Abstain"].copy()
    
    # coverage 
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples
    
    valid_df["final_prediction"] = valid_df["final_prediction"].astype(int)
    y_true = df.loc[valid_df.index, "gt_label"].astype(int)
    y_pred = valid_df["final_prediction"]
    
    # micro-F1 score 
    precision = precision_score(y_true, y_pred, average="micro")
    recall = recall_score(y_true, y_pred, average="micro")
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # sample-wise F1 score 
    sample_f1_scores = f1_score(y_true, y_pred, average=None)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # Hit metric
    hit = (y_true == y_pred).mean()
    

    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }



def merge_files(file_paths):

    dfs = [pd.read_csv(file, header=None, names=['id', 'prediction', 'gt_label']) for file in file_paths]
    merged_df = pd.concat(dfs)

    merged_df['prediction'] = merged_df['prediction'].apply(lambda x: eval(x) if isinstance(x, str) else x)

    grouped_df = merged_df.groupby(['id', 'gt_label'])['prediction'].sum().reset_index()

    grouped_df = grouped_df[['id', 'prediction', 'gt_label']]

    grouped_df.to_csv('merged_predictions_5.csv', index=False, header=False)
    return grouped_df



grouped_df = merge_files(["./results/single_agent/op_qwen_14b_sup_gpt-4o-mini_iter_15_pr_1_temp_0.9_topp_0.9.csv",
                          "./results/single_agent/op_qwen_14b_sup_gpt-4o-mini_iter_15_pr_1_temp_0.9_topp_0.95.csv",
                          "./results/single_agent/op_qwen_14b_sup_gpt-4o-mini_iter_15_pr_1_temp_0.95_topp_0.95.csv"])
metrics = compute_metrics_ensemble("./results/single_agent/op_qwen_14b_sup_gpt-4o-mini_iter_15_pr_1_temp_0.9_topp_0.9.csv")

print(metrics)