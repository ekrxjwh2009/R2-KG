import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from ast import literal_eval
from difflib import get_close_matches

def compute_metrics(csv_file, output_csv="filtered_data.csv"):
    # CSV 파일 로드 (헤더 있는 경우와 없는 경우 처리)
    try:
        df = pd.read_csv(csv_file)
        if set(["qid", "prediction", "gt_label"]) - set(df.columns):
            raise ValueError("CSV 파일에 필요한 컬럼이 없습니다. 헤더가 없는 경우를 고려하세요.")
    except (pd.errors.ParserError, ValueError):
        df = pd.read_csv(csv_file, header=None)
        if df.shape[1] != 3:
            raise ValueError("CSV 파일의 컬럼 개수가 예상과 다릅니다. (예상: 3개)")
        df.columns = ["qid", "prediction", "gt_label"]
    
    # 데이터 타입 변환
    df["qid"] = pd.to_numeric(df["qid"], errors='coerce').dropna().astype(int)
    
    # gt_label 변환 (리스트 형태로 변환 후 정리)
    def process_labels(label_str):
        try:
            label_str = label_str.strip("{} ")  # 중괄호 제거
            labels = literal_eval(label_str) if label_str.startswith("[") else label_str.split(",")
            return set(str(label).strip().lower().replace("\"", "").replace("'", "") for label in labels)
        except (SyntaxError, ValueError, AttributeError):
            return set()
    
    df["gt_label"] = df["gt_label"].apply(process_labels)
    
    # prediction 변환 (리스트 형태로 변환 후 정리)
    def process_predictions(pred, gt_labels):
        try:
            pred = pred.strip("{} ")  # 중괄호 제거
            labels = literal_eval(pred) if pred.startswith("[") else pred.split(",")
            pred_set = set(str(label).strip().lower().replace("\"", "").replace("'", "") for label in labels)
            
            # gt_label과 가장 유사한 label 찾기
            for pred_label in list(pred_set):
                closest_match = get_close_matches(pred_label, gt_labels, n=1, cutoff=0.7)
                if closest_match:
                    pred_set.remove(pred_label)
                    pred_set.add(closest_match[0])
            
            return pred_set
        except Exception:
            return set()
    
    df["final_prediction"] = df.apply(lambda row: process_predictions(row["prediction"], row["gt_label"]), axis=1)
    
    # Abstain 처리 (빈 값이거나 "abstain" 포함된 경우 필터링)
    def is_abstain(pred):
        return len(pred) == 0 or "abstain" in pred
    
    valid_df = df[~df["final_prediction"].apply(is_abstain)].copy()
    
    # 필터링된 데이터 저장
    valid_df.to_csv(output_csv, index=False)
    
    # coverage 계산
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples if total_samples > 0 else 0
    
    # Multi-label F1 score 계산
    y_true = valid_df["gt_label"]
    y_pred = valid_df["final_prediction"]
    
    def f1_per_sample(true, pred):
        if len(true) == 0 and len(pred) == 0:
            return 1  # 완전히 비어있는 경우 F1=1
        tp = len(true & pred)
        fp = len(pred - true)
        fn = len(true - pred)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    sample_f1_scores = valid_df.apply(lambda row: f1_per_sample(row["gt_label"], row["final_prediction"]), axis=1)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # 개선된 Micro-F1 score 계산 (전체 TP, FP, FN을 기반으로 계산)
    total_tp, total_fp, total_fn = 0, 0, 0
    for true_set, pred_set in zip(y_true, y_pred):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Hit metric 계산 (gt_label에 final_prediction 중 하나라도 포함되면 1, 아니면 0)
    hit = valid_df.apply(lambda row: 1 if len(row["gt_label"] & row["final_prediction"]) > 0 else 0, axis=1).mean()
    
    # 결과 출력
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }
    
    


