"""
Column Mapping Similarity Tool
Compares two CSV tables and suggests column mappings based on similarity measures.
"""

import re
import pandas as pd
import editdistance

from collections import Counter


# ========== CONFIG ==========
CSV1 = "table1.csv"
CSV2 = "table2.csv"

NGRAM_N = 3
TOP_N_CANDIDATES = 15

W_NGRAM = 0.1
W_PATTERN = 0.1
W_COLNAME = 0.1
W_OVERLAP = 2.0
# ============================


def normalize_value(x):
    """
    Normalize textual values for comparison.
    """
    x = re.sub(r'\s+', ' ', str(x).strip().lower())

    if (len(x) > 9 and re.fullmatch(r'\d+', x)) or not x.strip("0"):
        x = x.lstrip("0")
    return x


def char_ngrams_set(x, n=NGRAM_N):
    """
    Generate character n-grams from a string.
    """
    x = re.sub(r'\s+', ' ', str(x).strip().lower())

    if (len(x) > 9 and re.fullmatch(r'\d+', x)) or not x.strip("0"):
        x = x.lstrip("0")

    padded = "#" * (n-1) + x + "$" * (n-1)
    ngrams = set()
    for i in range(len(padded) - n + 1):
        ngrams.add(padded[i:i+n])
    return ngrams


def detect_pattern(x):
    """
    Convert a value into a simplified pattern: digits -> '#', letters -> 'A', others -> '?'
    """
    pattern = ""
    for ch in str(x):
        if ch.isdigit():
            pattern += "#"
        elif ch.isalpha():
            pattern += "A"
        else:
            pattern += "?"
    return pattern


def jaccard(a, b):
    """
    Compute Jaccard similarity between two sets.
    """
    if not a and not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union > 0 else 0.0


def column_name_similarity(col1, col2):
    """
    Compute normalized edit distance similarity between column names.
    """
    clean1 = re.sub(r'[^a-z0-9]', '', col1.lower())
    clean2 = re.sub(r'[^a-z0-9]', '', col2.lower())

    if not clean1 or not clean2:
        return 0.0

    dist = editdistance.eval(clean1, clean2)
    dist = 1 - (dist / max(len(clean1), len(clean2)))
    return max(dist, 0.0)


def build_column_profile(series):
    """
    Generate statistical and textual profile for a column.
    """
    total_count = len(series)
    nonnull_series = series.dropna().astype(str).map(normalize_value)
    nonnull_series = nonnull_series[nonnull_series != ""]
    nonnull_count = len(nonnull_series)
    null_count = total_count - nonnull_count
    sample_factor = int(nonnull_count * 0.1)

    if nonnull_count == 0:
        return {
            "count": 0,
            "total": total_count,
            "nulls": null_count,
            "unique_ratio": 0,
            "avg_len": 0,
            "top_values_set": set(),
            "ngram_union": set(),
            "patterns": set()
        }

    sample = nonnull_series.sample(nonnull_count, random_state=42)

    unique_ratio = sample.nunique() / len(sample)
    avg_len = sample.map(len).mean()

    top = Counter(sample).most_common(sample_factor)
    top_values_set = set()
    for v, _ in top:
        top_values_set.add(v)

    ngram_union = set()
    patterns = set()
    for v in list(sample.head(sample_factor)):
        ngram_union |= char_ngrams_set(v)
        patterns.add(detect_pattern(v))

    profile = {
        "count": nonnull_count,
        "total": total_count,
        "nulls": null_count,
        "unique_ratio": unique_ratio,
        "avg_len": avg_len,
        "top_values_set": top_values_set,
        "ngram_union": ngram_union,
        "patterns": patterns
    }

    return profile


def profile_similarity(p1, p2, col1, col2):
    """
    Compute similarity between two column profiles.
    Combines ngram, pattern, column name similarity, and value overlap.
    """
    if p1["count"] == 0 or p2["count"] == 0:
        return 0.0, {
            "ngram": 0,
            "pattern": 0,
            "colname": 0,
            "overlap": 0
        }

    ngram_score = jaccard(p1["ngram_union"], p2["ngram_union"])
    pattern_score = jaccard(p1["patterns"], p2["patterns"])
    colname_score = column_name_similarity(col1, col2)
    overlap_score = jaccard(p1["top_values_set"], p2["top_values_set"])

    base_score = (
        W_NGRAM * ngram_score +
        W_PATTERN * pattern_score +
        W_COLNAME * colname_score +
        W_OVERLAP * overlap_score
    )

    components = {}
    components["ngram"] = round(ngram_score, 4)
    components["pattern"] = round(pattern_score, 4)
    components["colname"] = round(colname_score, 4)
    components["overlap"] = round(overlap_score, 4)

    return round(base_score, 4), components


def suggest_mappings(df1, df2):
    """
    Suggest column mappings between two tables.
    """
    profiles1 = {}
    for col in df1.columns:
        profiles1[col] = build_column_profile(df1[col])

    profiles2 = {}
    for col in df2.columns:
        profiles2[col] = build_column_profile(df2[col])

    rows = []

    for c1, p1 in profiles1.items():
        candidate_scores = {}

        for c2, p2 in profiles2.items():
            score, comps = profile_similarity(p1, p2, c1, c2)
            candidate_scores[c2] = (score, comps, p1, p2)

        best_candidates = sorted(candidate_scores.items(), key=lambda x: x[1][0], reverse=True)[:TOP_N_CANDIDATES]

        if not best_candidates:
            row = {}
            row["table1_col"] = c1
            row["table2_col"] = None
            row["score"] = 0
            row["rank"] = None
            row["ngram"] = 0
            row["pattern"] = 0
            row["colname_ngram"] = 0
            row["overlap"] = 0
            row["table1_total"] = p1["total"]
            row["table1_nulls"] = p1["nulls"]
            row["table1_nonnulls"] = p1["count"]
            row["table2_total"] = 0
            row["table2_nulls"] = 0
            row["table2_nonnulls"] = 0
            rows.append(row)
        else:
            for rank, (c2, (sc, comps, p1d, p2d)) in enumerate(best_candidates, start=1):
                row = {}
                row["table1_col"] = c1
                row["table2_col"] = c2
                row["score"] = sc
                row["rank"] = rank
                row["ngram"] = comps["ngram"]
                row["pattern"] = comps["pattern"]
                row["colname_ngram"] = comps["colname"]
                row["overlap"] = comps["overlap"]
                row["table1_total"] = p1d["total"]
                row["table1_nulls"] = p1d["nulls"]
                row["table1_nonnulls"] = p1d["count"]
                row["table2_total"] = p2d["total"]
                row["table2_nulls"] = p2d["nulls"]
                row["table2_nonnulls"] = p2d["count"]
                rows.append(row)

    df_results = pd.DataFrame(rows)
    df_results = df_results.sort_values(["table1_col", "rank"], na_position="last")
    return df_results


if __name__ == "__main__":
    print("Reading CSV files...")
    df1 = pd.read_csv(CSV1, dtype=str, low_memory=False)
    df2 = pd.read_csv(CSV2, dtype=str, low_memory=False)

    print("Generating column mapping suggestions...")
    suggestions = suggest_mappings(df1, df2)

    print("Saving results to 'cmapping.csv'...")
    suggestions.to_csv("cmapping.csv", index=False)

    print("Process completed successfully.")
