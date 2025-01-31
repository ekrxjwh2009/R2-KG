import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
import ast

def compute_metrics(csv_file):
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
    df["gt_label"] = df["gt_label"].astype(str).str.strip().str.lower().map(lambda x: x in ["true", "1"])
    
    # prediction 변환 (True/False 대소문자 및 숫자 처리)
    def convert_prediction(pred):
        pred = str(pred).strip().lower()
        if pred in ["true", "1"]:
            return 1
        elif pred in ["false", "0"]:
            return 0
        return "Abstain"
    
    df["final_prediction"] = df["prediction"].apply(convert_prediction)
    
    # Abstain이 아닌 데이터만 필터링
    valid_df = df[df["final_prediction"] != "Abstain"].copy()
    
    # coverage 계산
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples
    
    # prediction을 int로 변환
    valid_df["final_prediction"] = valid_df["final_prediction"].astype(int)
    y_true = df.loc[valid_df.index, "gt_label"].astype(int)
    y_pred = valid_df["final_prediction"]
    
    # micro-F1 score 계산
    precision = precision_score(y_true, y_pred, average="micro")
    recall = recall_score(y_true, y_pred, average="micro")
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # sample-wise F1 score 계산
    sample_f1_scores = f1_score(y_true, y_pred, average=None)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # Hit metric 계산
    hit = (y_true == y_pred).mean()
    
    # 결과 출력
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }


def compute_metrics_ensemble(csv_file):
    # CSV 파일 로드 (헤더 있는 경우와 없는 경우 처리)
    try:
        df = pd.read_csv(csv_file)
        if set(["qid", "predictions", "gt_label"]) - set(df.columns):
            raise ValueError("CSV 파일에 필요한 컬럼이 없습니다. 헤더가 없는 경우를 고려하세요.")
    except (pd.errors.ParserError, ValueError):
        df = pd.read_csv(csv_file, header=None)
        if df.shape[1] != 3:
            raise ValueError("CSV 파일의 컬럼 개수가 예상과 다릅니다. (예상: 3개)")
        df.columns = ["qid", "predictions", "gt_label"]
    
    # 데이터 타입 변환
    df["qid"] = df["qid"].astype(int)
    df["gt_label"] = df["gt_label"].astype(bool)
    
    # prediction 컬럼을 리스트로 변환
    df["predictions"] = df["predictions"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # 최종 prediction 결정
    def resolve_prediction(predictions):
        predictions = [str(p).strip().lower() for p in predictions]
        if "abstain" in predictions or len(set(predictions)) > 1:
            return "Abstain"
        return predictions[0] in ["true", "1"]  # True 값으로 인정되는 값들
    
    df["final_prediction"] = df["predictions"].apply(resolve_prediction)
    
    # Abstain이 아닌 데이터만 필터링
    valid_df = df[df["final_prediction"] != "Abstain"].copy()
    
    # coverage 계산
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples
    
    # prediction을 int로 변환
    valid_df["final_prediction"] = valid_df["final_prediction"].astype(int)
    y_true = df.loc[valid_df.index, "gt_label"].astype(int)
    y_pred = valid_df["final_prediction"]
    
    # micro-F1 score 계산
    precision = precision_score(y_true, y_pred, average="micro")
    recall = recall_score(y_true, y_pred, average="micro")
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # sample-wise F1 score 계산
    sample_f1_scores = f1_score(y_true, y_pred, average=None)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # Hit metric 계산
    hit = (y_true == y_pred).mean()
    
    # 결과 출력
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }

def compute_metrics_ensemble_3files(csv_files, output_csv="ensemble_results.csv"):
    # 여러 개의 CSV 파일을 병합하여 ensemble 수행
    #dfs = [pd.read_csv(file) for file in csv_files]
    dfs=[]
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            if set(["qid", "prediction", "gt_label"]) - set(df.columns):
                raise ValueError("CSV 파일에 필요한 컬럼이 없습니다. 헤더가 없는 경우를 고려하세요.")
        except (pd.errors.ParserError, ValueError):
            df = pd.read_csv(csv_file, header=None)
            if df.shape[1] != 3:
                raise ValueError("CSV 파일의 컬럼 개수가 예상과 다릅니다. (예상: 3개)")
            df.columns = ["qid", "prediction", "gt_label"]
        dfs.append((df))
    
    
    # 모든 파일이 같은 qid, gt_label을 가져야 함
    for df in dfs:
        if set(["qid", "prediction", "gt_label"]) - set(df.columns):
            raise ValueError("CSV 파일에 필요한 컬럼이 없습니다.")
    # 데이터 병합 (qid 기준 정렬)
    for df in dfs:
        df["qid"] = df["qid"].astype(str)  # qid를 문자열로 변환하여 정렬 오류 방지
    
    # 데이터 병합 (qid 기준 정렬)
    df = pd.concat(dfs, axis=0, ignore_index=True).sort_values(by="qid")
    df = df.groupby("qid").agg({"prediction": list, "gt_label": "first"}).reset_index()
    
    # 데이터 타입 변환
    df["qid"] = df["qid"].astype(int)
    df["gt_label"] = df["gt_label"].astype(bool)
    
    # 최종 prediction 결정
    def resolve_prediction(predictions):
        predictions = [str(p).strip().lower() for p in predictions]
        if "abstain" in predictions or len(set(predictions)) > 1:
            return "Abstain"
        return predictions[0] in ["true", "1"]  # True 값으로 인정되는 값들
    
    df["final_prediction"] = df["prediction"].apply(resolve_prediction)
    
    # Abstain이 아닌 데이터만 필터링
    valid_df = df[df["final_prediction"] != "Abstain"].copy()
    
    # coverage 계산
    total_samples = len(df)
    valid_samples = len(valid_df)
    coverage = valid_samples / total_samples
    
    # prediction을 int로 변환
    valid_df["final_prediction"] = valid_df["final_prediction"].astype(int)
    y_true = df.loc[valid_df.index, "gt_label"].astype(int)
    y_pred = valid_df["final_prediction"]
    
    # micro-F1 score 계산
    precision = precision_score(y_true, y_pred, average="micro")
    recall = recall_score(y_true, y_pred, average="micro")
    micro_f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # sample-wise F1 score 계산
    sample_f1_scores = f1_score(y_true, y_pred, average=None)
    sample_wise_f1 = sample_f1_scores.mean()
    
    # Hit metric 계산
    hit = (y_true == y_pred).mean()
    
    # 결과 저장
    df.to_csv(output_csv, index=False)
    
    return {
        "Coverage": coverage,
        "Micro-F1 Score": micro_f1,
        "Sample-wise F1 Score": sample_wise_f1,
        "Hit": hit
    }




#metrics = compute_metrics("/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/without_kg/only_result.csv")
#metrics = compute_metrics_ensemble("/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/Paraphrase/qwen_14b/Processed/all_trials_results.csv")
metrics = compute_metrics_ensemble_3files(["/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.3_temp_0.5.csv",
                                           "/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.7_temp_1.0.csv",
                                           "/nfs_edlab/smjo/KG-gpt2/ver_7_factKG/results_final/Parameter_ensemble/gpt-4o-mini/only_result_top_p_0.95_temp_1.5.csv"])
print(metrics)