def compute_metrics_ensemble(csv_files, output_csv="./filtered_data.csv"):

    # 여러 개의 CSV 파일을 로드하여 행 순서를 유지하면서 병합
    dfs = []
    for i, file in enumerate(csv_files):
        try:
            df = pd.read_csv(file)
            if set(["qid", "prediction", "gt_label"]) - set(df.columns):
                raise ValueError(f"{file}에 필요한 컬럼이 없습니다. 헤더가 없는 경우를 고려하세요.")
        except (pd.errors.ParserError, ValueError):
            df = pd.read_csv(file, header=None)
            if df.shape[1] != 3:
                raise ValueError(f"{file}의 컬럼 개수가 예상과 다릅니다. (예상: 3개)")
            df.columns = ["qid", "prediction", "gt_label"]
        df = df.rename(columns={"prediction": f"prediction_{i}"})
        dfs.append(df)
    
    # 행 순서를 유지하면서 병합 (qid 기준이 아니라 인덱스 기준)
    df = pd.concat(dfs, axis=1, ignore_index=False)
    df = df.loc[:, ~df.columns.duplicated()].copy()  # 중복되는 컬럼 제거
    
    # gt_label 변환 (리스트 형태로 변환 후 정리)
    def process_labels(label_str):
        try:
            labels = literal_eval(label_str) if isinstance(label_str, str) else label_str
            return set(str(label).strip().lower().replace("'", "") for label in labels)
        except (SyntaxError, ValueError, AttributeError):
            return set()
    
    df["gt_label"] = df["gt_label"].apply(process_labels)
    
    # prediction 변환 및 gt_label 기반 대체
    def process_predictions(pred, gt_labels):
        try:
            if isinstance(pred, float) or pred.strip().lower() == "abstain":
                return set(["abstain"])
            pred_list = literal_eval(pred) if isinstance(pred, str) and pred.startswith("[") else [pred]
            pred_set = set(str(label).strip().lower().replace("'", "") for label in pred_list)
            
            # gt_label과 가장 유사한 label 찾기
            matched_preds = set()
            for pred_label in pred_set:
                closest_match = get_close_matches(pred_label, gt_labels, n=1, cutoff=0.8)
                matched_preds.add(closest_match[0] if closest_match else pred_label)
            return matched_preds
        except Exception:
            return set(["abstain"])
    
    for i in range(len(csv_files)):
        prediction_col = f"prediction_{i}"
        df[prediction_col] = df.apply(lambda row: process_predictions(row[prediction_col], row["gt_label"]), axis=1)
    
    # 공통된 prediction 찾기
    def find_common_prediction(row):
        predictions = [row[f"prediction_{i}"] for i in range(len(csv_files))]
        if any("abstain" in pred for pred in predictions):
            return set(["abstain"])
        common_preds = set.intersection(*predictions)
        return common_preds if common_preds else set(["abstain"])
    
    df["final_prediction"] = df.apply(find_common_prediction, axis=1)
    
    # Abstain 처리 (빈 값이거나 "abstain" 포함된 경우 필터링)
    valid_df = df[df["final_prediction"].apply(lambda x: "abstain" not in x)].copy()
    
    # 필터링된 데이터 저장
    valid_df.to_csv(output_csv, index=False)
    
    # coverage 계산
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples if total_samples > 0 else 0
    
    # Multi-label F1 score 계산
    y_true = valid_df["gt_label"]
    y_pred = valid_df["final_prediction"]
    
    def f1_per_sample(true, pred):
        if len(true) == 0 and len(pred) == 0:
            return 1  # 완전히 비어있는 경우 F1=1
        tp = len(true & pred)
        fp = len(pred - true)
        fn = len(true - pred)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    sample_f1_scores = valid_df.apply(lambda row: f1_per_sample(row["gt_label"], row["final_prediction"]), axis=1)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # 개선된 Micro-F1 score 계산 (전체 TP, FP, FN을 기반으로 계산)
    total_tp, total_fp, total_fn = 0, 0, 0
    for true_set, pred_set in zip(y_true, y_pred):
        total_tp += len(true_set & pred_set)
        total_fp += len(pred_set - true_set)
        total_fn += len(true_set - pred_set)
    
    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Hit metric 계산 (gt_label에 final_prediction 중 하나라도 포함되면 1, 아니면 0)
    hit = valid_df.apply(lambda row: 1 if len(row["gt_label"] & row["final_prediction"]) > 0 else 0, axis=1).mean()
    
    # 결과 출력
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }




# 사용 예시
#metrics = compute_metrics("/nfs_edlab/smjo/KG-gpt2/ver_7_cronKG/results_final/without_kg/only_result.csv")
metrics = compute_metrics_ensemble(["/nfs_edlab/smjo/KG-gpt2/ver_7_cronKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.3_temp_0.5.csv", 
                                    "/nfs_edlab/smjo/KG-gpt2/ver_7_cronKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.7_temp_1.0.csv", 
                                    "/nfs_edlab/smjo/KG-gpt2/ver_7_cronKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.95_temp_1.5.csv"])
print(metrics)
